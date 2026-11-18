# PreCheck against an agent driving AHC

This tests whether PreCheck's role, compiling an SOP into a fixed, checked protocol, gives better results than the
alternative it competes with: an agent that reads the SOP and drives AHC directly. Both arms get the same SOP text
and use the same model (the Claude Code default). They are scored by the same answer key, written by hand from the
SOP, not from PreCheck's own requirement reader.

## The arms

| Arm | What runs | Script |
|---|---|---|
| PreCheck | `pipeline.py <sop.txt> --target lab --yes`: draft, fidelity check, deck from the lab's labware, simulate, repair. Its healed protocol is scored. | `run_precheck.py` |
| Agent + AHC | A Claude agent whose instructions are AHC's own `lab-hardware` skill and whose only tools are AHC's, on AHC's STARlet forced to simulation, in a fresh task folder. Its AHC run log is scored. | `run_agent_ahc.py` |

AHC asks a person to confirm the deck of a new layout. In this benchmark the harness allows that one call and
replaces its note with "Automated simulation benchmark: no person", so no record claims a person approved. Nothing
else is changed. Refusals are AHC's, and the agent replans on its own, as it would with a scientist.

## What is measured

- **Fidelity.** Both arms are reduced to the liquid moves AHC records (container and volume, channel by channel),
  and each tip remembers the reagent it carries. `score.py` then checks the SOP's key against them:
  - DNA extraction: 180 µL ATL, 20 µL proteinase K, 200 µL AL, 200 µL ethanol, the lysate onto a column, 500 µL AW1,
    500 µL AW2 and 100 µL TE, per sample, in that order (±2%).
  - Serial dilution: every dilution well at 1:10, or 1:11 by the SOP's "1 ml in 10 ml" (±3%), over at least two
    steps.
  - Steps done by hand count as not done by the robot; the table reports them separately.
- **Repeatability.** Three trials per arm and SOP. Two trials are the same plan when every key item has the same
  per-sample volume and the same number of wells, in the same order. PreCheck's written protocols are also compiled
  twice, to show the protocol itself is fixed.
- **Problems found before a session.** PreCheck: draft attempts sent back (unusable, changed the SOP, no labware) and
  repair rounds. Agent + AHC: AHC calls refused during the session.
- **Time and cost.** Wall time. Model cost: the SDK's total for the agent; the drafting cost PreCheck prints (repair
  rounds go through the Claude CLI and are not counted).

## Run it

```bash
cd comparison
python3 run_precheck.py dna_extraction 1                    # PreCheck's code via `uv run` in plugin/
<python with ahc, mcp, claude_agent_sdk> run_agent_ahc.py dna_extraction 1 \
    --ahc-mcp <path to ahc-mcp> --skill <ahc repo>/skills/lab-hardware
cd ../plugin && uv run python ../comparison/report.py       # writes comparison/RESULTS.md
```

Trial records go to `results/trials/` and each trial's working folder to `results/` (git-ignored). Trial 0 is a smoke
test and is left out of the report.

## Limits of this comparison

- Two SOPs and three trials per arm: enough to see a difference, not to estimate a rate.
- The key covers liquid handling. Whether the off-deck steps are right (vortex, 56 °C, the spins) is not scored for
  either arm.
- The agent arm is AHC as its plugin is meant to be used, with no extra prompting. A better prompt or a
  PreCheck-like checker in front of AHC would change its numbers. That is the point being tested: whether the
  checking is worth having as its own step.
