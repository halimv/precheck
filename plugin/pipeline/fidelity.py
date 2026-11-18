"""Experimental fidelity: the plan does the experiment the SOP describes, at the SOP's quantities.

The simulator says a plan is physically possible; AHC keeps the hardware honest while it runs. Neither knows what the
scientist's SOP asked for, so a plan could pass both while adding 72 uL where the SOP says 180. This module is the
check that it does not.

Before drafting, a separate Claude call (stage0_drafter.extract_requirements) reads the SOP, and only the SOP, and
lists its requirements: each liquid added to a sample and how much, and each other step with the numbers it must keep
(temperatures, times, speeds, g-forces, amounts of tissue), each with the sentence it comes from, in order. That list is
checked against the SOP text here (`spec_errors`): every quote must be in the SOP, and every number must be in its
quote, so a requirement cannot be invented or misread into a different quantity.

The drafter tags each step with the requirement it carries out ("sop": "R3"), and `check` holds the plan to the list:

- every requirement is carried out (by the robot, as a manual step, or declared done before or after the run in
  "outside_run", which only the first or last requirements may be);
- an addition puts exactly the SOP's volume into every sample well (several dispenses may add up to it), from a source
  holding that reagent; a manual one says the volume in its instruction;
- every other requirement keeps the SOP's numbers (in the manual instruction, or the incubate/shake settings);
- the requirements happen in the SOP's order, and every robot addition reaches the same number of samples;
- no reagent goes into a sample that no requirement asks for.

Nothing scales a volume. A plan that cannot fit the SOP's volumes on the robot uses larger labware, splits an addition
into several dispenses, or hands that addition to the operator as a manual step. Only the scientist may change an SOP
quantity: a "deviations" entry is accepted when its "approved" text is the scientist's own words from a revision request
(pipeline.py --revise), and the report lists it.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

ROWS = "ABCDEFGH"
KINDS = ("addition", "step")
_TO_UL = {"nl": 0.001, "ul": 1.0, "ml": 1000.0, "l": 1_000_000.0}
_QUANTITY = re.compile(r"(\d{1,3}(?:,\d{3})+(?!\d)|\d+(?:[.,]\d+)?)\s*(nl|ul|ml|l)\b")
_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?!\d)|\d+(?:[.,]\d+)?")  # "20,000" is twenty thousand, "0,5" one half
# Words that name no reagent in particular, so "Buffer ATL" is not matched by "Buffer AL".
_GENERIC = {"buffer", "solution", "reagent", "the", "of", "and", "a", "an", "molecular", "biology", "grade", "sterile",
            "stock", "fresh", "kit", "100", "per", "sample", "each", "in", "to", "for", "with", "mix", "mixture"}


def _norm(text: str) -> str:
    """Lowercase, micro signs as u, whitespace collapsed."""
    text = str(text).replace("µ", "u").replace("μ", "u").lower()
    return " ".join(text.split())


def _alnum(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", _norm(text))


def _num(n: str) -> float:
    return float(n.replace(",", "") if re.fullmatch(r"\d{1,3}(?:,\d{3})+", n) else n.replace(",", "."))


def _numbers(text: str) -> List[float]:
    return [_num(n) for n in _NUMBER.findall(_norm(text))]


def _values(v: Any) -> Optional[List[float]]:
    """A value's numbers: {"value": 56} or a range {"min": 12, "max": 15}; None if it is neither."""
    if not isinstance(v, dict):
        return None
    if isinstance(v.get("value"), (int, float)):
        return [float(v["value"])]
    ends = [x for x in (v.get("min"), v.get("max")) if x is not None]  # a range, or one end ("at least 6000 x g")
    return [float(x) for x in ends] if ends and all(isinstance(x, (int, float)) for x in ends) else None


def _shown(v: Dict[str, Any]) -> str:
    nums = _values(v) or []
    bound = ">=" if isinstance(v, dict) and "value" not in v and v.get("max") is None else (
        "<=" if isinstance(v, dict) and "value" not in v and v.get("min") is None else "")
    return (bound + "-".join(f"{x:g}" for x in nums) + f" {v.get('unit', '')}").strip()


def volumes_ul(text: str) -> List[float]:
    """Every liquid volume written in `text`, in uL ("1.2 mL" -> 1200)."""
    return [round(_num(n) * _TO_UL[u], 6) for n, u in _QUANTITY.findall(_norm(text))]


