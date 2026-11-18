"""Stage 0: Drafter (protocol text or PDF -> protocol IR, by the Claude CLI).

The scientist's written protocol (a PDF, a text file, or a pasted paragraph) goes to Claude
through the `claude` command-line tool in print mode, with the IR rules and what labware there is.
Claude's reply streams to the terminal as it is written.

Claude does not pick deck positions. It names the labware the protocol needs by role in the IR's
`labware` section (kind and size: "culture": a tube of at least 5 mL), and the steps use those names.
Each reply goes through two checks, and whatever fails goes back to Claude in the same CLI session:

1. structure: the labware section, known actions, fields every step needs;
2. the deck (pipeline/deck_builder.py): real labware for every need, from what is on the STARlet
   now and VENUS's labware library. A need nothing fits comes back with the closest options.

Whether the plan is physically sound is decided by the simulator (stages 2-3), and the local model in
the self-healing loop repairs what it rejects.

Each draft is written to drafts/ with the source text it came from, and its deck to decks/ (the deck
config, and a mapping from each IR name to the labware chosen, its barcode and where it goes), so the
self-healing loop's input is always reviewable.

revise() takes a scientist's change request for a healed IR: Claude gets the protocol text, the
current plan and the request, and the revised plan goes through the same checks as a first draft.
"""

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

from pipeline import deck_builder
from pipeline import fidelity
from pipeline import paths
from pipeline.deck import INSTRUMENT_DECK, ROOT, build_deck, loaded_wells
from pipeline.labware_limits import labware_limits
from pipeline.setup_guide import nominal_tip_ul
from pipeline.stage2_compiler import ACTIONS, CompilationError, translate_step

DRAFTS = paths.DRAFTS  # the working folder
DECKS = paths.DECKS
# The CLI binary; set CLAUDE_BIN to use another install (or a stand-in for tests).
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
DIM, RESET = "\033[2m", "\033[0m"

