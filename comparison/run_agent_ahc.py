"""One trial of the agent-plus-AHC arm: a Claude agent with AHC's tools runs an SOP on AHC's simulated STARlet.

This is AHC used the way its plugin is meant to be used:
- the agent is given AHC's own `lab-hardware` skill (SKILL.md and patterns.md) as its instructions;
- its only tools are AHC's;
- the model is the Claude Code default, as PreCheck's drafter uses.

AHC's server runs forced to simulation (`--backend sim`), in a fresh task folder per trial.

The person's part is played by this harness, and only in simulation:
- AHC asks a person to confirm a new layout's deck (`record_verdict`). The harness allows that call and replaces its
  note with "Automated simulation benchmark: no person", so the run log never claims a person approved.
- The dashboard is not opened.

Nothing else is changed or retried. Refusals are AHC's, and the agent replans as it would with a scientist.

Run it with a Python that has `ahc`, `mcp` and `claude_agent_sdk` (ARGUS's venv does):

    python run_agent_ahc.py dna_extraction 1 --out results --ahc-mcp <path to ahc-mcp> --skill <ahc>/skills/lab-hardware
"""

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any, Dict, List

from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, PermissionResultAllow,
                              PermissionResultDeny, ResultMessage, TextBlock, ToolResultBlock, ToolUseBlock,
                              UserMessage)

import score

HERE = Path(__file__).resolve().parent
SOPS = {"dna_extraction": HERE / "sops" / "dna_extraction.txt", "serial_dilution": HERE / "sops" / "serial_dilution.txt"}
AHC_TOOLS = ["agent_verdict", "aspirate", "capture", "configure_devices", "confirm_config", "describe_device", "disconnect",
             "dispense", "drop_tips", "find_layout_references", "find_robots", "get_params", "get_run", "get_state",
             "invoke", "lab_overview", "list_checks", "load_layout", "map_camera", "mix", "open_dashboard",
             "physical_world_context", "pick_up_tips", "propose_verdict", "record_verdict", "recover_tips",
             "report_decision", "request_plate_calibration", "verify"]
HARNESS_NOTE = ("Automated simulation benchmark: no person. The comparison harness confirms simulated deck checks so "
                "the run can go on; nothing here is a person's verdict.")
TASK = """Here is a laboratory SOP. Carry it out on the simulated Hamilton STARlet with the AHC tools, as far as the
robot can: plan it, lay out the deck, run the liquid handling, and check the result. Steps the robot cannot do (for
example vortexing, incubating, centrifuging) are done by a person: say where they come in your plan and in your
reports. This is a simulation only. There is no real robot, and the deck checks that need a person are confirmed by
the benchmark harness.

<sop>
{sop}
</sop>"""


def _labels(layout: Any) -> Dict[str, str]:
    """For each labware in the agent's layout, the text it gave about it (type, liquid names), for `score.classify`."""
    out: Dict[str, str] = {}

    def walk(node: Any, key: str = "") -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    walk(v, k)
                elif isinstance(v, str):
                    out[key] = f"{out.get(key, '')} {k} {v}".strip()
        elif isinstance(node, list):
            for v in node:
                walk(v, key)
    walk(layout)
    return out


