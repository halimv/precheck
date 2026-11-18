# DNeasy tissue DNA extraction (nPOD SOP-79, section 1.0)

**PASSED: ready for AHC**

## Result

- Steps: 49
- Simulated on: PyLabRobot's STAR model, configured as this instrument
- Repair models tried: claude-haiku-5-5 (1 round(s), HEALED)
- Final simulator result: passed

## Needs human review

| Severity | Area | Item | Detail |
|---|---|---|---|
| must | deck | Place on the deck before the run | tips_50: add carrier: hamilton_96_tiprack_50uL_filter at TIP_CAR_480_1 (rail 1) position 1 |
| must | deck | Place on the deck before the run | tips_300: add carrier: hamilton_96_tiprack_300uL_filter at TIP_CAR_480_1 (rail 1) position 2 |
| must | deck | Place on the deck before the run | tips_1000: add carrier: hamilton_96_tiprack_1000uL_filter at TIP_CAR_480_1 (rail 1) position 3 |
| must | deck | Place on the deck before the run | buffer_atl: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_7 (rail 7) position 1 |
| must | deck | Place on the deck before the run | proteinase_k: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_7 (rail 7) position 2 |
| must | deck | Place on the deck before the run | buffer_al: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_7 (rail 7) position 3 |
| must | deck | Place on the deck before the run | ethanol: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_7 (rail 7) position 4 |
| must | deck | Place on the deck before the run | buffer_aw1: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_8 (rail 8) position 1 |
| must | deck | Place on the deck before the run | buffer_aw2: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_8 (rail 8) position 2 |
| must | deck | Place on the deck before the run | te_buffer: add carrier: hamilton_1_trough_60mL_Vb at Trough_CAR_5R60_A00_8 (rail 8) position 3 |
| must | deck | Place on the deck before the run | lysis_tubes: add carrier: Cor_96_wellplate_2mL_Vb at PLT_CAR_L5MD_9 (rail 9) position 1 |
| must | deck | Place on the deck before the run | spin_columns: add carrier: eppendorf_96_wellplate_1000ul_Vb at PLT_CAR_L5MD_9 (rail 9) position 2 |
| check | fidelity | Held to 31 requirements read from the SOP (Section 1.0 DNA Extraction from Tissue (fresh or snap frozen tissue), steps 1.1 through 1.14) | Every volume and number below is the SOP's. Confirm none is missing. Left out: Section 2.0 DNA Extraction from OCT Blocks (alternative sample preparation that joins at step 1.2); Section 3.0 DNA Extraction from Formalin-fixed Paraffin-embedded Tissue Sections (alternative xylene/ethanol deparaffinization and overnight digestion, which joins at step 1.5); Section 4.0 Quantification and Quality Analysis (step 1.15 points to it; spectrophotometer measurement, data analysis, concentration adjustment, aliquoting and -80°C storage); Safety policy, equipment list and references sections. |
| check | manual | Step 1 is done by hand (about 20 min) | Place tissue in a 1.5 ml microcentrifuge tube for each of the 8 samples. Use 12-15 mg spleen or 25 mg pancreas. Mince further with sterile scissors or scalpel to aid digestion. Put the open tubes in positions A1-H1 of the lysis tube rack on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 12 is done by hand (about 3 min) | Cap the tubes, mix thoroughly by vortexing, then return the open tubes to positions A1-H1 on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 13 is done by hand (about 150 min) | Incubate the capped tubes at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours; if digestion is incomplete, continue 1-2 more hours. Then return the tubes to positions A1-H1 on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 14 is done by hand (about 2 min) | Vortex the capped tubes 15 seconds, then return the open tubes to positions A1-H1 on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 19 is done by hand (about 2 min) | Cap the tubes and vortex thoroughly, then return the open tubes to positions A1-H1 on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 24 is done by hand (about 2 min) | Cap the tubes and vortex again, then return the open tubes to positions A1-H1 on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 25 is done by hand (about 3 min) | Place 8 DNeasy Mini spin columns, each in a 2 ml collection tube, in positions A1-H1 of the spin column rack on the deck, lids open.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 30 is done by hand (about 4 min) | Close the spin columns, centrifuge at ≥6000 x g for 1 minute. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 31 is done by hand (about 2 min) | Place each DNeasy Mini spin column in a new 2 ml collection tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 36 is done by hand (about 4 min) | Close the spin columns, centrifuge for 1 minute at ≥6000 x g. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 37 is done by hand (about 2 min) | Place each DNeasy column in a new 2 ml collection tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 42 is done by hand (about 6 min) | Close the spin columns, centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 43 is done by hand (about 2 min) | Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 48 is done by hand (about 5 min) | Incubate at room temperature for 5 minutes.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 49 is done by hand (about 4 min) | Close the spin columns and centrifuge for 1 minute at ≥6000 x g to elute DNA. Keep the 1.5 ml tubes with the eluted DNA and discard the spin columns.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | drafting | Assumption made when drafting | 8 samples are processed, one per row (A-H) of column 1. |
| check | drafting | Assumption made when drafting | The 1.5 ml microcentrifuge tubes with the tissue sit in positions A1-H1 of a 96-position rack, represented as the plate 'lysis_tubes' (1500 uL per position). |
| check | drafting | Assumption made when drafting | DNeasy Mini spin columns in 2 ml collection tubes sit in positions A1-H1 of a 96-position rack, represented as the plate 'spin_columns' (about 700 uL per column). |
| check | drafting | Assumption made when drafting | The whole mixture is taken as 600 uL (180 ATL + 20 proteinase K + 200 AL + 200 ethanol), moved in one 1000 uL tip aspiration. The operator moves any leftover liquid by hand when the rack comes off the deck. |
| check | drafting | Assumption made when drafting | Proteinase K is loaded into a small trough so that all 8 channels can draw at once. 1000 uL is loaded to cover the trough's dead volume. |
| check | drafting | Assumption made when drafting | Filter tips are used throughout, as the SOP lists filter pipette tips. |
| check | drafting | Assumption made when drafting | Fresh tips are used for every addition. Tips are dropped before every manual step. |
| check | drafting | Assumption made when drafting | The labware is taken off the deck for each vortex, incubation and centrifuge step and put back in the same position. |
| check | drafting | Assumption made when drafting | The incubation duration_min is an estimate (2 h, plus up to 2 more if digestion is incomplete). |
| check | repair | Repair in round 0 (claude-haiku-5-5) | 1 edit(s) to the steps after: Step 7: UNRECOGNIZED (ValueError: no liquid class is known for channel 0's tip on proteinase_k: 60 uL, with filter, water, jet=False, blow_out=False. Give hamilton_liquid_classes, blow_out=True, which has one, or piston_volumes) |
| must | liquid | 'te_buffer' starts 3.7 mm deep and ends 1.8 mm deep | 1200 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |

## What the SOP requires

Each requirement was read from the SOP, and the plan was checked against it: the volumes are the SOP's, for each of 8 sample(s).

| Requirement | How | Steps | uL per sample | From | SOP |
|---|---|---|---|---|---|
| R1 (1.1) place tissue in microcentrifuge tube (1.5 ml) | by hand | 1 |  |  | Place tissue in a 1.5 ml microcentrifuge tube. |
| R2 (1.1.1) tissue amount: spleen or pancreas (12-15 mg, 25 mg) | by hand | 1 |  |  | Use 12-15 mg spleen or 25 mg pancreas. |
| R3 (1.1.2) mince tissue with sterile scissors or scalpel | by hand | 1 |  |  | Mince further with sterile scissors or scalpel to aid digestion. |
| R4 (1.2) add 180 uL of Buffer ATL to each sample | on the robot | 4 | 180 | buffer_atl (Buffer ATL (DNeasy Blood & Tissue Kit)) | Add 180 µl Buffer ATL. |
| R5 (1.3) add 20 uL of proteinase K to each sample | on the robot | 10 | 20 | proteinase_k (Proteinase K (DNeasy Blood & Tissue Kit)) | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R6 (1.3) mix thoroughly by vortexing | by hand | 12 |  |  | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R7 (1.4) incubate in hybridization oven with moderate rotation until tissue completely lysed (56 C) | by hand | 13 |  |  | Incubate at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. |
| R8 (1.4.1) vortex well periodically during incubation (30 min) | by hand | 13 |  |  | Vortex well every 30 minutes. |
| R9 (1.4.2) check level of digestion (2 h) | by hand | 13 |  |  | Check level of digestion at 2 hours. |
| R10 (1.4.2) if digestion incomplete, continue incubation (1-2 h) | by hand | 13 |  |  | If digestion is incomplete, continue 1-2 more hours. |
| R11 (1.5) vortex (15 s) | by hand | 14 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R12 (1.5) add 200 uL of Buffer AL to each sample | on the robot | 17 | 200 | buffer_al (Buffer AL (DNeasy Blood & Tissue Kit)) | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R13 (1.5) vortex thoroughly | by hand | 19 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R14 (1.6) add 200 uL of 100% ethanol to each sample | on the robot | 22 | 200 | ethanol (100% ethanol (molecular biology grade)) | Add 200 µl 100% ethanol and vortex again. |
| R15 (1.6) vortex again | by hand | 24 |  |  | Add 200 µl 100% ethanol and vortex again. |
| R16 (1.7) DNeasy Mini spin column placed in collection tube (2 ml) | by hand | 25 |  |  | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R17 (1.7) add all of the mixture (into DNeasy Mini spin column) to each sample | on the robot | 28 |  | lysis_tubes (lysis_tubes) | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R18 (1.8) centrifuge (>=6000 x g, 1 min) | by hand | 30 |  |  | Centrifuge at ≥6000 x g for 1 minute. |
| R19 (1.8) discard flow-through and collection tube | by hand | 30 |  |  | Discard flow-through and collection tube. |
| R20 (1.9) place spin column in new collection tube (2 ml) | by hand | 31 |  |  | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R21 (1.9) add 500 uL of Buffer AW1 to each sample | on the robot | 34 | 500 | buffer_aw1 (Buffer AW1 (DNeasy Blood & Tissue Kit, ethanol added)) | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R22 (1.10) centrifuge (1 min, >=6000 x g) | by hand | 36 |  |  | Centrifuge for 1 minute at ≥6000 x g. |
| R23 (1.10) discard flow-through and collection tube | by hand | 36 |  |  | Discard flow-through and collection tube. |
| R24 (1.11) place column in new collection tube (2 ml) | by hand | 37 |  |  | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R25 (1.11) add 500 uL of Buffer AW2 to each sample | on the robot | 40 | 500 | buffer_aw2 (Buffer AW2 (DNeasy Blood & Tissue Kit, ethanol added)) | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R26 (1.12) centrifuge to dry DNeasy membrane (3 min, 20000 x g) | by hand | 42 |  |  | Centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. |
| R27 (1.12) discard flow-through and collection tube | by hand | 42 |  |  | Discard flow-through and collection tube. |
| R28 (1.13) place spin column in new microcentrifuge tube (1.5 ml) | by hand | 43 |  |  | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R29 (1.13) add 100 uL of 1x Tris-EDTA buffer (to the center of the spin column membrane) to each sample | on the robot | 46 | 100 | te_buffer (1x Tris-EDTA, DNase/RNase-free (pH 8.0, 10 mM Tris-HCl, 1 mM EDTA)) | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R30 (1.14) incubate at room temperature (5 min) | by hand | 48 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |
| R31 (1.14) centrifuge to elute DNA (1 min, >=6000 x g) | by hand | 49 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |

## Labware and deck

| Name | Type | Where | Holds |
|---|---|---|---|
| waste | tip waste | the deck's tip waste |  |
| tips_50 | hamilton_96_tiprack_50uL_filter | TIP_CAR_480 at rail 1, position 1 |  |
| tips_300 | hamilton_96_tiprack_300uL_filter | TIP_CAR_480 at rail 1, position 2 |  |
| tips_1000 | hamilton_96_tiprack_1000uL_filter | TIP_CAR_480 at rail 1, position 3 |  |
| buffer_atl | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 7, position 1 | Buffer ATL (DNeasy Blood & Tissue Kit) |
| proteinase_k | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 7, position 2 | Proteinase K (DNeasy Blood & Tissue Kit) |
| buffer_al | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 7, position 3 | Buffer AL (DNeasy Blood & Tissue Kit) |
| ethanol | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 7, position 4 | 100% ethanol (molecular biology grade) |
| buffer_aw1 | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 8, position 1 | Buffer AW1 (DNeasy Blood & Tissue Kit, ethanol added) |
| buffer_aw2 | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 8, position 2 | Buffer AW2 (DNeasy Blood & Tissue Kit, ethanol added) |
| te_buffer | hamilton_1_trough_60mL_Vb | Trough_CAR_5R60_A00 at rail 8, position 3 | 1x Tris-EDTA, DNase/RNase-free (pH 8.0, 10 mM Tris-HCl, 1 mM EDTA) |
| lysis_tubes | Cor_96_wellplate_2mL_Vb | PLT_CAR_L5MD at rail 9, position 1 |  |
| spin_columns | eppendorf_96_wellplate_1000ul_Vb | PLT_CAR_L5MD at rail 9, position 2 |  |

## Reagents

| Labware | Loaded uL | Drawn uL | Left uL |
|---|---|---|---|
| buffer_atl | 2000 | 1440 | 560 |
| proteinase_k | 1000 | 160 | 840 |
| buffer_al | 2500 | 1600 | 900 |
| ethanol | 2500 | 1600 | 900 |
| buffer_aw1 | 5000 | 4000 | 1000 |
| buffer_aw2 | 5000 | 4000 | 1000 |
| te_buffer | 1200 | 800 | 400 |

## Plate wells

| Plate | Column | Rows | Volume uL | Contents | Flags |
|---|---|---|---|---|---|
| lysis_tubes | 1 | ABCDEFGH | 0.0 |  |  |
| spin_columns | 1 | ABCDEFGH | 0 |  |  |

## Files

- ir: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626.json`
- script: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626_plr.py`
- heal_log: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626_heal_log.json`
- ahc_layout: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626.ahc_layout.yaml`
- summary: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626_summary.md`
- report: `healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626_report.json`