PROMPT = """\
You turn a scientist's written lab protocol into a JSON plan for a Hamilton STARlet liquid handler \
with an 8-channel pipetting head, driven by PyLabRobot. Reply with the plan as a single JSON object in \
a ```json block, after at most a short paragraph of reasoning.

# Labware
Name every labware the protocol needs in "labware", by its role in the protocol ("diluent", "culture", \
"dilution_plate", "tips", "waste"), and say what it must be; the steps use these names. Real labware is then \
found for each need in the lab's library, preferring what is on the deck now. Kinds:
- tip_rack: "tip_volume_ul" (the smallest tip that holds one aspiration), optional "filter": true/false
- plate: "wells": 96, "min_capacity_ul" (per well)
- reservoir (a trough), tube (one tube in a tube rack): "min_capacity_ul" (what you load, plus margin)
- waste: tips and discarded liquid; every protocol has one
On the deck now (use these when they fit): {deck}
In the library as well: {library}

# Plan format
{{
  "protocol_name": "short name",
  "description": "one or two sentences on what the run does",
  "assumptions": ["every choice you made that the text did not state, e.g. which plate holds the samples"],
  "outside_run": ["<ids of requirements done wholly before or after the run>"],
  "labware": {{
    "tips": {{"kind": "tip_rack", "tip_volume_ul": 300, "filter": true, "description": "what it is for"}},
    "diluent": {{"kind": "reservoir", "min_capacity_ul": 8000, "description": "..."}},
    "dilution_plate": {{"kind": "plate", "wells": 96, "min_capacity_ul": 200, "description": "..."}},
    "waste": {{"kind": "waste"}}
  }},
  "reagents": {{"<reservoir or tube name>": "what the scientist loads there, e.g. 0.9% saline (sterile)"}},
  "initial_volumes_ul": {{"<reservoir or tube name>": <uL loaded before the run>, "<plate>:A1:H1": <uL in EACH of those wells>}},
  "steps": [
    {{"step": 1, "action": "tips_on", "labware": "tips", "column": 1, "volume_ul": 0, "channels": [0,1,2,3,4,5,6,7], "description": "..."}},
    {{"step": 2, "action": "aspirate", "labware": "diluent", "volume_ul": 50, "channels": [0,1,2,3,4,5,6,7], "description": "..."}},
    {{"step": 3, "action": "dispense", "labware": "dilution_plate", "column": 2, "volume_ul": 50, "channels": [0,1,2,3,4,5,6,7], "sop": "R2", "description": "..."}},
    {{"step": 4, "action": "tips_off", "labware": "waste", "volume_ul": 0, "channels": [0,1,2,3,4,5,6,7], "description": "..."}}
  ]
}}

Actions: {actions}. Every step has action, labware, volume_ul (0 for tips_on/tips_off), channels and \
description; "column" (1-12) is required for plates and tip racks and left out for reservoirs, tubes and waste.
- Channel i works on row "ABCDEFGH"[i] of a plate or tip rack, so one step with all 8 channels covers a \
whole plate column (8 replicate rows).
- tips_on picks up one column of a tip rack; each tip column can be used once in the whole run.
- tips_off drops every mounted tip into the waste.
- Tips may aspirate repeatedly from the same source; use tips_off and fresh tips before aspirating from a \
different source. Dispensing never changes a tip's source, but aspirating from the well you just dispensed into does, so mix a well before taking liquid out of it, not after filling it: for a serial transfer, mix column k (aspirate and dispense in column k), aspirate the transfer volume from column k, dispense into column k+1, then tips_off. Mix the last column with fresh tips at the end.
- Keep one aspiration within the tip you ask for. Plate wells start empty; only what initial_volumes_ul lists \
holds liquid at the start: reservoirs and tubes by name, and pre-filled plate wells as "<plate>:A1:H1" (each well \
holding that volume). A different sample per row goes in a column of a separate source plate, pre-filled this way, so all \
8 channels draw their own sample at once. Pre-fill only such samples, never the wells the steps dispense into, and \
never a reagent that is the same for every well (a diluent): that stays in a reservoir and the robot pipettes it. Load at least what is drawn plus {well_min:g} uL per well. A well should \
keep {well_min:g} uL or more and stay below its capacity.
- Use the protocol's volumes exactly; never scale them. Each sample gets what the protocol says it gets. When a \
volume does not fit, change the hardware, not the experiment: a deep-well plate or tubes that hold it, larger tips, or \
several aspirate/dispense cycles that add up to it. If the robot cannot do an addition at that volume, it is a manual step \
that says the volume.
- A step the robot cannot do but the experiment needs between liquid-handling steps (centrifuge, vortex, \
incubate or shake off the deck, move labware on or off the deck, add a sample by hand) is a "manual" step, in its \
place in the order: {{"action": "manual", "labware": "<the labware the operator handles>", "volume_ul": 0, \
"channels": [0], "instruction": "<one plain instruction, with speeds, times and temperatures from the text>", \
"duration_min": <about how long, optional>, "empties": [{{"labware": "<plate>", "column": <c>}}], "description": "..."}}. \
"empties" lists the plate columns the step leaves empty (a spin column's flow-through that is discarded); leave it out \
otherwise. Tips must be off before a manual step. The operator is asked to do it and the robot waits, so keep the \
instruction exact and complete, with every number as the protocol writes it.
{extended}
# What the protocol requires
These requirements were read from the protocol, in its order. The plan is checked against them, and a plan that \
changes any of them is sent back:
{requirements}
- Tag every step that carries out a requirement with "sop": "<id>" (a list of ids if one step does several): the \
dispenses of an addition, the manual or incubate step of anything else. Each addition puts exactly its volume into every \
sample, from a reservoir or tube whose "reagents" entry names that reagent; no reagent goes into a sample without a tag.
- The requirements happen in this order. Only the first or last ones may be done wholly before or after the run \
(weighing tissue, reading a spectrophotometer, storage): list their ids in "outside_run". Every one in between is in the \
plan, as a manual step if the robot cannot do it.
- A requirement keeps its numbers (temperatures, times, speeds, g-forces, amounts): write them in the manual \
instruction as the protocol writes them, or set them on the incubate/shake step.

# Protocol text from the scientist
<protocol>
{source}
</protocol>
"""

EXTENDED = """- empty: aspirate everything in a plate column into the waste (volume_ul 0).
- incubate / shake: hold a plate on its heater-shaker for duration_s seconds (temperature_c, speed_rpm); \
tips must be off first. Only plates placed on a heater-shaker can be incubated or shaken.
"""

