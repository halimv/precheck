"""Experimental fidelity: a plan does the SOP's experiment at the SOP's quantities (pipeline/fidelity.py).

The requirements are read from the SOP and checked against its text; the plan's tagged steps are held to them: no
scaled volume, no lost number, nothing missing, out of order or added; only the scientist's own revision request may
change an SOP quantity."""
import copy
import io
import json
import sys
from pathlib import Path

import pytest

from pipeline import fidelity
from pipeline.flow import NotFaithful, finish
from pipeline.self_heal import apply_valid_edits
from pipeline.summary import review_items

DECK = json.loads((Path(__file__).parent / "fixtures" / "serial_deck.json").read_text())
KINDS = {lid: spec["kind"] for lid, spec in DECK["labware"].items()}
ALL = list(range(8))
SOP = """1.1 Place 10 mg tissue in each tube.
1.2 Add 180 µl Buffer ATL.
1.3 Add 20 µl proteinase K and mix by pipetting.
1.4 Incubate at 56°C for 30 min.
1.5 Store the lysate at 4°C."""
REQS = [
    {"id": "R1", "section": "1.1", "kind": "step", "what": "place tissue", "values": [{"value": 10, "unit": "mg"}],
     "quote": "Place 10 mg tissue in each tube."},
    {"id": "R2", "section": "1.2", "kind": "addition", "what": "Buffer ATL", "volume_ul": 180, "values": [],
     "quote": "Add 180 µl Buffer ATL."},
    {"id": "R3", "section": "1.3", "kind": "addition", "what": "proteinase K", "volume_ul": 20, "values": [],
     "quote": "Add 20 µl proteinase K and mix by pipetting."},
    {"id": "R4", "section": "1.3", "kind": "step", "what": "mix by pipetting", "values": [],
     "quote": "Add 20 µl proteinase K and mix by pipetting."},
    {"id": "R5", "section": "1.4", "kind": "step", "what": "incubate",
     "values": [{"value": 56, "unit": "C"}, {"value": 30, "unit": "min"}], "quote": "Incubate at 56°C for 30 min."},
    {"id": "R6", "section": "1.5", "kind": "step", "what": "store", "values": [{"value": 4, "unit": "C"}],
     "quote": "Store the lysate at 4°C."},
]


def step(action, labware, **kw):
    return {"action": action, "labware": labware, "volume_ul": kw.pop("volume_ul", 0), "channels": kw.pop("channels", ALL),
            "description": action, **kw}


def plan(atl=180.0, pk=20.0, atl_split=1):
    steps = [step("manual", "dilution_plate", channels=[0], sop="R1",
                  instruction="Place 10 mg minced tissue in each well of dilution_plate column 1"),
             step("tips_on", "tips", column=1)]
    for _ in range(atl_split):
        steps += [step("aspirate", "diluent", volume_ul=atl / atl_split),
                  step("dispense", "dilution_plate", column=1, volume_ul=atl / atl_split, sop="R2")]
    steps += [step("tips_off", "waste"),
              step("tips_on", "tips", column=2),
              step("aspirate", "culture", volume_ul=pk),
              step("dispense", "dilution_plate", column=1, volume_ul=pk, sop="R3"),
              step("aspirate", "dilution_plate", column=1, volume_ul=100, sop="R4"),
              step("dispense", "dilution_plate", column=1, volume_ul=100, sop="R4"),
              step("tips_off", "waste"),
              step("manual", "dilution_plate", channels=[0], sop="R5", duration_min=30,
                   instruction="Incubate dilution_plate at 56 C for 30 min")]
    for i, s in enumerate(steps, start=1):
        s["step"] = i
    return {"protocol_name": "lysis", "labware": {}, "reagents": {"diluent": "Buffer ATL", "culture": "Proteinase K"},
            "initial_volumes_ul": {"diluent": 3000, "culture": 400}, "steps": steps, "requirements": copy.deepcopy(REQS),
            "outside_run": ["R6"]}


def errors(p, notes=()):
    return fidelity.check(p, KINDS, notes)["errors"]


# --- the requirements, against the SOP ---