def _has(numbers: List[float], value: float) -> bool:
    return any(abs(n - value) <= 1e-6 * max(1.0, abs(value)) for n in numbers)


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", _norm(text)) if w not in _GENERIC and len(w) > 1}


# --- The requirements, checked against the SOP --------------------------------------------------------------------

def spec_errors(spec: Dict[str, Any], sop_text: Optional[str]) -> List[str]:
    """Problems with an extracted requirements list. With the SOP text, every quote must be in it and every number in
    its quote; without it (a scanned PDF), only the structure is checked."""
    reqs = spec.get("requirements")
    if not isinstance(reqs, list) or not reqs:
        return ["'requirements' must be a non-empty list"]
    errors, seen = [], set()
    source = _alnum(sop_text or "")
    for i, r in enumerate(reqs, start=1):
        if not isinstance(r, dict):
            errors.append(f"requirement {i} is not an object")
            continue
        rid = r.get("id")
        if not isinstance(rid, str) or not rid or rid in seen:
            errors.append(f"requirement {i} needs a unique 'id' (R1, R2, ...)")
        seen.add(rid)
        if r.get("kind") not in KINDS:
            errors.append(f"{rid}: 'kind' must be one of {', '.join(KINDS)}")
        quote = r.get("quote")
        if not isinstance(quote, str) or not quote.strip():
            errors.append(f"{rid}: 'quote' must be the sentence of the SOP it comes from")
            continue
        if sop_text and _alnum(quote) not in source:
            errors.append(f"{rid}: the quote {quote!r} is not in the SOP; quote it word for word")
        said = _numbers(quote)
        vol = r.get("volume_ul")
        if r.get("kind") == "addition" and vol is not None:
            if not isinstance(vol, (int, float)) or vol <= 0:
                errors.append(f"{rid}: 'volume_ul' must be a positive number, or null when the SOP says to move all of it")
            elif not _has(volumes_ul(quote), float(vol)):
                errors.append(f"{rid}: volume_ul {vol:g} is not a volume written in its quote {quote!r} (in uL)")
        for v in r.get("values") or []:
            nums = _values(v)
            if nums is None:
                errors.append(f"{rid}: each of 'values' is {{\"value\": <number>, \"unit\": \"...\"}}, or a range "
                              f"{{\"min\": <number>, \"max\": <number>, \"unit\": \"...\"}}; got {v!r}")
            elif not all(_has(said, x) for x in nums):
                errors.append(f"{rid}: the value {_shown(v)} is not written in its quote {quote!r}")
    return errors[:12]


def describe(r: Dict[str, Any], deviation: Optional[Dict[str, Any]] = None) -> str:
    """One line for a requirement: 'R2 (1.2) add 180 uL of Buffer ATL to each sample'."""
    vol = (deviation or {}).get("volume_ul", r.get("volume_ul"))
    head = f"{r['id']}" + (f" ({r['section']})" if r.get("section") else "")
    if r.get("kind") == "addition":
        amount = f"{vol:g} uL of " if isinstance(vol, (int, float)) else "all of "
        return f"{head} add {amount}{r.get('what', '?')} to each sample"
    values = ", ".join(_shown(v) for v in r.get("values") or [])
    return f"{head} {r.get('what', '?')}" + (f" ({values})" if values else "")


def prompt_lines(reqs: List[Dict[str, Any]]) -> str:
    return "\n".join(f"- {describe(r)}. SOP: \"{' '.join(str(r.get('quote', '')).split())}\"" for r in reqs)


# --- The plan, checked against the requirements ------------------------------------------------------------------

def _tags(step: Dict[str, Any]) -> List[str]:
    tag = step.get("sop")
    if isinstance(tag, str):
        return [tag]
    return [t for t in tag if isinstance(t, str)] if isinstance(tag, list) else []


def _approved_deviations(protocol: Dict[str, Any], ids: set, errors: List[str],
                         extra_notes: Tuple[str, ...] = ()) -> Dict[str, Dict[str, Any]]:
    """The plan's deviations that the scientist asked for; any other one is an error."""
    notes = [_alnum(r.get("note", "")) for r in protocol.get("revisions") or []] + [_alnum(n) for n in extra_notes]
    out = {}
    for d in protocol.get("deviations") or []:
        rid = d.get("sop") if isinstance(d, dict) else None
        if rid not in ids:
            errors.append(f"a deviation names {rid!r}, which is not a requirement")
            continue
        approved = _alnum(d.get("approved", ""))
        if not approved or not any(approved in n for n in notes):
            errors.append(f"{rid} deviates from the SOP without the scientist's request: only the scientist may change "
                          "an SOP quantity (a revision request), and 'approved' quotes their words")
            continue
        out[rid] = d
    return out