REVISE = """
# Current plan
The plan below was drafted from this protocol, then repaired until it passed the simulator.{history}

```json
{current}
```

# Change requested by the scientist
<request>
{note}
</request>

Revise the current plan to make this change. Keep everything the request does not touch as it is, \
including repairs already made (for example, steps split per channel), and the "sop" tags. Update "assumptions" if the \
change affects them. If the request changes something a requirement fixes (a volume, a number, or leaving one out), \
add to "deviations": {{"sop": "<id>", "volume_ul": <new uL per sample> or "values": [{{"value": .., "unit": ".."}}] \
or "omit": true, "approved": "<the words of the request that ask for it, copied exactly>"}}; keep the deviations already \
in the plan. Reply with the whole revised plan as a single JSON object in a ```json block.
"""

RETRY = """\
Your plan could not be used: {errors}
Reply with the corrected plan as a single JSON object in a ```json block."""

UNRESOLVED = """\
No real labware was found for these labware needs:
{feedback}
Change those needs (a size the library has, or another kind, and the steps and volumes that depend on it), \
record the change in "assumptions", and reply with the whole corrected plan as a single JSON object in a \
```json block."""


REQUIREMENTS = """\
Read the lab protocol below and list what the experiment requires, so that a plan for a liquid-handling robot can be \
checked against it. Do not plan anything and do not adapt anything to a robot: write down what the protocol says.

If the protocol has alternative procedures (for different sample types, say), cover the main one: the first, unless the \
text says otherwise. Name what you covered and what you left out in "scope".

List, in the order they happen, one requirement per action:
- "addition": a liquid added to each sample: "what" is the reagent as the protocol names it, and "volume_ul" how much \
goes into one sample, in uL (180 for "180 ul", 1200 for "1.2 ml"); null when the protocol moves all of a liquid \
("pipet the mixture into the column").
- "step": anything else the experiment needs (place or mince tissue, vortex, mix, incubate, centrifuge, discard, \
transfer the column to a new tube): "what" says it in a few words.
Give each "values": every number the action must keep, other than an addition's volume (temperatures, times, speeds, \
g-forces, masses, repeat counts), each as written in the protocol, with its unit: {{"value": 56, "unit": "C"}}, or \
{{"min": 12, "max": 15, "unit": "mg"}} for a range, {{"min": 6000, "unit": "x g"}} for "at least". Give each the "quote": the sentence of \
the protocol it comes from, copied word for word, which holds every number you give for it; and the "section" number if \
the protocol has them.

Reply with a single JSON object in a ```json block:
{{
  "scope": {{"covered": "the procedure covered", "left_out": ["each alternative or section left out"]}},
  "requirements": [
    {{"id": "R1", "section": "1.2", "kind": "addition", "what": "Buffer ATL", "volume_ul": 180, "values": [], "quote": "Add 180 ul Buffer ATL."}},
    {{"id": "R2", "section": "1.4", "kind": "step", "what": "incubate until lysed", "volume_ul": null, \
"values": [{{"value": 56, "unit": "C"}}], "quote": "Incubate at 56C until tissue is completely lysed."}}
  ]
}}

<protocol>
{source}
</protocol>
"""


class DraftError(RuntimeError):
    """The CLI could not be run, or did not return a usable plan."""


@dataclass
class Draft:
    protocol: Dict[str, Any]
    path: Path
    attempts: int
    cost_usd: float = 0.0
    replies: List[str] = field(default_factory=list)
    deck_path: Optional[Path] = None
    mapping_path: Optional[Path] = None
    deck_rounds: int = 0  # replies whose labware needs did not all resolve


def read_source(source: str) -> Dict[str, Any]:
    """The protocol text from a PDF or text file path, or `source` itself when it is not a file.

    Returns {"text", "name", "pdf"}; "pdf" is the path of a PDF whose text could not be extracted
    (e.g. a scan), for Claude to read itself.
    """
    path = Path(source).expanduser()
    try:
        is_file = "\n" not in source and path.is_file()
    except OSError:  # e.g. a paragraph longer than a file name can be
        is_file = False
    if not is_file:
        return {"text": source.strip(), "name": "pasted_text", "pdf": None}
    if path.suffix.lower() != ".pdf":
        return {"text": path.read_text().strip(), "name": path.stem, "pdf": None}
    from pypdf import PdfReader

    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages).strip()
    return {"text": text, "name": path.stem, "pdf": None if text else path}


