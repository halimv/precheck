# DNeasy DNA extraction from tissue (nPOD SOP-79, section 1.0)

**PASSED: ready for AHC**

## Result

- Steps: 50
- Simulated on: PyLabRobot's STAR model, configured as this instrument
- Repair models tried: claude-haiku-5-5 (0 round(s), ALREADY_PASSING)
- Final simulator result: passed

## Needs human review

| Severity | Area | Item | Detail |
|---|---|---|---|
| must | deck | Place on the deck before the run | tips_1000: add labware: HTF_L at TIP_CAR_480_A00_0001 (rail 7) position 3 |
| must | deck | Place on the deck before the run | lysis_plate: add labware: Rack - RGT 96 Refill at PLT_CAR_L5_DWP_0001 (rail 1) position 1 |
| must | deck | Place on the deck before the run | spin_column_rack: add labware: HAM_DWP_96x08mL at PLT_CAR_L5_DWP_0001 (rail 1) position 2 |
| must | deck | Place on the deck before the run | buffer_atl: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 1 |
| must | deck | Place on the deck before the run | proteinase_k: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 2 |
| must | deck | Place on the deck before the run | buffer_al: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 3 |
| must | deck | Place on the deck before the run | ethanol: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 4 |
| must | deck | Place on the deck before the run | buffer_aw1: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 5 |
| must | deck | Place on the deck before the run | buffer_aw2: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_14 (rail 14) position 1 |
| must | deck | Place on the deck before the run | te_buffer: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_14 (rail 14) position 2 |
| must | AHC | AHC cannot load this item | spin_column_rack (HAM_DWP_96x08mL) on PLT_CAR_L5_DWP_0001 is not labware AHC accepts |
| must | AHC | AHC cannot load this item | lysis_plate (Rack - RGT 96 Refill) on PLT_CAR_L5_DWP_0001 is not labware AHC accepts |
| check | fidelity | Held to 31 requirements read from the SOP (Section 1.0 DNA Extraction from Tissue (fresh or snap frozen tissue), steps 1.1 to 1.14) | Every volume and number below is the SOP's. Confirm none is missing. Left out: Section 2.0 DNA Extraction from OCT Blocks (alternative sample type); Section 3.0 DNA Extraction from Formalin-fixed Paraffin-embedded Tissue Sections (alternative sample type); Step 1.15 and Section 4.0 Quantification and Quality Analysis (spectrophotometry, concentration adjustment, aliquoting, storage at -80°C); Policy, safety, equipment and materials lists (not procedural actions). |
| check | manual | Step 1 is done by hand (about 20 min) | Use 12-15 mg spleen or 25 mg pancreas per sample. Mince further with sterile scissors or scalpel to aid digestion. Place each tissue sample in its 1.5 ml well (A1-H1) of the lysis plate, standing in for a 1.5 ml microcentrifuge tube, and put the plate on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 10 is done by hand (about 2 min) | Seal the lysis plate and mix thoroughly by vortexing.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 11 is done by hand (about 240 min) | Incubate at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours. If digestion is incomplete, continue 1-2 more hours.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 12 is done by hand (about 2 min) | Vortex 15 seconds, unseal the plate and return it to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 17 is done by hand (about 2 min) | Seal the plate, vortex thoroughly, unseal and return it to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 22 is done by hand (about 2 min) | Seal the plate, vortex again, unseal and return it to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 23 is done by hand (about 5 min) | Place a DNeasy Mini spin column in a 2 ml collection tube at each of positions A1-H1 of the spin column rack, open the lids and put the rack on the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 28 is done by hand (about 3 min) | Close the spin columns and centrifuge at ≥6000 x g for 1 minute.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 29 is done by hand (about 2 min) | Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 30 is done by hand (about 3 min) | Place each DNeasy Mini spin column in a new 2 ml collection tube at positions A1-H1, open the lids and return the rack to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 35 is done by hand (about 3 min) | Close the spin columns and centrifuge for 1 minute at ≥6000 x g.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 36 is done by hand (about 2 min) | Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 37 is done by hand (about 3 min) | Place each DNeasy column in a new 2 ml collection tube at positions A1-H1, open the lids and return the rack to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 42 is done by hand (about 5 min) | Close the spin columns and centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 43 is done by hand (about 2 min) | Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 44 is done by hand (about 3 min) | Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube at positions A1-H1, open the lids and return the rack to the deck.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 49 is done by hand (about 5 min) | Incubate at room temperature for 5 minutes.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 50 is done by hand (about 3 min) | Close the spin columns and centrifuge for 1 minute at ≥6000 x g to elute DNA. Keep the 1.5 ml tubes containing the eluted DNA.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | drafting | Assumption made when drafting | 8 tissue samples are processed, one per row (A-H) in column 1 of the lysis plate. |
| check | drafting | Assumption made when drafting | A 96 deep-well plate with wells of at least 1.5 ml stands in for the 1.5 ml microcentrifuge tubes during lysis, so the 8 channels can add reagents to all samples at once. |
| check | drafting | Assumption made when drafting | The 8 DNeasy Mini spin columns, each in a 2 ml collection tube, are held in a 96-position rack (shown as a plate) at positions A1-H1 so the robot can pipette into them. |
| check | drafting | Assumption made when drafting | 'All of the mixture' is 180 + 20 + 200 + 200 = 600 µL per sample. It is moved in one 600 µL aspiration with 1000 µL filter tips, so the lysis wells end empty instead of keeping 30 µL. |
| check | drafting | Assumption made when drafting | Filter tips are used throughout, as the SOP lists filter pipette tips. The deck's 300 µL filter tips are used for additions of 200 µL or less, and 1000 µL filter tips for the 600 µL transfer and the 500 µL washes. |
| check | drafting | Assumption made when drafting | A fresh tip column is used for each reagent. |
| check | drafting | Assumption made when drafting | Proteinase K is pipetted from a small reservoir with extra volume for the robot's dead volume. |
| check | drafting | Assumption made when drafting | Whenever an SOP step needs vortexing, an oven or a centrifuge, the operator takes the plate or rack off the deck for that step (sealed if needed) and puts it back afterwards. |
| check | drafting | Assumption made when drafting | Sections 2.0, 3.0 and 4.0 (OCT blocks, FFPE tissue, quantification and storage) are not part of this run. |
| check | AHC | AHC's model differs from VENUS | carrier PLT_CAR_L5_DWP_0001: AHC builds PyLabRobot's PLT_CAR_L5_DWP, which differs from VENUS (position 5 y: PyLabRobot 8.2, VENUS 9 (-0.80 mm), and 9 more) |
| check | AHC | AHC's model differs from VENUS | Cos_96_PCR_0002: VENUS's Cos_96_PCR goes to AHC as Cor_96_wellplate_360ul_Fb (AHC has no PCR plate, so it gets the 96-well plate AHC has run on this carrier: on a PLT_CAR_L5_DWP its wells are 0.4 mm off in x, their bottom 0.86 mm higher, 10.67 mm deep where VENUS says 20.5, and 360 uL where VENUS says 290) |
| check | AHC | AHC's model differs from VENUS | Cos_96_PCR_0001: VENUS's Cos_96_PCR goes to AHC as Cor_96_wellplate_360ul_Fb (AHC has no PCR plate, so it gets the 96-well plate AHC has run on this carrier: on a PLT_CAR_L5_DWP its wells are 0.4 mm off in x, their bottom 0.86 mm higher, 10.67 mm deep where VENUS says 20.5, and 360 uL where VENUS says 290) |
| check | AHC | AHC's model differs from VENUS | buffer_aw1: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | ethanol: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | buffer_al: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | proteinase_k: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | buffer_atl: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | te_buffer: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | buffer_aw2: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| must | liquid | 'buffer_atl' starts 1.6 mm deep and ends 0.4 mm deep | 2000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'proteinase_k' starts 0.4 mm deep and ends 0.3 mm deep | 500 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'buffer_al' starts 1.6 mm deep and ends 0.3 mm deep | 2000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'ethanol' starts 1.6 mm deep and ends 0.3 mm deep | 2000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'buffer_aw1' starts 3.6 mm deep and ends 0.4 mm deep | 4500 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'buffer_aw2' starts 3.6 mm deep and ends 0.4 mm deep | 4500 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'te_buffer' starts 0.9 mm deep and ends 0.2 mm deep | 1100 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |

