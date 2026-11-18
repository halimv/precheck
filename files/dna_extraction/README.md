# DNA extraction fixture (nPOD OPPC-SOP-79.1)

This folder is a ready-made PreCheck working folder for testing app changes on a protocol that is not a serial
dilution. It holds three healed protocols drafted from `sop.txt` (the text of the nPOD DNA extraction SOP, Qiagen
DNeasy).

| Protocol (`healed/`) | Built for | What it exercises |
|---|---|---|
| `dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823` | PreCheck + AHC (the lab's VENUS labware) | 50 steps, 17 by hand. The output (8 spin columns of 100 uL TE) leaves the deck by centrifuge. Two items AHC cannot load. Shallow troughs. |
| `npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908` | PreCheck + AHC | The samples are four separate tubes, so the output is tubes, not a plate. |
| `dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626` | PreCheck alone (PyLabRobot's catalog, `--target plr`) | Every piece of labware is PyLabRobot's. It needed one repair: no liquid class for 50 uL filter tips. |

Each protocol has its IR (`.json`), a standalone PyLabRobot script (`_plr.py`), its report, summary, heal log and AHC
layout. Its deck is in `decks/`.

## Use it

```bash
# open the pages on this folder (Execute lists the three protocols)
cd files/dna_extraction && PRECHECK_PORT=8020 ../../plugin/bin/precheck --ui

# rehearse a script on the simulated STAR (manual steps wait for Enter; `yes ""` answers them)
cd plugin && yes "" | uv run python ../files/dna_extraction/healed/<name>_plr.py --backend chatterbox

# check one again from its IR
cd plugin && PRECHECK_WORKDIR=../files/dna_extraction uv run python pipeline.py --protocol ../files/dna_extraction/healed/<name>.json
```

The scripts find PreCheck's code in this repo (`PLUGIN_ROOT` is `plugin/`, relative to the script). Their run outputs
(`runs/`, `build/`, `drafts/`, `knowledge/`) are git-ignored here.
