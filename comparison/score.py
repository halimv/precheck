"""Score a plan against an SOP's answer key, the same way for PreCheck and for an agent driving AHC.

Both sides are reduced to the same thing first: the liquid moves, channel by channel, as AHC's run log records them
(`effective.containers` and `effective.volumes_ul`):

- PreCheck: its healed IR, each step expanded to the wells of its column for the channels it uses (`ir_ops`).
- AHC: the run log the agent's session wrote (`ahc_ops`).

Each tip remembers where its liquid came from, so a dispense is attributed to the reagent it carries. A container is
a reagent when its name or its label (PreCheck's `reagents`, the agent's layout liquids) matches one of the key's
reagents. The keys (`KEYS`) are written from the SOP texts by hand, independently of PreCheck's own requirement
reader, so neither side is scored by its own reading.

    python score.py <trial.json>   # prints the score of one trial
"""

import json
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

ROWS = "ABCDEFGH"
Op = Dict[str, Any]  # {"op": "aspirate"|"dispense"|"pick_up_tips"|"drop_tips", "containers": [...], "volumes": [...]}


# --- the answer keys, from the SOP texts ---

KEYS: Dict[str, Dict[str, Any]] = {
    "dna_extraction": {
        "sop": "nPOD OPPC-SOP-79.1, section 1.0 (DNA extraction from tissue, Qiagen DNeasy)",
        "kind": "additions",
        # in the SOP's order; "into": the sample tubes, or the spin column the lysate went to (step 1.7)
        "items": [
            {"id": "ATL", "match": ["atl"], "ul": 180, "into": "sample", "sop": "1.2 Add 180 µl Buffer ATL."},
            {"id": "proteinase K", "match": ["proteinase", "protk", "pk"], "ul": 20, "into": "sample",
             "sop": "1.3 Add 20 µl proteinase K"},
            {"id": "AL", "match": ["al"], "ul": 200, "into": "sample", "sop": "1.5 ... add 200 µl Buffer AL"},
            {"id": "ethanol", "match": ["ethanol", "etoh"], "ul": 200, "into": "sample",
             "sop": "1.6 Add 200 µl 100% ethanol"},
            {"id": "lysate to column", "transfer": True, "ul": 600, "tolerance": 0.05, "into": "column",
             "sop": "1.7 Pipette the mixture into a DNeasy Mini spin column"},
            {"id": "AW1", "match": ["aw1"], "ul": 500, "into": "column", "sop": "1.9 add 500 µl Buffer AW1"},
            {"id": "AW2", "match": ["aw2"], "ul": 500, "into": "column", "sop": "1.11 add 500 µl Buffer AW2"},
            {"id": "TE", "match": ["te", "tris", "edta", "elution"], "ul": 100, "into": "column",
             "sop": "1.13 add 100 µl 1x Tris-EDTA buffer"},
        ],
        # buffers whose labels mention another reagent ("AW1, ethanol added") are matched first
        "priority": ["AW1", "AW2", "ATL", "proteinase K", "AL", "TE", "ethanol"],
    },
    "serial_dilution": {
        "sop": "PreCheck files/input.txt (1:10 serial dilution of a culture in 0.9% saline)",
        "kind": "series",
        "diluent": ["saline", "diluent", "nacl", "solvent", "pbs", "water"],
        "sample": ["culture", "sample", "bacteria", "stock"],
        # "a ratio of 1:10 dilution i.e. (1ml of the culture diluted in 10ml of the solvent)": either reading
        "factors": [10.0, 11.0],
        "tolerance": 0.03,
        "min_steps": 2,
    },
}
TOLERANCE = 0.02  # an addition matches when it is within 2% of the SOP's volume


# --- both sides as liquid moves ---

def ir_ops(protocol: Dict[str, Any], kinds: Dict[str, str]) -> List[Op]:
    """PreCheck's IR as AHC would record it: a plate step names the wells of its column for its channels."""
    ops: List[Op] = []
    for s in protocol.get("steps", []):
        action, lw, ch = s.get("action"), s.get("labware"), s.get("channels") or [0]
        if action == "tips_on":
            ops.append({"op": "pick_up_tips", "containers": [f"tip{c}" for c in ch], "channels": ch})
        elif action == "tips_off":
            ops.append({"op": "drop_tips"})
        elif action in ("aspirate", "dispense"):
            if kinds.get(lw) == "plate":
                containers = [f"{lw}_well_{ROWS[c]}{s['column']}" for c in ch]
            else:
                containers = [lw] * len(ch)
            ops.append({"op": action, "containers": containers, "volumes": [float(s["volume_ul"])] * len(ch),
                        "channels": ch})
        elif action in ("manual", "empty"):
            ops.append({"op": "manual", "empties": s.get("empties") or []})
    return ops