## What the SOP requires

Each requirement was read from the SOP, and the plan was checked against it: the volumes are the SOP's, for each of 8 sample(s).

| Requirement | How | Steps | uL per sample | From | SOP |
|---|---|---|---|---|---|
| R1 (1.1) place tissue in 1.5 ml microcentrifuge tube (1.5 ml) | by hand | 1 |  |  | Place tissue in a 1.5 ml microcentrifuge tube. |
| R2 (1.1.1) tissue amount: spleen or pancreas (12-15 mg, 25 mg) | by hand | 1 |  |  | Use 12-15 mg spleen or 25 mg pancreas. |
| R3 (1.1.2) mince tissue with sterile scissors or scalpel | by hand | 1 |  |  | Mince further with sterile scissors or scalpel to aid digestion. |
| R4 (1.2) add 180 uL of Buffer ATL to each sample | on the robot | 4 | 180 | buffer_atl (Buffer ATL (DNeasy Blood & Tissue Kit)) | Add 180 µl Buffer ATL. |
| R5 (1.3) add 20 uL of proteinase K to each sample | on the robot | 8 | 20 | proteinase_k (proteinase K (DNeasy Blood & Tissue Kit)) | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R6 (1.3) mix thoroughly by vortexing | by hand | 10 |  |  | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R7 (1.4) incubate in hybridization oven with moderate rotation until tissue completely lysed (56 C) | by hand | 11 |  |  | Incubate at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. |
| R8 (1.4.1) vortex well periodically during incubation (30 min) | by hand | 11 |  |  | Vortex well every 30 minutes. |
| R9 (1.4.2) check level of digestion (2 h) | by hand | 11 |  |  | Check level of digestion at 2 hours. |
| R10 (1.4.2) if digestion incomplete, continue incubation (1-2 h) | by hand | 11 |  |  | If digestion is incomplete, continue 1-2 more hours. |
| R11 (1.5) vortex (15 s) | by hand | 12 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R12 (1.5) add 200 uL of Buffer AL to each sample | on the robot | 15 | 200 | buffer_al (Buffer AL (DNeasy Blood & Tissue Kit)) | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R13 (1.5) vortex thoroughly | by hand | 17 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R14 (1.6) add 200 uL of 100% ethanol to each sample | on the robot | 20 | 200 | ethanol (100% ethanol (molecular biology grade)) | Add 200 µl 100% ethanol and vortex again. |
| R15 (1.6) vortex again | by hand | 22 |  |  | Add 200 µl 100% ethanol and vortex again. |
| R16 (1.7) DNeasy Mini spin column placed in 2 ml collection tube (2 ml) | by hand | 23 |  |  | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R17 (1.7) add all of the mixture (into DNeasy Mini spin column) to each sample | on the robot | 26 |  | lysis_plate (lysis_plate) | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R18 (1.8) centrifuge (>=6000 x g, 1 min) | by hand | 28 |  |  | Centrifuge at ≥6000 x g for 1 minute. |
| R19 (1.8) discard flow-through and collection tube | by hand | 29 |  |  | Discard flow-through and collection tube. |
| R20 (1.9) place spin column in new 2 ml collection tube (2 ml) | by hand | 30 |  |  | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R21 (1.9) add 500 uL of Buffer AW1 (to column) to each sample | on the robot | 33 | 500 | buffer_aw1 (Buffer AW1 (DNeasy Blood & Tissue Kit)) | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R22 (1.10) centrifuge (1 min, >=6000 x g) | by hand | 35 |  |  | Centrifuge for 1 minute at ≥6000 x g. |
| R23 (1.10) discard flow-through and collection tube | by hand | 36 |  |  | Discard flow-through and collection tube. |
| R24 (1.11) place column in new 2 ml collection tube (2 ml) | by hand | 37 |  |  | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R25 (1.11) add 500 uL of Buffer AW2 to each sample | on the robot | 40 | 500 | buffer_aw2 (Buffer AW2 (DNeasy Blood & Tissue Kit)) | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R26 (1.12) centrifuge to dry DNeasy membrane (3 min, 20000 x g) | by hand | 42 |  |  | Centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. |
| R27 (1.12) discard flow-through and collection tube | by hand | 43 |  |  | Discard flow-through and collection tube. |
| R28 (1.13) place spin column in new 1.5 ml microcentrifuge tube (1.5 ml) | by hand | 44 |  |  | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R29 (1.13) add 100 uL of 1x Tris-EDTA buffer (to center of spin column membrane) to each sample | on the robot | 47 | 100 | te_buffer (1x Tris-EDTA buffer, DNase/RNase-free (pH 8.0, 10 mM Tris-HCl, 1 mM EDTA)) | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R30 (1.14) incubate at room temperature (5 min) | by hand | 49 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |
| R31 (1.14) centrifuge to elute DNA (1 min, >=6000 x g) | by hand | 50 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |

