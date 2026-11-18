"""What a run tells the scientist: a summary file, and the list of things that need a person's review.

Every run gets a summary. A protocol that passed gets it next to its files in healed/; one that did not pass gets it
in the working folder's build/ instead, because nothing is written to healed/ for a protocol that does not pass.

Each review item has a severity:
- "must": the protocol cannot be run as it stands (AHC cannot load an item, an operator has to place something before
  the run, or the run did not pass).
- "check": a choice that was made for the scientist and should be confirmed (an assumption, a repair that changed the
  steps, labware that AHC substitutes, a liquid that is too shallow to draw from reliably).
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _mapping_for(deck_path: Optional[Path]) -> Dict[str, Any]:
    """The deck mapping the drafter wrote beside a deck config (what was placed where, and what the operator adds)."""
    if deck_path is None:
        return {}
    mapping = deck_path.with_suffix(".mapping.json")
    return json.loads(mapping.read_text()) if mapping.exists() else {}


def review_items(protocol: Dict[str, Any], rounds: List[Dict[str, Any]], review: Dict[str, Any],
                 suggestions: List[Dict[str, Any]], ahc: Dict[str, Any], deck_path: Optional[Path] = None,
                 passed: bool = True, fidelity: Optional[Dict[str, Any]] = None,
                 target: str = "lab") -> List[Dict[str, str]]:
    """What the scientist reviews, most important first. `target` "plr" is precheck alone (PyLabRobot's catalog,
    no lab deck): what AHC would make of the deck is not part of it."""
    items: List[Dict[str, str]] = []
    with_ahc = target != "plr"

    def add(severity: str, area: str, item: str, detail: str = "") -> None:
        items.append({"severity": severity, "area": area, "item": item, "detail": detail})

    if not passed:
        add("must", "run", "Not ready", "The protocol did not pass the simulator; nothing was written to healed/.")
    for change in _mapping_for(deck_path).get("operator_changes", []):
        add("must", "deck", "Place on the deck before the run", change)
    for problem in ahc.get("not_on_layout", []) if with_ahc else []:
        add("must", "AHC", "AHC cannot load this item", problem)
    fid = fidelity or {}
    if fidelity is not None and not fid.get("checked"):
        add("must", "fidelity", "Not checked against an SOP",
            "This plan has no requirements read from an SOP, so nothing checked that its volumes and numbers are the "
            "SOP's. Compare it with the SOP yourself.")
    elif fid.get("checked"):
        rows = fid.get("requirements", [])
        scope = fid.get("scope") or {}
        left = "; ".join(scope.get("left_out") or [])
        add("check", "fidelity", f"Held to {len(rows)} requirements read from the SOP"
            + (f" ({scope['covered']})" if scope.get("covered") else ""),
            "Every volume and number below is the SOP's. Confirm none is missing." + (f" Left out: {left}." if left else "")
            + ("" if scope.get("quotes_checked", True) else " The SOP is a scan: its quotes could not be checked."))
        for r in rows:
            if r.get("deviation"):
                d = r["deviation"]
                change = ("left out" if d.get("omit") else f"{d['volume_ul']:g} uL per sample" if "volume_ul" in d
                          else "values " + ", ".join(str(v.get("value", f"{v.get('min')}-{v.get('max')}")) + f" {v.get('unit', '')}"
                                             for v in d.get("values", [])))
                add("must", "fidelity", f"{r['requirement']}: changed to {change}", f"You asked: \"{d.get('approved')}\"")
            elif r.get("how") == "before or after the run, by hand":
                add("check", "fidelity", f"{r['requirement']}: done before or after the run, not in the plan", r.get("quote", ""))
            elif r.get("kind") == "step" and r.get("how") == "on the robot":
                add("check", "fidelity", f"{r['requirement']}: done on the robot (steps {_span(r['steps'])})",
                    f"The SOP says: \"{r.get('quote')}\". Confirm the robot's way does the same.")
    for s in protocol.get("steps", []):
        if s.get("action") == "manual":
            took = f" (about {s['duration_min']:g} min)" if isinstance(s.get("duration_min"), (int, float)) else ""
            add("check", "manual", f"Step {s.get('step')} is done by hand{took}",
                f"{s.get('instruction')}. The robot waits for the operator (AHC asks them with request_manual_step).")
    for assumption in review.get("assumptions", []):
        add("check", "drafting", "Assumption made when drafting", assumption)
    for warning in ahc.get("differs_from_venus", []) if with_ahc else []:
        add("check", "AHC", "AHC's model differs from VENUS", warning)
    for round_ in rounds:
        applied = round_.get("edits_applied")
        if applied:
            model = round_.get("model", "")
            add("check", "repair", f"Repair in round {round_['round']} ({model})",
                f"{len(applied)} edit(s) to the steps after: {round_.get('result', '')}")
    for suggestion in suggestions:
        if suggestion.get("id") == "liquid_too_shallow":
            add("must", "liquid", suggestion["title"], suggestion["detail"])
    for well in review.get("wells", []):
        for flag in well.get("flags", []):
            add("check", "wells", f"{well['plate']} column {well['column']}: {flag}")
    return items


def _span(steps: List[Any]) -> str:
    nums = [n for n in steps if isinstance(n, int)]
    return f"{min(nums)}-{max(nums)}" if len(nums) > 1 else ", ".join(map(str, steps))


def _table(rows: List[List[str]], head: List[str]) -> List[str]:
    if not rows:
        return ["_none_", ""]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c).replace("|", "/") for c in row) + " |" for row in rows]
    return out + [""]


def markdown(protocol: Dict[str, Any], rounds: List[Dict[str, Any]], tiers: List[Dict[str, Any]], review: Dict[str, Any],
             items: List[Dict[str, str]], files: Dict[str, str], passed: bool,
             fidelity: Optional[Dict[str, Any]] = None, target: str = "lab") -> str:
    from pipeline.flow import passed_banner
    head = passed_banner(target) if passed else "NOT READY: did not pass the simulator"
    name = protocol.get("protocol_name") or "protocol"
    lines = [f"# {name}", "", f"**{head}**", ""]
    lines += ["## Result", ""]
    lines.append(f"- Steps: {len(protocol.get('steps', []))}")
    lines.append(f"- Simulated on: {files.get('simulated_on', '')}")
    if tiers:
        tried = ", ".join(f"{t['model']} ({max(len(t['rounds']) - 1, 0)} round(s), {t['status']})" for t in tiers)
        lines.append(f"- Repair models tried: {tried}")
    else:
        lines.append("- Repairs: none needed")
    if rounds:
        last = rounds[-1]
        lines.append(f"- Final simulator result: {'passed' if last.get('passed') else 'FAILED: ' + str(last.get('result', ''))}")
    lines += ["", "## Needs human review", ""]
    lines += _table([[i["severity"], i["area"], i["item"], i["detail"]] for i in items],
                    ["Severity", "Area", "Item", "Detail"])
    if (fidelity or {}).get("checked"):
        lines += ["## What the SOP requires", "",
                  f"Each requirement was read from the SOP, and the plan was checked against it: the volumes are the "
                  f"SOP's, for each of {fidelity.get('samples') or 'the'} sample(s).", ""]
        lines += _table([[r["requirement"], r.get("how", ""), _span(r.get("steps", [])),
                          ", ".join(f"{v:g}" for v in r.get("per_sample_ul", [])), "; ".join(r.get("from", [])),
                          " ".join(str(r.get("quote", "")).split())] for r in fidelity.get("requirements", [])],
                        ["Requirement", "How", "Steps", "uL per sample", "From", "SOP"])
    lines += ["## Labware and deck", ""]
    lines += _table([[l["name"], l["type"], l["where"], l.get("holds") or ""] for l in review.get("labware", [])],
                    ["Name", "Type", "Where", "Holds"])
    lines += ["## Reagents", ""]
    lines += _table([[g["labware"], f"{g['loaded_ul']:g}", f"{g['drawn_ul']:g}", f"{g['left_ul']:g}"]
                     for g in review.get("reagents", [])], ["Labware", "Loaded uL", "Drawn uL", "Left uL"])
    lines += ["## Plate wells", ""]
    lines += _table([[w["plate"], w["column"], w["rows"], w["volume_ul"],
                      "; ".join(f"{n} {c['ul']:.3g} uL" for n, c in w["contents"].items()), "; ".join(w["flags"])]
                     for w in review.get("wells", [])],
                    ["Plate", "Column", "Rows", "Volume uL", "Contents", "Flags"])
    lines += ["## Files", ""]
    lines += [f"- {k}: `{v}`" for k, v in files.items() if k not in ("simulated_on",)] + [""]
    return "\n".join(lines)


def failure_markdown(protocol: Dict[str, Any], tiers: List[Dict[str, Any]], max_rounds: int, log: Path) -> str:
    """The summary for a protocol that did not pass: what was tried and where the heal log is. Nothing is written to
    healed/ for it."""
    name = protocol.get("protocol_name") or "protocol"
    lines = [f"# {name}", "", "**NOT READY: did not pass the simulator**", "",
             f"Each model had up to {max_rounds} repair round(s):", ""]
    for tier in tiers:
        used = max(len(tier["rounds"]) - 1, 0)
        lines.append(f"- {tier['model']}: {used} round(s), {tier['status']}")
    last = tiers[-1]["rounds"][-1] if tiers and tiers[-1]["rounds"] else None
    lines += ["", "## Final failure", ""]
    lines.append(f"- Round {last['round']}: {last.get('result', '')}" if last else "- none recorded")
    lines += ["", "## Needs human review", "",
              "- The protocol must change before it can run. Change the request or the protocol text and check again.",
              f"- Heal log: `{log}`", ""]
    return "\n".join(lines)