def ahc_ops(log_rows: List[Dict[str, Any]]) -> List[Op]:
    """An AHC run log's liquid moves: only the calls AHC carried out (status ok)."""
    ops: List[Op] = []
    for r in log_rows:
        op, eff = r.get("op"), r.get("effective") or {}
        if r.get("status") != "ok" or op not in ("aspirate", "dispense", "pick_up_tips", "drop_tips"):
            continue
        if op in ("aspirate", "dispense"):
            ops.append({"op": op, "containers": eff.get("containers", []), "volumes": eff.get("volumes_ul", []),
                        "channels": list(range(len(eff.get("containers", []))))})
        else:
            ops.append({"op": op, "channels": list(range(len(eff.get("tips", []) or [])))})
    return ops


def _wells_of(target: str) -> List[str]:
    """An AHC target ("plate:col2", "plate:rowB", "plate:A1", "plate:A1:H1", "trough") as AHC's container names."""
    lw, _, spec = target.partition(":")
    if not spec:
        return [lw]
    if m := re.fullmatch(r"col(\d+)", spec, re.I):
        return [f"{lw}_well_{r}{m.group(1)}" for r in ROWS]
    if m := re.fullmatch(r"row([A-H])", spec, re.I):
        return [f"{lw}_well_{m.group(1).upper()}{c}" for c in range(1, 13)]
    if m := re.fullmatch(r"([A-H])(\d+):([A-H])(\d+)", spec, re.I):
        r0, r1 = sorted((ROWS.index(m.group(1).upper()), ROWS.index(m.group(3).upper())))
        c0, c1 = sorted((int(m.group(2)), int(m.group(4))))
        return [f"{lw}_well_{ROWS[r]}{c}" for c in range(c0, c1 + 1) for r in range(r0, r1 + 1)]
    return [f"{lw}_well_{spec.upper()}"]


def ahc_labels(log_rows: List[Dict[str, Any]]) -> Dict[str, str]:
    """The names an agent gave its liquids in AHC's layout: `aliases` ({"protk": "reagents:col2"}) label every
    container they cover."""
    labels: Dict[str, str] = {}
    for r in log_rows:
        if r.get("op") == "load_layout" and r.get("status") == "ok":
            for alias, target in ((r.get("effective") or {}).get("aliases") or {}).items():
                for t in target if isinstance(target, list) else [target]:
                    for c in _wells_of(str(t)):
                        labels[c] = f"{labels.get(c, '')} {alias}".strip()
    return labels


def _base(container: str) -> str:
    return container.split("_well_")[0]


def _tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def classify(container: str, labels: Dict[str, str], names: List[Tuple[str, List[str]]]) -> Optional[str]:
    """Which key reagent a container holds, from its labware name and its label, by whole tokens."""
    text = f"{_base(container)} {labels.get(_base(container), '')} {labels.get(container, '') if container != _base(container) else ''}"
    tokens = _tokens(text)
    joined = " ".join(tokens)
    for name, words in names:
        if any(w in tokens or (len(w) > 3 and w in joined) for w in words):
            return name
    return None


def moves(ops: List[Op]) -> List[Dict[str, Any]]:
    """Every dispense as (source container, destination container, uL), in order. A tip carries the source of the
    liquid in it; a tip that emptied takes the source of what it draws next, and one that holds liquid from two
    places is "mixed"."""
    tip: Dict[int, Optional[str]] = {}
    held: Dict[int, float] = defaultdict(float)
    filled: set = set()  # containers liquid was dispensed into so far: what they hold was made in the run
    made: Dict[int, bool] = {}
    out = []
    for i, o in enumerate(ops):
        if o["op"] in ("pick_up_tips", "drop_tips"):
            tip, held = {}, defaultdict(float)
        elif o["op"] == "aspirate":
            for k, c in enumerate(o["containers"]):
                ch = o["channels"][k] if k < len(o["channels"]) else k
                empty = held[ch] <= 1e-6
                tip[ch] = c if empty or tip.get(ch) in (None, c) else "mixed"
                made[ch] = c in filled
                held[ch] += float(o["volumes"][k])
        elif o["op"] == "dispense":
            for k, c in enumerate(o["containers"]):
                ch = o["channels"][k] if k < len(o["channels"]) else k
                out.append({"i": i, "source": tip.get(ch), "dest": c, "ul": float(o["volumes"][k]),
                            "made": made.get(ch, False)})
                held[ch] = max(0.0, held[ch] - float(o["volumes"][k]))
                filled.add(c)
    return out


# --- scoring ---