def test_the_requirements_hold_against_the_sop_text():
    assert fidelity.spec_errors({"requirements": REQS}, SOP) == []
    invented = [{**REQS[1], "quote": "Add 72 ul Buffer ATL."}]
    assert "is not in the SOP" in fidelity.spec_errors({"requirements": invented}, SOP)[0]
    misread = [{**REQS[1], "volume_ul": 72}]
    assert "volume_ul 72 is not a volume written in its quote" in fidelity.spec_errors({"requirements": misread}, SOP)[0]
    lost = [{**REQS[4], "values": [{"value": 37, "unit": "C"}]}]
    assert "the value 37 C is not written in its quote" in fidelity.spec_errors({"requirements": lost}, SOP)[0]
    ml = [{"id": "R1", "kind": "addition", "what": "ethanol", "volume_ul": 1200, "quote": "Add 1.2 mL ethanol."}]
    assert fidelity.spec_errors({"requirements": ml}, "Then add 1.2  mL ethanol. Mix.") == []
    spin = [{"id": "R1", "kind": "step", "what": "spin", "values": [{"value": 20000, "unit": "x g"}, {"value": 3, "unit": "min"}],
             "quote": "Centrifuge for 3 minutes at 20,000 x g."}]
    assert fidelity.spec_errors({"requirements": spin}, "Centrifuge for 3 minutes at 20,000 x g.") == []
    tissue = [{"id": "R1", "kind": "step", "what": "tissue", "values": [{"min": 12, "max": 15, "unit": "mg"}],
               "quote": "Use 12-15 mg spleen."}]
    assert fidelity.spec_errors({"requirements": tissue}, "Use 12-15 mg spleen.") == []
    assert "12-15 mg" in fidelity.describe(tissue[0])
    least = [{"id": "R1", "kind": "step", "what": "spin", "values": [{"min": 6000, "unit": "x g"}],
              "quote": "Centrifuge at \u22656000 x g for 1 minute."}]
    assert fidelity.spec_errors({"requirements": least}, "Centrifuge at \u22656000 x g for 1 minute.") == []
    assert ">=6000 x g" in fidelity.describe(least[0])


# --- the plan, against the requirements ---

def test_the_sops_plan_passes_and_the_report_says_how_each_requirement_is_done():
    result = fidelity.check(plan(), KINDS)
    assert result["errors"] == [] and result["samples"] == 8
    rows = {r["id"]: r for r in result["requirements"]}
    assert rows["R2"]["per_sample_ul"] == [180.0] and rows["R2"]["from"] == ["diluent (Buffer ATL)"]
    assert rows["R1"]["how"] == "by hand" and rows["R4"]["how"] == "on the robot"
    assert rows["R6"]["how"] == "before or after the run, by hand"


def test_a_scaled_volume_is_refused_and_split_dispenses_that_add_up_are_not():
    scaled = errors(plan(atl=72, pk=8))
    assert any("R2 (1.2) add 180 uL of Buffer ATL" in e and "gets 72 uL" in e and "not a scaled one" in e for e in scaled)
    assert any("R3" in e and "gets 8 uL" in e for e in scaled)
    assert errors(plan(atl_split=2)) == []  # 2 x 90 uL is the SOP's 180


def test_a_manual_step_keeps_the_sops_numbers():
    p = plan()
    p["steps"][-1]["instruction"] = "Incubate dilution_plate at 56 C until lysed"
    assert any("does not keep 30 min" in e for e in errors(p))
    p = plan()
    p["steps"][0]["instruction"] = "Place 4 mg minced tissue in each well"  # tissue scaled with the volumes
    assert any("R1" in e and "does not keep 10 mg" in e for e in errors(p))


def test_a_manual_addition_says_the_volume():
    p = plan()
    p["steps"] = [s for s in p["steps"] if s.get("sop") != "R2" and not (s["action"] == "aspirate" and s["labware"] == "diluent")]
    p["steps"].insert(1, step("manual", "dilution_plate", channels=[0], sop="R2", instruction="Add Buffer ATL to each well"))
    assert any("manual instruction does not say 180 uL" in e for e in errors(p))
    p["steps"][1]["instruction"] = "Add 180 uL Buffer ATL to each well of column 1"
    assert errors(p) == []


def test_nothing_is_missing_out_of_order_or_added():
    p = plan()
    p["steps"] = [s for s in p["steps"] if s.get("sop") != "R5"]
    assert any("R5 (1.4) incubate" in e and "is not carried out" in e for e in errors(p))

    p = plan()
    p["outside_run"] = ["R4", "R6"]  # one in the middle
    assert any("only the first or last requirements" in e for e in errors(p))

    p = plan()
    p["steps"][0]["sop"] = "R3"  # the tissue step now claims an addition that comes later
    p["steps"][7]["sop"] = "R1"
    assert any("comes before" in e and "keep the SOP's order" in e for e in errors(p))

    p = plan()
    del p["steps"][3]["sop"]  # Buffer ATL into the samples with no requirement for it
    assert any("dispenses diluent into dilution_plate, but no SOP requirement says so" in e for e in errors(p))

    p = plan()
    p["reagents"]["diluent"] = "Buffer AL"  # the wrong buffer
    assert any("does not hold Buffer ATL" in e for e in errors(p))