def deck_summary(deck_config: Dict[str, Any]) -> Dict[str, Any]:
    """Labware lines for the prompt, with the capacities PLR uses for them and the plate limits stage 1 checks
    (pipeline/labware_limits.py); with several plates, the strictest limits."""
    _, res = build_deck(deck_config)
    limits = {lid: spec["well_specifications"]["well_volume_range"] for lid, spec in labware_limits(deck_config)["plates"].items()}
    lines, tip_max = [], 300.0
    well = (max((v["min_ul"] for v in limits.values()), default=30.0), min((v["max_ul"] for v in limits.values()), default=330.0))
    for lid, spec in deck_config["labware"].items():
        kind, r = spec["kind"], res[lid]
        if kind == "tip_rack":
            tip_max = nominal_tip_ul(spec["factory"], r.get_item("A1").get_tip().maximal_volume)
            lines.append(f"- {lid}: tip rack, 96 tips of {tip_max:g} uL (12 columns)")
        elif kind == "plate":
            on = f", on heater-shaker {spec['on']}" if "on" in spec else ""
            usable = f", usable {limits[lid]['min_ul']:g}-{limits[lid]['max_ul']:g} uL" if lid in limits else ""
            lines.append(f"- {lid}: 96-well plate, {r.get_item('A1').max_volume:.4g} uL wells{usable}{on}")
        elif kind == "container":
            lines.append(f"- {lid}: single container ({spec['factory']}), holds {r.max_volume / 1000:g} mL")
        elif kind == "trash":
            lines.append(f"- {lid}: waste (tips and discarded liquid)")
    return {"deck": "\n".join(lines), "tip_max": tip_max, "well_min": well[0], "well_max": well[1]}


def available(base_deck: Dict[str, Any], root: Path = ROOT) -> Dict[str, str]:
    """What labware there is, in the words of the needs: on the deck now, and in VENUS's library."""
    _, res = build_deck(base_deck)
    on_deck = []
    for lid, spec in base_deck["labware"].items():
        r = res[lid]
        if spec["kind"] == "tip_rack":
            tip = r.get_item("A1").get_tip()
            on_deck.append(f"a rack of 96 {nominal_tip_ul(spec['factory'], tip.maximal_volume):g} uL tips"
                           f"{' with filter' if tip.has_filter else ''}")
        elif spec["kind"] == "plate":
            on_deck.append(f"a 96-well plate of {r.get_item('A1').max_volume:.4g} uL wells ({spec.get('venus_type', spec['factory'])})")
        elif spec["kind"] == "container":
            on_deck.append(f"a container of {r.max_volume / 1000:g} mL")
    entries = deck_builder.catalog(root, base_deck.get("catalog", "venus"))

    def sizes(kind: str, key: str, unit: float, fmt: str) -> str:
        values = sorted({round(e[key] / unit, 1) for e in entries if e["kind"] == kind})
        return ", ".join(fmt.format(v) for v in values[:14]) + (" and more" if len(values) > 14 else "")

    tips = sorted({(e["tip_volume_ul"], e["filter"]) for e in entries if e["kind"] == "tip_rack"})
    library = (f"tips of {', '.join(f'{v:g} uL' + (' (filter)' if f else '') for v, f in tips)}; "
               f"96-well plates of {sizes('plate', 'capacity_ul', 1, '{:g}')} uL per well; "
               f"reservoirs of {sizes('reservoir', 'capacity_ul', 1000, '{:g}')} mL; "
               f"tubes of {sizes('tube_rack', 'capacity_ul', 1000, '{:g}')} mL")
    return {"deck": "; ".join(on_deck) or "nothing", "library": library}


def build_prompt(source_text: str, base_deck: Dict[str, Any], pdf: Optional[Path] = None,
                 requirements: Optional[List[Dict[str, Any]]] = None) -> str:
    has_devices = bool(base_deck.get("machines"))
    actions = ACTIONS if has_devices else tuple(a for a in ACTIONS if a not in ("empty", "incubate", "shake"))  # manual stays
    source = source_text or f"(The protocol is in the PDF file {pdf.name} in the current directory; read it.)"
    reqs = (fidelity.prompt_lines(requirements) if requirements else
            "(None were read. Keep every volume and number of the protocol exactly; steps need no \"sop\" tag.)")
    return PROMPT.format(**available(base_deck), well_min=30, actions=", ".join(actions),
                         extended=EXTENDED if has_devices else "", requirements=reqs, source=source)