def _within(got: float, want: float, tol: float) -> bool:
    return abs(got - want) <= tol * want


def score_additions(key: Dict[str, Any], ops: List[Op], labels: Dict[str, str]) -> Dict[str, Any]:
    items = {it["id"]: it for it in key["items"]}
    names = [(n, items[n]["match"]) for n in key["priority"]]
    mv = moves(ops)
    kind_of = {}
    for m in mv:
        if m["source"] and m["source"] != "mixed" and not m["made"] and m["source"] not in kind_of:
            kind_of[m["source"]] = classify(m["source"], labels, names)
    # the samples: where the first key reagent went; the columns: where liquid drawn from a sample went
    first = key["items"][0]["id"]
    samples = sorted({m["dest"] for m in mv if kind_of.get(m["source"]) == first})
    columns = sorted({m["dest"] for m in mv if m["source"] in samples and m["dest"] not in samples})
    got: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    first_seen: Dict[str, int] = {}
    for m in mv:
        what = "lysate to column" if m["source"] in samples and m["dest"] in columns else kind_of.get(m["source"])
        if what:
            got[what][m["dest"]] += m["ul"]
            first_seen.setdefault(what, m["i"])
    rows = []
    for it in key["items"]:
        wells = samples if it["into"] == "sample" else columns
        per = [got[it["id"]].get(w, 0.0) for w in wells]
        ok = bool(wells) and all(_within(v, it["ul"], it.get("tolerance", TOLERANCE)) for v in per)
        stray = sorted(set(got[it["id"]]) - set(wells))
        rows.append({"item": it["id"], "sop_ul": it["ul"], "ok": ok, "per_well_ul": sorted(set(round(v, 2) for v in per)),
                     "wells": len(wells), "elsewhere": stray[:4], "sop": it["sop"]})
    done = [r["item"] for r in rows if r["ok"]]
    order = [it["id"] for it in key["items"] if it["id"] in first_seen]
    in_order = order == sorted(order, key=lambda n: first_seen[n])
    return {"kind": "additions", "items": rows, "correct": len(done), "of": len(rows),
            "fidelity": round(len(done) / len(rows), 3), "in_sop_order": in_order, "samples": len(samples),
            "columns": len(columns)}


def score_series(key: Dict[str, Any], ops: List[Op], labels: Dict[str, str]) -> Dict[str, Any]:
    names = [("diluent", key["diluent"]), ("sample", key["sample"])]
    mv = moves(ops)
    kind = {m["source"]: classify(m["source"], labels, names) for m in mv
            if m["source"] and m["source"] != "mixed" and not m["made"]}
    diluent: Dict[str, float] = defaultdict(float)
    incoming: Dict[str, float] = defaultdict(float)
    came_from: Dict[str, str] = {}
    for m in mv:
        if kind.get(m["source"]) == "diluent":
            diluent[m["dest"]] += m["ul"]
        elif m["source"] and m["source"] != m["dest"]:
            incoming[m["dest"]] += m["ul"]
            came_from.setdefault(m["dest"], m["source"])
    wells = [w for w in diluent if incoming.get(w)]
    factors = {w: round((diluent[w] + incoming[w]) / incoming[w], 3) for w in wells}
    ok = [w for w, f in factors.items() if any(_within(f, want, key["tolerance"]) for want in key["factors"])]

    def depth(w: str, seen: frozenset = frozenset()) -> int:  # dilution steps from the sample to this well
        src = came_from.get(w)
        return 1 + (depth(src, seen | {w}) if src in factors and src not in seen else 0)

    steps = max((depth(w) for w in wells), default=0)
    return {"kind": "series", "wells": len(wells), "correct": len(ok), "of": len(wells),
            "fidelity": round(len(ok) / len(wells), 3) if wells else 0.0, "steps": steps,
            "enough_steps": steps >= key["min_steps"], "factors": sorted(set(factors.values()))[:6]}


def score(sop: str, ops: List[Op], labels: Dict[str, str]) -> Dict[str, Any]:
    key = KEYS[sop]
    return score_additions(key, ops, labels) if key["kind"] == "additions" else score_series(key, ops, labels)


def signature(result: Dict[str, Any]) -> str:
    """What two plans must share to count as the same experiment: the key items each got right or wrong, with the
    volumes they put in, in order (additions); or the dilution factors and number of steps (series)."""
    if result["kind"] == "additions":
        return json.dumps([(r["item"], r["per_well_ul"], r["wells"]) for r in result["items"]] + [result["in_sop_order"]])
    return json.dumps([result["factors"], result["steps"], result["wells"]])


if __name__ == "__main__":
    trial = json.loads(open(sys.argv[1]).read())
    print(json.dumps(trial.get("score"), indent=2))
