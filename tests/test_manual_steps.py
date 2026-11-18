"""Manual steps: work the operator does by hand because the robot cannot (centrifuge, vortex, incubate off deck).
They stay in the protocol, compile to pipeline.pipetting.manual_step (which asks the operator, or logs in simulation),
empty the wells they name, and the intent guard keeps each one and what the wells hold when it comes."""
import copy
import json
from pathlib import Path

import pytest

from pipeline import pipetting
from pipeline.design_review import trace_mixtures
from pipeline.flow import manual_steps
from pipeline.self_heal import SelfHealer
from pipeline.stage0_drafter import structural_errors
from pipeline.labware_limits import labware_limits
from pipeline.stage1_verifier import Verifier
from pipeline.stage2_compiler import CompilationError, compile_protocol, translate_step
from pipeline.summary import review_items

DECK = json.loads((Path(__file__).parent / "fixtures" / "serial_deck.json").read_text())
KINDS = {lid: spec["kind"] for lid, spec in DECK["labware"].items()}
ALL = [0, 1, 2, 3, 4, 5, 6, 7]
SPIN = "Centrifuge dilution_plate at 6000 x g for 1 min and discard the flow-through"


def step(action, labware, **kw):
    return {"action": action, "labware": labware, "volume_ul": kw.pop("volume_ul", 0), "channels": kw.pop("channels", ALL),
            "description": kw.pop("description", action), **kw}


def protocol(manual=True, empties=True):
    steps = [step("tips_on", "tips", column=1),
             step("aspirate", "diluent", volume_ul=150),
             step("dispense", "dilution_plate", column=1, volume_ul=150),
             step("tips_off", "waste")]
    if manual:
        steps.append(step("manual", "dilution_plate", channels=[0], instruction=SPIN, duration_min=1,
                          **({"empties": [{"labware": "dilution_plate", "column": 1}]} if empties else {})))
    steps += [step("tips_on", "tips", column=2),
              step("aspirate", "culture", volume_ul=20),
              step("dispense", "dilution_plate", column=1, volume_ul=20),
              step("tips_off", "waste")]
    for i, s in enumerate(steps, start=1):
        s["step"] = i
    return {"protocol_name": "manual test", "labware": {}, "reagents": {"diluent": "buffer", "culture": "sample"},
            "initial_volumes_ul": {"diluent": 5000, "culture": 400}, "steps": steps}


def test_a_manual_step_compiles_to_the_operator_helper_with_the_wells_it_empties():
    code = compile_protocol(protocol(), DECK)
    assert "from pipeline.pipetting import aspirate, dispense, manual_step, tips_off, tips_on" in code
    line = next(l for l in code.splitlines() if "manual_step(lh" in l).strip()
    assert line.startswith(f"await manual_step(lh, {SPIN!r}, empties=[")
    assert 'res["dilution_plate"].get_item("A1")' in line and 'res["dilution_plate"].get_item("H1")' in line
    assert "manual_step" not in compile_protocol(protocol(manual=False), DECK)


def test_a_manual_step_needs_an_instruction_and_empties_must_name_plate_columns():
    with pytest.raises(CompilationError, match="instruction"):
        translate_step(step("manual", "dilution_plate", step=1), KINDS)
    with pytest.raises(CompilationError, match="not a plate"):
        translate_step(step("manual", "dilution_plate", step=1, instruction="x", empties=[{"labware": "diluent", "column": 1}]), KINDS)
    with pytest.raises(CompilationError, match="1-12"):
        translate_step(step("manual", "dilution_plate", step=1, instruction="x", empties=[{"labware": "dilution_plate", "column": 13}]), KINDS)


def test_the_drafter_accepts_a_manual_step():
    plan = {**protocol(), "labware": {"tips": {"kind": "tip_rack", "tip_volume_ul": 300},
                                      "diluent": {"kind": "reservoir", "min_capacity_ul": 8000},
                                      "culture": {"kind": "tube", "min_capacity_ul": 1000},
                                      "dilution_plate": {"kind": "plate", "wells": 96, "min_capacity_ul": 200},
                                      "waste": {"kind": "waste"}}}
    assert structural_errors(plan) == []


def test_the_gate_passes_it_and_the_wells_it_empties_hold_nothing_afterwards(tmp_path):
    gate = SelfHealer(DECK, work_dir=str(tmp_path)).evaluate(protocol(), 0)
    assert gate.passed, gate.feedback
    where, _ = trace_mixtures(protocol(), KINDS)
    assert where[("dilution_plate", 1, 0)] == {"sample": 20.0}  # the buffer was spun through and discarded


def test_simulation_logs_the_step_and_a_handler_is_asked(tmp_path):
    asked = []
    pipetting.set_manual_handler(asked.append)
    try:
        assert SelfHealer(DECK, work_dir=str(tmp_path)).evaluate(protocol(), 0).passed
    finally:
        pipetting.set_manual_handler(None)
    assert asked == [SPIN]


def test_the_verifier_wants_tips_off_before_a_manual_step(tmp_path):
    ir = protocol()
    ir["steps"] = [s for s in ir["steps"] if s["step"] != 4]  # the tips stay on into the manual step
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps(ir))
    verdict = Verifier(labware_limits(DECK), str(plan)).run_verification()
    assert verdict["error_code"] == "TIPS_DURING_HOLD", verdict
    plan.write_text(json.dumps(protocol()))
    assert Verifier(labware_limits(DECK), str(plan)).run_verification().get("error_code") != "TIPS_DURING_HOLD"


def test_the_intent_guard_keeps_each_manual_step_and_what_the_wells_hold_when_it_comes(tmp_path):
    healer = SelfHealer(DECK, work_dir=str(tmp_path))
    base = healer._transfers(protocol())
    assert ("manual", 0, SPIN[:60]) in base
    assert healer._intent_violations(base, healer._transfers(copy.deepcopy(protocol()))) == []

    removed = healer._intent_violations(base, healer._transfers(protocol(manual=False)))
    assert any("manual step 1" in c and "removed or changed" in c for c in removed)

    moved = protocol()  # the culture added before the spin: same final well, different well at the manual step
    s = moved["steps"]
    s[:] = s[:4] + s[5:] + [s[4]]
    for i, x in enumerate(s, start=1):
        x["step"] = i
    changed = healer._intent_violations(base, healer._transfers(moved))
    assert any("when manual step 1" in c for c in changed), changed

    reworded = protocol()
    reworded["steps"][4]["instruction"] = "Vortex the plate"
    assert any("manual step 1" in c for c in healer._intent_violations(base, healer._transfers(reworded)))


def test_the_report_lists_manual_steps_as_ahc_asks_for_them():
    listed = manual_steps(protocol())
    assert listed == [{"step": 5, "instruction": SPIN, "labware": "dilution_plate", "duration_min": 1,
                       "empties": ["dilution_plate:A1:H1"]}]
    items = review_items(protocol(), [], {"assumptions": [], "wells": []}, [], {})
    assert any(i["area"] == "manual" and "Step 5 is done by hand (about 1 min)" in i["item"] for i in items)