def test_only_the_scientists_request_changes_an_sop_quantity():
    p = plan(atl=72)
    p["deviations"] = [{"sop": "R2", "volume_ul": 72, "approved": "use 72 uL of ATL"}]
    assert any("without the scientist's request" in e for e in errors(p))  # the drafter's own idea
    p["revisions"] = [{"note": "Please use 72 uL of ATL to save buffer.", "from": "lysis.json"}]
    assert errors(p) == []
    result = fidelity.check(p, KINDS)
    items = review_items(p, [], {"assumptions": [], "wells": []}, [], {}, fidelity=result)
    assert any(i["severity"] == "must" and "changed to 72 uL per sample" in i["item"] for i in items)
    assert errors(plan(atl=72), notes=("use 72 uL of ATL",)) != []  # a note alone does not change the plan's deviations


def test_a_plan_with_no_requirements_is_flagged_for_the_scientist():
    result = fidelity.check({"steps": []}, KINDS)
    assert result["checked"] is False
    items = review_items({"steps": []}, [], {"assumptions": [], "wells": []}, [], {}, fidelity=result)
    assert items[0]["severity"] == "must" and items[0]["item"] == "Not checked against an SOP"


# --- the rest of the pipeline keeps it ---

def test_a_repair_that_splits_a_step_keeps_its_requirement():
    p = plan()
    split = [{k: v for k, v in step("dispense", "dilution_plate", column=1, volume_ul=180, channels=[c]).items()}
             for c in range(8)]
    new, applied, errs = apply_valid_edits(p, [{"op": "replace_step", "step": 4, "new_steps": split}], KINDS)
    assert errs == [] and all(s["sop"] == "R2" for s in new["steps"][3:11])
    assert errors(new) == []


def test_finish_writes_nothing_for_a_plan_that_changes_the_sop(tmp_path):
    with pytest.raises(NotFaithful, match="gets 72 uL"):
        finish(plan(atl=72), DECK, "scaled", [], healed=tmp_path)
    assert not list(tmp_path.iterdir())
    report = finish(plan(), DECK, "faithful", [], healed=tmp_path)
    assert report["fidelity"]["checked"] and report["fidelity"]["samples"] == 8
    assert "## What the SOP requires" in (tmp_path / "faithful_summary.md").read_text()


def test_the_drafter_sends_a_scaled_plan_back(tmp_path, monkeypatch):
    """A stand-in CLI reads the requirements, drafts with scaled volumes, and, told so, uses the SOP's."""
    import pipeline.stage0_drafter as drafter
    from test_deck_builder import SERIAL_DILUTION, base

    def drafted(atl):
        p = plan(atl=atl)
        p.pop("requirements")
        p["labware"] = {k: v for k, v in SERIAL_DILUTION.items() if k != "saline"}
        p["labware"]["diluent"] = SERIAL_DILUTION["saline"]
        return p

    prompts = tmp_path / "prompts.jsonl"
    fake = tmp_path / "claude"
    fake.write_text(f"""#!{sys.executable}
import json, sys
prompt = sys.stdin.read()
open({str(prompts)!r}, "a").write(json.dumps(prompt) + "\\n")
if "list what the experiment requires" in prompt:
    reply = {json.dumps({"requirements": REQS})!r}
elif "does not do what the SOP says" in prompt:
    reply = {json.dumps(drafted(180))!r}
else:
    reply = {json.dumps(drafted(72))!r}
print(json.dumps({{"type": "result", "is_error": False, "result": "```json\\n" + reply + "\\n```", "session_id": "s"}}))
""")
    fake.chmod(0o755)
    monkeypatch.setattr(drafter, "CLAUDE_BIN", str(fake))
    d = drafter.draft(SOP, base(), out=io.StringIO(), drafts_dir=tmp_path / "drafts", decks_dir=tmp_path / "decks",
                      stem="lysis")
    sent = [json.loads(line) for line in prompts.read_text().splitlines()]
    assert len(sent) == 3 and "never scale them" in sent[1] and "R2 (1.2) add 180 uL of Buffer ATL" in sent[1]
    assert "gets 72 uL" in sent[2]
    assert d.protocol["requirements"] == REQS and d.protocol["requirements_scope"]["quotes_checked"] is True
    assert {s["volume_ul"] for s in d.protocol["steps"] if s.get("sop") == "R2"} == {180.0}