async def trial(sop: str, k: int, out: Path, ahc_mcp: str, skill: Path, max_turns: int) -> Dict[str, Any]:
    folder = (out / "agent_ahc" / sop / f"t{k}").resolve()
    folder.mkdir(parents=True, exist_ok=True)
    instructions = "\n\n".join(p.read_text() for p in (skill / "SKILL.md", skill / "patterns.md") if p.exists())
    approvals: List[Dict[str, Any]] = []

    async def can_use_tool(name: str, args: Dict[str, Any], _ctx: Any):
        tool = name.rsplit("__", 1)[-1]
        if tool == "open_dashboard":
            return PermissionResultDeny(message="No dashboard in this benchmark: carry on without it.")
        if tool in ("record_verdict", "confirm_config"):
            approvals.append({"tool": tool, "args": {k: v for k, v in args.items() if k != "note"}})
            if tool == "record_verdict":
                return PermissionResultAllow(updated_input={**args, "note": HARNESS_NOTE})
        return PermissionResultAllow(updated_input=args)

    options = ClaudeAgentOptions(
        system_prompt=instructions,
        mcp_servers={"ahc": {"type": "stdio", "command": ahc_mcp,
                             "args": ["--backend", "sim", "--device", "hamilton.starlet", "--workspace", str(folder)]}},
        strict_mcp_config=True, tools=[], allowed_tools=[], can_use_tool=can_use_tool,
        setting_sources=[], cwd=str(folder), max_turns=max_turns,
        env={"MCP_TOOL_TIMEOUT": str(10 * 60 * 1000)},
    )
    calls: List[Dict[str, Any]] = []
    texts: List[str] = []
    result: Dict[str, Any] = {}
    started = time.time()
    async with ClaudeSDKClient(options=options) as client:
        await client.query(TASK.format(sop=SOPS[sop].read_text()))
        pending: Dict[str, Dict[str, Any]] = {}
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, ToolUseBlock):
                        entry = {"tool": b.name.rsplit("__", 1)[-1], "input": b.input}
                        pending[b.id] = entry
                        calls.append(entry)
                    elif isinstance(b, TextBlock):
                        texts.append(b.text)
            elif isinstance(msg, UserMessage) and isinstance(msg.content, list):
                for b in msg.content:
                    if isinstance(b, ToolResultBlock) and b.tool_use_id in pending:
                        pending[b.tool_use_id]["error"] = bool(b.is_error)
                        text = b.content if isinstance(b.content, str) else json.dumps(b.content)[:2000]
                        pending[b.tool_use_id]["result"] = text[:1500]
            elif isinstance(msg, ResultMessage):
                result = {"cost_usd": msg.total_cost_usd, "duration_s": round((msg.duration_ms or 0) / 1000, 1),
                          "turns": msg.num_turns, "is_error": msg.is_error, "subtype": msg.subtype}
    rows = []
    for log in sorted((folder / ".ahc" / "runs").glob("*.jsonl")):
        rows += [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
    layouts = [c["input"].get("layout") for c in calls if c["tool"] in ("load_layout", "report_decision") and c["input"].get("layout")]
    labels: Dict[str, str] = {}
    for layout in layouts:
        labels.update(_labels(layout))
    labels.update(score.ahc_labels(rows))  # the names the agent gave its liquids (layout aliases)
    ops = score.ahc_ops(rows)
    refused = [c for c in calls if c.get("error")]
    finished = any(c["tool"] == "report_decision" and c["input"].get("plan_done") and not c.get("error") for c in calls)
    return {
        "arm": "agent+AHC", "sop": sop, "trial": k, "folder": str(folder),
        "wall_s": round(time.time() - started, 1), **result,
        "tool_calls": len(calls), "refused_calls": len(refused),
        "refusals": [{"tool": c["tool"], "result": c.get("result", "")[:300]} for c in refused][:20],
        "liquid_calls_ok": sum(1 for o in ops if o["op"] in ("aspirate", "dispense")),
        "finished": finished, "harness_approvals": approvals,
        "labware": sorted({t for r in rows if r.get("op") == "load_layout" and r.get("status") == "ok"
                           for t in ((r.get("effective") or {}).get("labware") or {}).values()}),
        "score": score.score(sop, ops, labels),
        "last_text": (texts[-1] if texts else "")[:3000],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sop", choices=sorted(SOPS))
    ap.add_argument("trial", type=int)
    ap.add_argument("--out", default=str(HERE / "results"))
    ap.add_argument("--ahc-mcp", required=True)
    ap.add_argument("--skill", required=True, type=Path)
    ap.add_argument("--max-turns", type=int, default=250)
    a = ap.parse_args()
    out = Path(a.out)
    record = asyncio.run(trial(a.sop, a.trial, out, a.ahc_mcp, a.skill, a.max_turns))
    path = out / "trials" / f"agent_ahc_{a.sop}_t{a.trial}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str))
    s = record["score"]
    print(f"agent+AHC {a.sop} t{a.trial}: {s['correct']}/{s['of']} correct, finished={record['finished']}, "
          f"refused={record['refused_calls']}, {record.get('duration_s')} s, ${record.get('cost_usd')}")


if __name__ == "__main__":
    main()
