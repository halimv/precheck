"""One trial of the PreCheck arm: PreCheck turns an SOP into a checked, repaired protocol.

The same SOP text the agent gets goes to PreCheck's CLI, unchanged, in a fresh working folder per trial:

    pipeline.py <sop.txt> --target lab --yes --no-visualize

`lab` builds the deck from the lab's labware, the path that hands off to AHC. The healed IR, if any, is scored with
`score.py` exactly as the agent's AHC run log is.

    python run_precheck.py dna_extraction 1 --out results [--target plr]
"""

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict

import score

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / "plugin"
SOPS = {"dna_extraction": HERE / "sops" / "dna_extraction.txt", "serial_dilution": HERE / "sops" / "serial_dilution.txt"}


def trial(sop: str, k: int, out: Path, target: str) -> Dict[str, Any]:
    folder = (out / f"precheck_{target}" / sop / f"t{k}").resolve()
    folder.mkdir(parents=True, exist_ok=True)
    started = time.time()
    proc = subprocess.run(["uv", "run", "--quiet", "python", "pipeline.py", str(SOPS[sop]), "--target", target, "--yes",
                           "--no-visualize"], cwd=PLUGIN, env={**os.environ, "PRECHECK_WORKDIR": str(folder)},
                          capture_output=True, text=True)
    wall = round(time.time() - started, 1)
    log = proc.stdout + "\n" + proc.stderr
    (folder / "precheck.log").write_text(log)
    healed = sorted((p for p in (folder / "healed").glob("*.json") if not p.stem.endswith(("_report", "_heal_log"))),
                    key=lambda p: p.stat().st_mtime)
    record: Dict[str, Any] = {
        "arm": f"PreCheck ({target})", "sop": sop, "trial": k, "folder": str(folder), "wall_s": wall,
        "exit_code": proc.returncode, "passed": bool(healed),
        "draft_attempts": int(m.group(1)) if (m := re.search(r"(\d+) attempt\(s\)", log)) else None,
        "draft_cost_usd": float(m.group(1)) if (m := re.search(r"attempt\(s\), \$([0-9.]+)", log)) else None,
        "draft_retries": {"not_usable": len(re.findall(r"\[draft\] attempt", log)),
                          "changed_the_sop": len(re.findall(r"\[fidelity\] attempt", log)),
                          "no_labware": len(re.findall(r"\[deck\] attempt", log))},
        "result_line": next((l.strip() for l in log.splitlines() if l.startswith(("PASSED", "NOT READY"))), None),
    }
    if not healed:
        record["score"] = {**score.score(sop, [], {}), "note": "no protocol passed, so nothing was written"}
        record["tail"] = log[-2500:]
        return record
    ir_path = healed[-1]
    protocol = json.loads(ir_path.read_text())
    report = json.loads(ir_path.with_name(f"{ir_path.stem}_report.json").read_text())
    deck = json.loads((folder / protocol["deck_config"]).read_text())
    kinds = {lid: spec["kind"] for lid, spec in deck["labware"].items()}
    record.update({
        "ir": str(ir_path), "steps": len(protocol["steps"]),
        "manual_steps": sum(1 for s in protocol["steps"] if s.get("action") == "manual"),
        "repair_rounds": report.get("repair_rounds"), "status": report.get("status"),
        "requirements_held": len((report.get("fidelity") or {}).get("requirements", [])),
        "ahc_not_on_layout": len((report.get("ahc") or {}).get("not_on_layout", [])),
        "labware": sorted({spec.get("venus_type") or spec.get("factory") or "" for lid, spec in deck["labware"].items()
                           if lid in {s.get("labware") for s in protocol["steps"]}} - {""}),
        "score": score.score(sop, score.ir_ops(protocol, kinds), protocol.get("reagents", {})),
    })
    return record


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sop", choices=sorted(SOPS))
    ap.add_argument("trial", type=int)
    ap.add_argument("--out", default=str(HERE / "results"))
    ap.add_argument("--target", choices=["lab", "plr"], default="lab")
    a = ap.parse_args()
    out = Path(a.out)
    record = trial(a.sop, a.trial, out, a.target)
    path = out / "trials" / f"precheck_{a.target}_{a.sop}_t{a.trial}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str))
    s = record["score"]
    print(f"PreCheck {a.target} {a.sop} t{a.trial}: passed={record['passed']} {s['correct']}/{s['of']} correct, "
          f"{record['wall_s']} s")


if __name__ == "__main__":
    main()