## Labware and deck

| Name | Type | Where | Holds |
|---|---|---|---|
| tips_300 | STF_L | TIP_CAR_480_A00 at rail 7, position 1 |  |
| waste | tip waste | the deck's tip waste |  |
| tips_1000 | HTF_L | TIP_CAR_480_A00 at rail 7, position 3 |  |
| lysis_plate | Rack - RGT 96 Refill | PLT_CAR_L5_DWP at rail 1, position 1 |  |
| spin_column_rack | HAM_DWP_96x08mL | PLT_CAR_L5_DWP at rail 1, position 2 |  |
| buffer_atl | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 1 | Buffer ATL (DNeasy Blood & Tissue Kit) |
| proteinase_k | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 2 | proteinase K (DNeasy Blood & Tissue Kit) |
| buffer_al | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 3 | Buffer AL (DNeasy Blood & Tissue Kit) |
| ethanol | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 4 | 100% ethanol (molecular biology grade) |
| buffer_aw1 | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 5 | Buffer AW1 (DNeasy Blood & Tissue Kit) |
| buffer_aw2 | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 14, position 1 | Buffer AW2 (DNeasy Blood & Tissue Kit) |
| te_buffer | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 14, position 2 | 1x Tris-EDTA buffer, DNase/RNase-free (pH 8.0, 10 mM Tris-HCl, 1 mM EDTA) |

## Reagents

| Labware | Loaded uL | Drawn uL | Left uL |
|---|---|---|---|
| buffer_atl | 2000 | 1440 | 560 |
| proteinase_k | 500 | 160 | 340 |
| buffer_al | 2000 | 1600 | 400 |
| ethanol | 2000 | 1600 | 400 |
| buffer_aw1 | 4500 | 4000 | 500 |
| buffer_aw2 | 4500 | 4000 | 500 |
| te_buffer | 1100 | 800 | 300 |

## Plate wells

| Plate | Column | Rows | Volume uL | Contents | Flags |
|---|---|---|---|---|---|
| lysis_plate | 1 | ABCDEFGH | 0.0 |  |  |
| spin_column_rack | 1 | ABCDEFGH | 0 |  |  |

## Files

- ir: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823.json`
- script: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823_plr.py`
- heal_log: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823_heal_log.json`
- ahc_layout: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823.ahc_layout.yaml`
- summary: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823_summary.md`
- report: `healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823_report.json`