def _realization(protocol: Dict[str, Any], kinds: Dict[str, str]) -> Tuple[Dict[str, List[int]], Dict, List[str]]:
    """Which steps carry out each requirement, how much each tagged dispense puts in each well (with the source it
    came from), and the untagged additions of a reagent to a well."""
    steps = protocol.get("steps", [])
    by_req: Dict[str, List[int]] = {}
    added: Dict[str, Dict[Any, float]] = {}
    sources: Dict[str, set] = {}
    untagged: List[str] = []
    source: Dict[int, Optional[str]] = {}  # channel -> the labware it last aspirated from
    for i, s in enumerate(steps):
        for t in _tags(s):
            by_req.setdefault(t, []).append(i)
        action, lid = s.get("action"), s.get("labware")
        chans = s.get("channels", [0])
        if action == "tips_off":
            for ch in chans:
                source.pop(ch, None)
        elif action == "aspirate":
            for ch in chans:
                source[ch] = lid
        elif action == "dispense" and kinds.get(lid) != "trash":
            from_reagent = [ch for ch in chans if kinds.get(source.get(ch)) == "container"]
            if not _tags(s) and from_reagent and kinds.get(lid) in ("plate", "container"):
                untagged.append(f"step {s.get('step', i + 1)} dispenses {source[from_reagent[0]]} into {lid}")
            for t in _tags(s):
                for ch in chans:
                    well = (lid, s.get("column"), ch) if kinds.get(lid) == "plate" else (lid,)
                    added.setdefault(t, {})[well] = added.get(t, {}).get(well, 0.0) + float(s.get("volume_ul") or 0)
                    if source.get(ch):
                        sources.setdefault(t, set()).add(source[ch])
    return by_req, {"added": added, "sources": sources}, untagged


def _well_name(well: Tuple) -> str:
    if len(well) == 1:
        return well[0]
    lid, col, ch = well
    return f"{lid}:{ROWS[ch] if isinstance(ch, int) and ch < 8 else ch}{col}"