def extract_requirements(src: Dict[str, Any], model: Optional[str] = None, out: TextIO = sys.stdout,
                         max_attempts: int = 3) -> Dict[str, Any]:
    """What the protocol requires (pipeline/fidelity.py), read from its text by its own Claude session, which knows
    nothing of the robot. Each reply is checked against the text (every quote in it, every number in its quote) and
    sent back until it holds. Returns {"scope", "requirements", "quotes_checked", "cost_usd"}."""
    prompt = REQUIREMENTS.format(source=src["text"] or f"(The protocol is in the PDF file {src['pdf'].name} in the "
                                                       "current directory; read it.)")
    cost, session, errors = 0.0, None, []
    with tempfile.TemporaryDirectory(prefix="ir_reqs_") as tmp:
        workdir = Path(tmp)
        if src.get("pdf"):
            shutil.copy(src["pdf"], workdir / src["pdf"].name)
        for attempt in range(1, max_attempts + 1):
            reply = _call_claude(prompt, workdir, model, bool(src.get("pdf")), out, resume=session)
            cost += reply["cost_usd"]
            session = reply["session_id"]
            try:
                spec = extract_plan(reply["text"])
                errors = fidelity.spec_errors(spec, src["text"] or None)
            except ValueError as e:
                spec, errors = {}, [str(e)]
            if not errors:
                return {"scope": spec.get("scope") or {}, "requirements": spec["requirements"],
                        "quotes_checked": bool(src["text"]), "cost_usd": cost}
            out.write(f"\n[requirements] attempt {attempt} not usable: {'; '.join(errors)}\n")
            if not session:
                break
            prompt = ("These requirements do not match the protocol: " + "; ".join(errors) +
                      "\nReply with the corrected list as a single JSON object in a ```json block.")
    raise DraftError(f"Could not read the protocol's requirements after {attempt} attempt(s): {'; '.join(errors)}")


def extract_plan(reply: str) -> Dict[str, Any]:
    """The JSON object in a reply: the last ```json block, else the outermost braces."""
    blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", reply, re.DOTALL)
    text = blocks[-1] if blocks else reply[reply.find("{"): reply.rfind("}") + 1]
    try:
        plan = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"the reply has no valid JSON object ({e})") from None
    if not isinstance(plan, dict):
        raise ValueError("the reply's JSON is not an object")
    return plan


def structural_errors(plan: Dict[str, Any]) -> List[str]:
    """Problems that stop the IR from compiling at all, before any labware is looked up."""
    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        return ["'steps' must be a non-empty list"]
    needs = plan.get("labware")
    errors = deck_builder.need_errors(needs)
    if errors:
        return errors
    kinds = {name: deck_builder.DECK_KIND[need["kind"]] for name, need in needs.items()}
    for lid in plan.get("initial_volumes_ul", {}) or {}:
        wells = loaded_wells(lid)
        if wells is not None:
            if kinds.get(wells[0]) != "plate":
                errors.append(f"initial_volumes_ul names wells of '{wells[0]}', which is not a plate in 'labware'")
        elif kinds.get(lid) != "container":
            errors.append(f"initial_volumes_ul names '{lid}', which is not a reservoir or tube in 'labware' "
                          "(or plate wells, as \"plate:A1:H1\")")
    for i, s in enumerate(steps, start=1):
        if not isinstance(s, dict):
            errors.append(f"step {i} is not an object")
            continue
        if s.get("labware") not in kinds:
            errors.append(f"step {i} uses '{s.get('labware')}', which is not in 'labware'")
            continue
        try:
            translate_step({**s, "step": i}, kinds)
        except CompilationError as e:
            errors.append(str(e))
    return errors[:10]


