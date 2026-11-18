# PreCheck and AHC: what is actually different

## The short answer

Most of what separates PreCheck from AHC today is features, and AHC could add features:

- a manual-step tool;
- tubes and deep-well plates;
- a deck picture;
- expected final volumes;
- an agent that reads the SOP before it plans.

None of those is a reason for PreCheck to exist.

The difference that holds is **when each one acts and what it leaves behind**.

| | PreCheck | AHC |
|---|---|---|
| Kind of tool | A compiler and verifier: SOP in, a fixed protocol out | A runtime interlock: one agent's calls in, checked one at a time |
| When it acts | Before any session, with no device, robot or person | During a session, as each call arrives |
| What it leaves | A reviewed, versioned protocol (IR and PyLabRobot script, `_r2`, `_r3`, ...) that runs the same way every time with no model in the loop | A run log of what one agent did, once |
| What it checks | The plan against the SOP: requirements read by a separate model, quotes checked against the text, repairs kept only if they move the same liquid | Each call against the device's limits, the deck against the layout, and final volumes against numbers the agent supplies |
| Whose rules | The experiment's: the SOP | The instrument's: its description file. It is deliberately agnostic of intent |

AHC could not take the left column without becoming a compiler, which is what PreCheck is. AHC is meant to stay a
thin layer of server-side rules between any agent and a robot. PreCheck is meant to turn a document into an
artifact a lab can review once and run many times. The two meet at the hand-off: PreCheck's protocol, layout and
expected volumes are AHC's plan, deck and `volumes_match`.

## Why that matters, as claims to test

The difference is only worth something if it shows up in results. Each claim below is something the comparison in
[`comparison/`](../comparison/README.md) measures, on the same SOPs, with the same scoring for both sides:

1. **Fidelity.** A plan checked against the SOP's own numbers keeps them more often than an agent planning on the
   fly. Measured: required additions present at the SOP's volume per sample, and steps dropped or added.
2. **Repeatability.** A compiled protocol is the same every time. An agent's plan varies from one run to the next.
   Measured: the same SOP planned three times; do the volumes, order and labware differ?
3. **Problems found before a session.** PreCheck finds failures offline and repairs them. With AHC, a problem
   surfaces as a refusal during a session, and the agent replans live. Measured: failures before any session against
   refusals in it, and whether the run finished.
4. **Cost and time.** Measured: wall-clock time and model cost to a protocol that runs.

If PreCheck wins on 1 and 2, that is the selling point: **the SOP, as written, runs the same reviewed way every
time**, backed by numbers rather than by features AHC could add next week. If it does not, the comparison says
so too.

## What the comparison found

The full tables are in [`comparison/RESULTS.md`](../comparison/RESULTS.md). There were 3 trials per arm on each of
two SOPs. Both arms used the same model and were scored by the same hand-written answer key.

| | Agent + AHC | PreCheck |
|---|---|---|
| DNA extraction: key additions right | 4/8 in every trial | 8/8 in every trial |
| Serial dilution: wells at the SOP's ratio | 100% | 100% |
| Serial dilution: SOP's own volumes (1 mL into 10 mL) | Scaled to 100 µL into 900 µL | Kept as written |
| Drafts sent back before a session because they changed the SOP | none (nothing checks) | 2 of 3 DNA trials, every serial trial |
| Same plan in all three trials | No (serial: 2 different plans) | No (serial: 2 different plans) |
| Written protocol compiles to the same script again | n/a: re-planned on every run | 3/3 |
| Time and model cost per run | ~80–110 s, $0.49–0.69 | ~170–270 s, $1.10–2.10, paid once per protocol |
| Labware AHC cannot load | 0 (it only uses AHC's list) | 2 to 5 per protocol |

What this supports:

1. **Fidelity, on an SOP with off-deck work. The claim holds.** On the DNA extraction, the agent did the four lysis
   additions right every time, then stopped. AHC has no tubes, no spin columns and no manual-step tool, so it handed
   the column, the washes and the elution to a person. PreCheck kept all eight additions on the robot at the SOP's
   volumes, with the 17 or 18 off-deck steps as manual steps in order. Its fidelity gate caught a first draft that
   changed the SOP in two of the three trials. Part of the gap is AHC's labware list, which AHC could add. The
   fidelity gate is the part AHC is not built to have.
2. **Fidelity, on a simple SOP. A tie on the ratio.** Both arms got every well of the serial dilution right, as 1:10
   or as the SOP's literal "1 ml in 10 ml" (1:11). They differ on the volumes themselves: the agent scaled them down
   tenfold to fit a plate, while PreCheck kept 1 mL into 10 mL in tubes, which AHC cannot load. Which is right depends
   on whether the SOP's volumes matter to the scientist. PreCheck's rule is that only the scientist may change them.
3. **Repeatability. Only after the protocol is written.** Neither arm drafts the same plan every time. In one serial
   trial PreCheck made a single dilution and left the repeats to a person, which is a worse plan. What does repeat is
   the artifact: a written PreCheck protocol compiles to the same script every time and runs with no model.
   Agent + AHC plans again on every run.
4. **Cost. Agent + AHC is cheaper and faster per run.** PreCheck costs about twice as much, once per protocol rather
   than per run. Its plans are also often not loadable on AHC as written, which is the "port to the lab" step below.

**The defensible selling point:** for an SOP with off-deck steps and fixed volumes, PreCheck turns the document into
a protocol that keeps every one of the SOP's additions and is checked against them, and that runs the same reviewed
way every time. An agent driving AHC got half of the DNA extraction's additions onto the robot, in every trial.
That rests on 2 SOPs and 3 trials each: enough to show a difference, not to put a rate on it.

## Two observations from the DNA extraction SOP

Two observations from the nPOD DNA extraction SOP (OPPC-SOP-79.1):

- **AHC's STARlet takes none of the SOP's own labware.** Its list has no tubes, no tube carriers and two plate
  types. An agent has to choose stand-ins, and nothing checks that the stand-ins keep the SOP's volumes.
  - PreCheck chose them from the lab's VENUS library (322 carriers, 81 plates, 48 tube racks) or from PyLabRobot's
    catalog when run alone.
  - It held the plan to 31 requirements read from the SOP.
  - It found the output: 8 spin columns of 100 µL TE, taken off the deck by the final spin.
- **Some problems are invisible at runtime, to both tools.** Every reagent trough ends 0.2 to 0.4 mm deep, below the
  roughly 2 mm a tip needs. Both simulators and AHC's digital twin track volume, not depth. PreCheck flags it from
  the container's geometry before the run.

## What each should take from the other

- **AHC:** a manual-step tool (PreCheck's reports already name `request_manual_step`, and AHC 0.9.3 has none);
  tubes, tube carriers and deep-well plates; and loading a PreCheck protocol as its plan, with PreCheck's output
  volumes as `volumes_match`.
- **PreCheck:**
  - port a PreCheck-alone protocol onto the lab's labware and AHC's list, and report what had to change. On the DNA
    SOP, PyLabRobot's catalog chose a deep-well plate on a `PLT_CAR_L5MD`, which AHC refuses as too tall.
  - write the expected output into the AHC layout file.

## Honest limits

- PreCheck's simulator checks volumes and positions, not liquid heights or physics. Its liquid-depth flag is a rule
  of thumb.
- The requirements are read by a model. Their quotes are checked against the SOP, but the scientist still has to
  confirm none is missing.
- Nothing PreCheck passes has been measured on an instrument. AHC is what runs it there, with a person on site.