def check(protocol: Dict[str, Any], kinds: Dict[str, str], extra_notes: Tuple[str, ...] = ()) -> Dict[str, Any]:
    """Hold the plan to its requirements. Returns {"errors": [...], "requirements": [one row per requirement: how it is
    carried out], "samples": n, "checked": bool}. A plan with no requirements (not drafted from an SOP) is not checked.
    `kinds` maps labware to its deck kind (plate, container, tip_rack, trash). `extra_notes` are revision requests
    not yet in the plan's "revisions"."""
    reqs = protocol.get("requirements") or []
    if not reqs:
        return {"checked": False, "errors": [], "requirements": [], "samples": None}
    steps = protocol.get("steps", [])
    ids = {r["id"] for r in reqs}
    errors: List[str] = []
    deviations = _approved_deviations(protocol, ids, errors, extra_notes)
    by_req, liquid, untagged = _realization(protocol, kinds)
    names = protocol.get("reagents") or {}
    outside = [o for o in protocol.get("outside_run") or [] if isinstance(o, str)]

    for t in by_req:
        if t not in ids:
            errors.append(f"steps are tagged {t!r}, which is not a requirement")
    for o in outside:
        if o not in ids:
            errors.append(f"outside_run names {o!r}, which is not a requirement")
        elif o in by_req:
            errors.append(f"{o} is in outside_run but steps carry it out")
    order = [r["id"] for r in reqs]
    out_pos = sorted(order.index(o) for o in outside if o in order)
    n = len(order)
    head = [p for p in out_pos if p < n / 2]
    tail = [p for p in out_pos if p >= n / 2]
    if head != list(range(len(head))) or tail != list(range(n - len(tail), n)):
        errors.append("only the first or last requirements may be done outside the run (outside_run); one in the "
                      "middle must be in the plan, as a manual step if the robot cannot do it")

    rows, counts, last_first = [], {}, None
    for r in reqs:
        rid = r["id"]
        dev = deviations.get(rid)
        idx = by_req.get(rid, [])
        row = {"id": rid, "section": r.get("section"), "kind": r.get("kind"), "requirement": describe(r),
               "quote": r.get("quote"), "steps": [steps[i].get("step", i + 1) for i in idx]}
        if dev:
            row["deviation"] = {k: v for k, v in dev.items() if k != "sop"}
        if dev and dev.get("omit"):
            row["how"] = "left out (the scientist's request)"
            rows.append(row)
            continue
        if rid in outside:
            row["how"] = "before or after the run, by hand"
            rows.append(row)
            continue
        if not idx:
            errors.append(f"{describe(r)} is not carried out: tag the steps that do it with \"sop\": \"{rid}\" (a manual "
                          "step if the robot cannot)")
            rows.append({**row, "how": "missing"})
            continue
        tagged = [steps[i] for i in idx]
        manual = [s for s in tagged if s.get("action") == "manual"]
        devices = [s for s in tagged if s.get("action") in ("incubate", "shake")]
        robot = [s for s in tagged if s.get("action") not in ("manual", "incubate", "shake")]
        row["how"] = "by hand" if not robot and not devices else ("on the robot" + (" and by hand" if manual else ""))
        said = " ".join(str(s.get("instruction", "")) for s in manual)
        numbers = _numbers(said)
        for s in devices:
            if s.get("temperature_c") is not None:
                numbers.append(float(s["temperature_c"]))
            if s.get("speed_rpm") is not None:
                numbers.append(float(s["speed_rpm"]))
            if s.get("duration_s") is not None:
                numbers += [float(s["duration_s"]), float(s["duration_s"]) / 60, float(s["duration_s"]) / 3600]
        want = (dev or {}).get("values", r.get("values")) or []
        for v in want:
            if not all(_has(numbers, x) for x in _values(v) or []):
                errors.append(f"{describe(r)}: the plan does not keep {_shown(v)}"
                              + " (write it in the manual instruction as the SOP does, or set it on the incubate/shake step)")
        if r.get("kind") == "addition":
            vol = (dev or {}).get("volume_ul", r.get("volume_ul"))
            wells = liquid["added"].get(rid, {})
            if robot and not wells:
                errors.append(f"{describe(r)}: steps tagged {rid} dispense nothing into a sample")
            if isinstance(vol, (int, float)) and wells:
                wrong = {w: v for w, v in wells.items() if abs(v - vol) > max(0.05, 0.005 * vol)}
                if wrong:
                    shown = ", ".join(f"{_well_name(w)} gets {v:g}" for w, v in list(wrong.items())[:3])
                    errors.append(f"{describe(r)}: {shown} uL. Use the SOP's volume, not a scaled one: a deep-well plate "
                                  "or tube that holds it, several dispenses that add up to it, or a manual step")
                row["per_sample_ul"] = sorted({round(v, 3) for v in wells.values()})
            if wells:
                counts[rid] = len(wells)
                row["samples"] = len(wells)
                srcs = sorted(liquid["sources"].get(rid, set()))
                row["from"] = [f"{s} ({names.get(s, s)})" for s in srcs]
                want_words = _words(r.get("what", ""))
                for s in srcs:
                    if kinds.get(s) == "container" and want_words and not (want_words & _words(f"{s} {names.get(s, '')}")):
                        errors.append(f"{describe(r)} is dispensed from {s} ({names.get(s, 'no reagent named')}), which "
                                      f"does not hold {r.get('what')}: name the reagent it holds in 'reagents'")
            if manual and isinstance(vol, (int, float)) and not _has(volumes_ul(said), float(vol)):
                errors.append(f"{describe(r)}: the manual instruction does not say {vol:g} uL (write the SOP's volume)")
        first = min(idx)
        if last_first is not None and first < last_first[0]:
            errors.append(f"{rid} comes before {last_first[1]} in the plan (step {steps[first].get('step', first + 1)}), "
                          "but after it in the SOP: keep the SOP's order")
        last_first = (first, rid) if last_first is None or first >= last_first[0] else last_first
        rows.append(row)

    if len(set(counts.values())) > 1:
        shown = ", ".join(f"{k}: {v}" for k, v in counts.items())
        errors.append(f"the robot's additions reach different numbers of samples ({shown}); every sample gets every one")
    for u in untagged:
        errors.append(f"{u}, but no SOP requirement says so: tag it with the requirement it carries out")
    return {"checked": True, "errors": errors[:15], "requirements": rows,
            "samples": next(iter(counts.values()), None) if counts else None}


def feedback(errors: List[str]) -> str:
    return "The plan does not do what the SOP says:\n" + "\n".join(f"- {e}" for e in errors)