def normalize(plan: Dict[str, Any], source: Dict[str, Any], deck_file: str,
              requirements: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Renumber steps, fill defaults the rest of the pipeline relies on, and keep the source text and the requirements
    read from it (never the drafter's own copy of them)."""
    plan.pop("requirements", None)
    plan.pop("requirements_scope", None)
    if requirements and requirements.get("requirements"):
        plan["requirements"] = requirements["requirements"]
        plan["requirements_scope"] = {**(requirements.get("scope") or {}),
                                      "quotes_checked": requirements.get("quotes_checked", True)}
    plan.setdefault("initial_volumes_ul", {})
    plan["deck_config"] = deck_file
    for i, s in enumerate(plan["steps"], start=1):
        s["step"] = i
        s.setdefault("volume_ul", 0)
        s.setdefault("channels", [0])
        s.setdefault("description", f"{s.get('action')} {s.get('labware', '')}".strip())
    plan["source"] = {"name": source["name"], "text": source["text"]}
    return plan


class _ReplyPrinter:
    """Writes Claude's reply as it streams, showing the JSON plan as a running step count
    instead of the raw JSON (the full reply is saved next to the draft)."""

    def __init__(self, out: TextIO):
        self.out, self.full, self.pos, self.json_start, self.steps = out, "", 0, None, -1

    def feed(self, text: str) -> None:
        self.full += text
        while True:
            if self.json_start is None:
                i = self.full.find("```json", self.pos)
                if i == -1:
                    safe = max(self.pos, len(self.full) - 7)  # a fence may be split across deltas
                    self.out.write(self.full[self.pos:safe])
                    self.pos = safe
                    break
                self.out.write(self.full[self.pos:i])
                self.json_start = self.pos = i + 7
                continue
            region = self.full[self.json_start:]
            end = region.find("```")
            steps = (region if end == -1 else region[:end]).count('"action"')
            if steps != self.steps:
                self.steps = steps
                self.out.write(f"\r  [writing the plan: {steps} steps]")
            if end == -1:
                break
            self.out.write("\n")
            self.pos, self.json_start = self.json_start + end + 3, None
        self.out.flush()

    def close(self) -> None:
        if self.json_start is None:
            self.out.write(self.full[self.pos:])
        self.out.write("\n")
        self.out.flush()


def _claude_env() -> Dict[str, str]:
    """The environment without the CLAUDE* variables a surrounding Claude session sets, so the CLI
    runs as its own session with its own login wherever the pipeline is started from."""
    keep = {"CLAUDE_BIN", "CLAUDE_CONFIG_DIR"}
    return {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE") or k in keep}


def _call_claude(prompt: str, workdir: Path, model: Optional[str], allow_read: bool,
                 out: TextIO, resume: Optional[str] = None) -> Dict[str, Any]:
    """Run `claude -p` and stream its reply to `out`. Returns {"text", "session_id", "cost_usd"}."""
    if shutil.which(CLAUDE_BIN) is None and not Path(CLAUDE_BIN).is_file():
        raise DraftError(
            f"The Claude CLI ('{CLAUDE_BIN}') is not on PATH. Install it with "
            "`npm install -g @anthropic-ai/claude-code`, run `claude` once to log in, then retry.")
    cmd = [CLAUDE_BIN, "-p", "--output-format", "stream-json", "--verbose", "--include-partial-messages"]
    cmd += ["--allowedTools", "Read"] if allow_read else ["--disallowedTools", "Bash,Edit,Write,WebFetch,WebSearch"]
    if model:
        cmd += ["--model", model]
    if resume:
        cmd += ["--resume", resume]
    proc = subprocess.Popen(cmd, cwd=workdir, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1, env=_claude_env())
    assert proc.stdin and proc.stdout and proc.stderr
    proc.stdin.write(prompt)
    proc.stdin.close()

    result: Dict[str, Any] = {"text": "", "session_id": resume, "cost_usd": 0.0}
    streamed = False  # True once text deltas arrive, so whole assistant messages are not printed twice
    printer = _ReplyPrinter(out)
    for line in proc.stdout:
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = ev.get("type")
        if kind == "stream_event":
            delta = ev.get("event", {}).get("delta", {})
            if delta.get("type") == "text_delta":
                streamed = True
                printer.feed(delta["text"])
            elif delta.get("type") == "thinking_delta":
                out.write(DIM + delta["thinking"] + RESET)
                out.flush()
        elif kind == "assistant" and not streamed:
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    printer.feed(block["text"])
        elif kind == "result":
            if ev.get("is_error"):
                raise DraftError(f"The Claude CLI reported an error: {ev.get('result') or ev.get('subtype')}")
            result.update(text=ev.get("result", ""), session_id=ev.get("session_id"),
                          cost_usd=float(ev.get("total_cost_usd") or 0.0))
    proc.wait()
    printer.close()
    if proc.returncode != 0 and not result["text"]:
        raise DraftError(f"The Claude CLI exited with code {proc.returncode}: {proc.stderr.read().strip()[:500]}")
    return result


def fidelity_errors(plan: Dict[str, Any], requirements: List[Dict[str, Any]], revisions: List[Dict[str, Any]] = (),
                    note: str = "") -> List[str]:
    """What a structurally sound plan changes about the experiment its requirements describe (pipeline/fidelity.py)."""
    if not requirements:
        return []
    kinds = {name: deck_builder.DECK_KIND[need["kind"]] for name, need in plan["labware"].items()}
    held = {**plan, "requirements": requirements, "revisions": list(revisions)}
    return fidelity.check(held, kinds, (note,) if note else ())["errors"]


def _ask_for_plan(prompt: str, base_deck: Dict[str, Any], model: Optional[str], out: TextIO,
                  max_attempts: int, pdf: Optional[Path] = None, name: str = "protocol",
                  requirements: Optional[List[Dict[str, Any]]] = None, revisions: List[Dict[str, Any]] = (),
                  note: str = ""):
    """Send `prompt` and return (plan, resolution, replies, cost, deck_rounds). A reply that is not valid JSON or
    does not compile, that changes what the protocol requires, or whose labware needs do not all resolve to real
    labware, is sent back to Claude, in the same CLI session, up to `max_attempts` replies in total."""
    replies: List[str] = []
    cost, session, errors, deck_rounds = 0.0, None, [], 0
    with tempfile.TemporaryDirectory(prefix="ir_draft_") as tmp:
        workdir = Path(tmp)  # Claude runs here, away from the repository
        if pdf:
            shutil.copy(pdf, workdir / pdf.name)
        for attempt in range(1, max_attempts + 1):
            reply = _call_claude(prompt, workdir, model, bool(pdf), out, resume=session)
            replies.append(reply["text"])
            cost += reply["cost_usd"]
            session = reply["session_id"]
            try:
                plan = extract_plan(reply["text"])
                errors = structural_errors(plan)
                unfaithful = [] if errors else fidelity_errors(plan, requirements or [], revisions, note)
            except ValueError as e:
                errors, unfaithful = [str(e)], []
            if errors:
                out.write(f"\n[draft] attempt {attempt} not usable: {'; '.join(errors)}\n")
                next_prompt = RETRY.format(errors="; ".join(errors))
            elif unfaithful:
                errors = unfaithful
                out.write(f"\n[fidelity] attempt {attempt} changes the experiment:\n" + "\n".join(f"  - {e}" for e in errors) + "\n")
                next_prompt = RETRY.format(errors=fidelity.feedback(errors))
            else:
                resolution = deck_builder.resolve(plan["labware"], base_deck, name=plan.get("protocol_name") or name)
                if resolution.ok:
                    return plan, resolution, replies, cost, deck_rounds
                deck_rounds += 1
                errors = [f"no labware for {', '.join(resolution.unresolved)}"]
                out.write(f"\n[deck] attempt {attempt}: no real labware for some needs:\n{resolution.feedback()}\n")
                next_prompt = UNRESOLVED.format(feedback=resolution.feedback())
            if not session:
                break
            prompt = next_prompt
    raise DraftError(f"No usable plan after {len(replies)} attempt(s): {'; '.join(errors)}")


def _stem(plan: Dict[str, Any]) -> str:
    name = plan.get("protocol_name") or plan["source"]["name"]
    slug = re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")[:50]
    return f"{slug or 'protocol'}_{datetime.datetime.now():%Y%m%d-%H%M%S}"


def _save(plan: Dict[str, Any], resolution: "deck_builder.Resolution", replies: List[str], cost: float,
          drafts_dir: Path, decks_dir: Path, stem: str, deck_rounds: int) -> Draft:
    """The draft (drafts/<stem>.json, with Claude's replies), its deck and the mapping (decks/<stem>.json,
    decks/<stem>.mapping.json). The draft's deck_config names the deck file."""
    deck_path, mapping_path = deck_builder.save(resolution, decks_dir, stem)
    plan["deck_config"] = paths.in_work(deck_path)
    drafts_dir.mkdir(parents=True, exist_ok=True)
    path = drafts_dir / f"{stem}.json"
    path.write_text(json.dumps(plan, indent=2))
    (drafts_dir / f"{stem}.claude.md").write_text("\n\n---\n\n".join(replies))
    return Draft(plan, path, len(replies), cost, replies, deck_path, mapping_path, deck_rounds)


def draft(
    source: str,
    base_deck: Dict[str, Any],
    deck_file: str = INSTRUMENT_DECK,
    model: Optional[str] = None,
    out: TextIO = sys.stdout,
    max_attempts: int = 5,
    drafts_dir: Path = DRAFTS,
    decks_dir: Path = DECKS,
    stem: Optional[str] = None,
) -> Draft:
    """Draft an IR for `source` (a PDF/text path or the protocol text), build its deck on `base_deck` (the deck on
    the STARlet, `deck_file`) from the labware library, and write both."""
    src = read_source(source)
    if not src["text"] and not src["pdf"]:
        raise DraftError("The protocol text is empty.")
    out.write("Reading what the protocol requires (its own Claude session, which knows nothing of the robot)\n")
    reqs = extract_requirements(src, model, out)
    out.write(f"\n{len(reqs['requirements'])} requirements:\n{fidelity.prompt_lines(reqs['requirements'])}\n\n")
    prompt = build_prompt(src["text"], base_deck, src["pdf"], reqs["requirements"])
    plan, resolution, replies, cost, deck_rounds = _ask_for_plan(prompt, base_deck, model, out, max_attempts,
                                                                 src["pdf"], src["name"], reqs["requirements"])
    plan = normalize(plan, src, deck_file, reqs)
    return _save(plan, resolution, replies, cost + reqs["cost_usd"], drafts_dir, decks_dir, stem or _stem(plan), deck_rounds)


def revision_stem(stem: str) -> str:
    """serial_dilution -> serial_dilution_r2 -> serial_dilution_r3."""
    m = re.fullmatch(r"(.*)_r(\d+)", stem)
    return f"{m.group(1)}_r{int(m.group(2)) + 1}" if m else f"{stem}_r2"


def revise(
    current: Dict[str, Any],
    note: str,
    base_deck: Dict[str, Any],
    current_name: str,
    deck_file: str = INSTRUMENT_DECK,
    model: Optional[str] = None,
    out: TextIO = sys.stdout,
    max_attempts: int = 5,
    drafts_dir: Path = DRAFTS,
    decks_dir: Path = DECKS,
    stem: Optional[str] = None,
) -> Draft:
    """Revise a healed IR (`current`, saved as `current_name`) with the scientist's change request, build the
    revision's deck again on `base_deck`, and write both. Earlier requests are kept in the IR's "revisions"."""
    note = note.strip()
    if not note:
        raise DraftError("The change request is empty.")
    source = current.get("source") or {"name": current_name, "text": ""}
    history = current.get("revisions", [])
    hidden = ("source", "revisions", "deck_config", "requirements", "requirements_scope")
    plan_only = {k: v for k, v in current.items() if k not in hidden}
    earlier = "".join(f"\n- {r['note']}" for r in history)
    requirements = current.get("requirements") or []
    prompt = build_prompt(source["text"] or "(Not available; work from the current plan.)", base_deck,
                          requirements=requirements)
    prompt += REVISE.format(
        current=json.dumps(plan_only, indent=1), note=note,
        history=f" Changes the scientist already asked for:{earlier}" if history else "")
    plan, resolution, replies, cost, deck_rounds = _ask_for_plan(prompt, base_deck, model, out, max_attempts,
                                                                 name=current_name, requirements=requirements,
                                                                 revisions=history, note=note)
    scope = dict(current.get("requirements_scope") or {})
    kept = ({"requirements": requirements, "quotes_checked": scope.pop("quotes_checked", True), "scope": scope}
            if requirements else None)
    plan = normalize(plan, source, deck_file, kept)
    plan["revisions"] = history + [{"note": note, "from": current_name}]
    return _save(plan, resolution, replies, cost, drafts_dir, decks_dir, stem or _stem(plan), deck_rounds)
