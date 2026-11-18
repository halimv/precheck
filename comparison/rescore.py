"""Recompute every trial's score from what it left on disk (the agent's AHC run logs, PreCheck's healed IR), so a fix
to score.py applies to trials already run. The rest of each trial record is kept."""
import json
from pathlib import Path

import score

HERE = Path(__file__).resolve().parent

for path in sorted((HERE / "results" / "trials").glob("*.json")):
    t = json.loads(path.read_text())
    folder = Path(t["folder"])
    if t["arm"] == "agent+AHC":
        rows = [json.loads(l) for f in sorted((folder / ".ahc" / "runs").glob("*.jsonl")) for l in f.read_text().splitlines() if l.strip()]
        t["score"] = score.score(t["sop"], score.ahc_ops(rows), score.ahc_labels(rows))
    elif t.get("ir"):
        protocol = json.loads(Path(t["ir"]).read_text())
        deck = json.loads((folder / protocol["deck_config"]).read_text())
        t["score"] = score.score(t["sop"], score.ir_ops(protocol, {k: v["kind"] for k, v in deck["labware"].items()}),
                                 protocol.get("reagents", {}))
    path.write_text(json.dumps(t, indent=2, default=str))
    s = t["score"]
    print(f"{path.stem:40} {s['correct']}/{s['of']}  " + (f"order={s.get('in_sop_order')}" if s["kind"] == "additions" else f"steps={s.get('steps')} factors={s.get('factors')}"))
