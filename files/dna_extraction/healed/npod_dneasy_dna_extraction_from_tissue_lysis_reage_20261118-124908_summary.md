# nPOD DNeasy DNA extraction from tissue (lysis reagent additions)

**PASSED: ready for AHC**

## Result

- Steps: 44
- Simulated on: PyLabRobot's STAR model, configured as this instrument
- Repairs: none needed
- Final simulator result: passed

## Needs human review

| Severity | Area | Item | Detail |
|---|---|---|---|
| must | deck | Place on the deck before the run | atl_buffer: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 1 |
| must | deck | Place on the deck before the run | proteinase_k: add carrier: SMP_CAR_32_EPIS_A00 at SMP_CAR_32_EPIS_A00_14 (rail 14) position 1 |
| must | deck | Place on the deck before the run | al_buffer: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 2 |
| must | deck | Place on the deck before the run | ethanol: add carrier: RGT_CONT_50ml_A00 at RGT_CAR_5R60_A00_13 (rail 13) position 3 |
| must | deck | Place on the deck before the run | sample_1: add carrier: SMP_CAR_32_EPIL_A00 at SMP_CAR_32_EPIL_A00_15 (rail 15) position 1 |
| must | deck | Place on the deck before the run | sample_2: add carrier: SMP_CAR_32_EPIL_A00 at SMP_CAR_32_EPIL_A00_15 (rail 15) position 2 |
| must | deck | Place on the deck before the run | sample_3: add carrier: SMP_CAR_32_EPIL_A00 at SMP_CAR_32_EPIL_A00_15 (rail 15) position 3 |
| must | deck | Place on the deck before the run | sample_4: add carrier: SMP_CAR_32_EPIL_A00 at SMP_CAR_32_EPIL_A00_15 (rail 15) position 4 |
| must | AHC | AHC cannot load this item | carrier SMP_CAR_32_EPIS_A00_14 (SMP_CAR_32_EPIS_A00, rail 14) is not a carrier AHC accepts |
| must | AHC | AHC cannot load this item | carrier SMP_CAR_32_EPIL_A00_15 (SMP_CAR_32_EPIL_A00, rail 15) is not a carrier AHC accepts |
| must | AHC | AHC cannot load this item | the 200 uL loaded in proteinase_k has no place in the AHC layout |
| check | fidelity | Held to 31 requirements read from the SOP (Section 1.0 DNA Extraction from Tissue (fresh or snap frozen tissue), steps 1.1 to 1.14) | Every volume and number below is the SOP's. Confirm none is missing. Left out: Section 2.0 DNA Extraction from OCT Blocks (alternative sample type; joins the main procedure at step 1.2); Section 3.0 DNA Extraction from Formalin-fixed Paraffin-embedded Tissue Sections (alternative sample type, xylene deparaffinization and ethanol washes; joins the main procedure at step 1.5); Section 4.0 Quantification and Quality Analysis (spectrophotometry, concentration adjustment, aliquoting and -80°C storage after extraction, reached via step 1.15). |
| check | fidelity | R1 (1.1) place tissue in microcentrifuge tube (1.5 ml): done before or after the run, not in the plan | Place tissue in a 1.5 ml microcentrifuge tube. |
| check | fidelity | R2 (1.1.1) use set tissue amount (spleen or pancreas) (12-15 mg, 25 mg): done before or after the run, not in the plan | Use 12-15 mg spleen or 25 mg pancreas. |
| check | fidelity | R3 (1.1.2) mince tissue with sterile scissors or scalpel: done before or after the run, not in the plan | Mince further with sterile scissors or scalpel to aid digestion. |
| check | manual | Step 18 is done by hand (about 2 min) | Cap sample tubes 1-4, take them off the deck and mix thoroughly by vortexing.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 19 is done by hand (about 240 min) | Incubate sample tubes 1-4 at 56°C in a hybridization oven with moderate rotation until the tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours; if digestion is incomplete, continue 1-2 more hours. Then put the tubes back in their deck positions, uncapped.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 20 is done by hand (about 2 min) | Take sample tubes 1-4 off the deck, vortex each for 15 seconds, then put them back in their deck positions, uncapped.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 28 is done by hand (about 2 min) | Cap sample tubes 1-4, take them off the deck and vortex thoroughly, then put them back in their deck positions, uncapped.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 36 is done by hand (about 2 min) | Cap sample tubes 1-4, take them off the deck and vortex again.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 37 is done by hand (about 5 min) | For each of samples 1-4, place a DNeasy Mini spin column in a 2 ml collection tube and pipette all of the mixture (about 600 µl) into it.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 38 is done by hand (about 3 min) | Centrifuge the spin columns at ≥6000 x g for 1 minute. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 39 is done by hand (about 3 min) | Place each DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to the column.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 40 is done by hand (about 3 min) | Centrifuge for 1 minute at ≥6000 x g. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 41 is done by hand (about 3 min) | Place each DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 42 is done by hand (about 5 min) | Centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. Discard flow-through and collection tube.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 43 is done by hand (about 3 min) | Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | manual | Step 44 is done by hand (about 7 min) | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA.. The robot waits for the operator (AHC asks them with request_manual_step). |
| check | drafting | Assumption made when drafting | 4 samples, one tissue sample per 1.5 ml microcentrifuge tube (sample_1 to sample_4), handled by channels 0-3; the protocol does not say how many samples |
| check | drafting | Assumption made when drafting | Sample tubes sit in a tube rack on the deck and are taken off and put back for vortexing and incubation |
| check | drafting | Assumption made when drafting | Buffer ATL, Buffer AL and 100% ethanol are each loaded into their own small trough so 4 channels can draw at once; proteinase K is loaded into a 1 mL tube to save enzyme and drawn one channel at a time |
| check | drafting | Assumption made when drafting | The library has no labware for DNeasy Mini spin columns or collection tubes, so moving the lysate onto the column (all of the mixture, about 600 µl) and adding Buffer AW1, Buffer AW2 and 1x Tris-EDTA are manual pipetting steps at the protocol's volumes |
| check | drafting | Assumption made when drafting | 300 uL filter tips (on deck) are used for the 180 and 200 uL additions, and 50 uL filter tips for the 20 uL proteinase K additions; the SOP calls for filter tips |
| check | drafting | Assumption made when drafting | Placing, weighing and mincing the tissue (1.1-1.1.2) is done before the run; quantification and storage (1.15, section 4) come after it and are not in the listed requirements |
| check | drafting | Assumption made when drafting | Fresh tips are used for each reagent; the tips touch only the reagent and are dispensed above the tissue |
| check | AHC | AHC's model differs from VENUS | carrier PLT_CAR_L5_DWP_0001: AHC builds PyLabRobot's PLT_CAR_L5_DWP, which differs from VENUS (position 5 y: PyLabRobot 8.2, VENUS 9 (-0.80 mm), and 9 more) |
| check | AHC | AHC's model differs from VENUS | Cos_96_PCR_0002: VENUS's Cos_96_PCR goes to AHC as Cor_96_wellplate_360ul_Fb (AHC has no PCR plate, so it gets the 96-well plate AHC has run on this carrier: on a PLT_CAR_L5_DWP its wells are 0.4 mm off in x, their bottom 0.86 mm higher, 10.67 mm deep where VENUS says 20.5, and 360 uL where VENUS says 290) |
| check | AHC | AHC's model differs from VENUS | Cos_96_PCR_0001: VENUS's Cos_96_PCR goes to AHC as Cor_96_wellplate_360ul_Fb (AHC has no PCR plate, so it gets the 96-well plate AHC has run on this carrier: on a PLT_CAR_L5_DWP its wells are 0.4 mm off in x, their bottom 0.86 mm higher, 10.67 mm deep where VENUS says 20.5, and 360 uL where VENUS says 290) |
| check | AHC | AHC's model differs from VENUS | ethanol: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | al_buffer: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| check | AHC | AHC's model differs from VENUS | atl_buffer: VENUS's RGT_CONT_50ml_A00 goes to AHC as hamilton_1_trough_60mL_Vb (the same Hamilton trough: AHC's model is 19 x 90 mm and 60 mL, VENUS's 20 x 90 mm and 63 mL in 8 connected positions) |
| must | liquid | 'atl_buffer' starts 0.8 mm deep and ends 0.2 mm deep | 1000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'al_buffer' starts 0.8 mm deep and ends 0.2 mm deep | 1000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |
| must | liquid | 'ethanol' starts 0.8 mm deep and ends 0.2 mm deep | 1000 uL spreads thin in this container. Below about 2 mm a tip draws air or misses the liquid; the simulator checks volume, not depth. Load more, or use a narrower container (a tube) for a small volume. |

## What the SOP requires

Each requirement was read from the SOP, and the plan was checked against it: the volumes are the SOP's, for each of 4 sample(s).

| Requirement | How | Steps | uL per sample | From | SOP |
|---|---|---|---|---|---|
| R1 (1.1) place tissue in microcentrifuge tube (1.5 ml) | before or after the run, by hand |  |  |  | Place tissue in a 1.5 ml microcentrifuge tube. |
| R2 (1.1.1) use set tissue amount (spleen or pancreas) (12-15 mg, 25 mg) | before or after the run, by hand |  |  |  | Use 12-15 mg spleen or 25 mg pancreas. |
| R3 (1.1.2) mince tissue with sterile scissors or scalpel | before or after the run, by hand |  |  |  | Mince further with sterile scissors or scalpel to aid digestion. |
| R4 (1.2) add 180 uL of Buffer ATL to each sample | on the robot | 3-6 | 180 | atl_buffer (Buffer ATL (DNeasy Blood & Tissue Kit)) | Add 180 µl Buffer ATL. |
| R5 (1.3) add 20 uL of proteinase K to each sample | on the robot | 13-16 | 20 | proteinase_k (Proteinase K (DNeasy Blood & Tissue Kit)) | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R6 (1.3) mix thoroughly by vortexing | by hand | 18 |  |  | Add 20 µl proteinase K and mix thoroughly by vortexing. |
| R7 (1.4) incubate in hybridization oven with moderate rotation until tissue completely lysed (56 C) | by hand | 19 |  |  | Incubate at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. |
| R8 (1.4.1) vortex well periodically during incubation (30 min) | by hand | 19 |  |  | Vortex well every 30 minutes. |
| R9 (1.4.2) check level of digestion (2 h) | by hand | 19 |  |  | Check level of digestion at 2 hours. |
| R10 (1.4.2) if digestion incomplete, continue incubation (1-2 h) | by hand | 19 |  |  | If digestion is incomplete, continue 1-2 more hours. |
| R11 (1.5) vortex (15 s) | by hand | 20 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R12 (1.5) add 200 uL of Buffer AL to each sample | on the robot | 23-26 | 200 | al_buffer (Buffer AL (DNeasy Blood & Tissue Kit; contains guanidine hydrochloride, do not mix with bleach)) | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R13 (1.5) vortex thoroughly | by hand | 28 |  |  | Vortex 15 seconds, then add 200 µl Buffer AL and vortex thoroughly. |
| R14 (1.6) add 200 uL of 100% ethanol to each sample | on the robot | 31-34 | 200 | ethanol (100% ethanol (molecular biology grade)) | Add 200 µl 100% ethanol and vortex again. |
| R15 (1.6) vortex again | by hand | 36 |  |  | Add 200 µl 100% ethanol and vortex again. |
| R16 (1.7) DNeasy Mini spin column placed in collection tube (2 ml) | by hand | 37 |  |  | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R17 (1.7) add all of the mixture (into the DNeasy Mini spin column) to each sample | by hand | 37 |  |  | Pipette the mixture into a DNeasy Mini spin column placed in a 2 ml collection tube. |
| R18 (1.8) centrifuge (>=6000 x g, 1 min) | by hand | 38 |  |  | Centrifuge at ≥6000 x g for 1 minute. |
| R19 (1.8) discard flow-through and collection tube | by hand | 38 |  |  | Discard flow-through and collection tube. |
| R20 (1.9) place spin column in new collection tube (2 ml) | by hand | 39 |  |  | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R21 (1.9) add 500 uL of Buffer AW1 to each sample | by hand | 39 |  |  | Place the DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to column. |
| R22 (1.10) centrifuge (1 min, >=6000 x g) | by hand | 40 |  |  | Centrifuge for 1 minute at ≥6000 x g. |
| R23 (1.10) discard flow-through and collection tube | by hand | 40 |  |  | Discard flow-through and collection tube. |
| R24 (1.11) place column in new collection tube (2 ml) | by hand | 41 |  |  | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R25 (1.11) add 500 uL of Buffer AW2 to each sample | by hand | 41 |  |  | Place the DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2. |
| R26 (1.12) centrifuge to dry the DNeasy membrane (3 min, 20000 x g) | by hand | 42 |  |  | Centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. |
| R27 (1.12) discard flow-through and collection tube | by hand | 42 |  |  | Discard flow-through and collection tube. |
| R28 (1.13) place spin column in new microcentrifuge tube (1.5 ml) | by hand | 43 |  |  | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R29 (1.13) add 100 uL of 1x Tris-EDTA buffer (to the center of the spin column membrane) to each sample | by hand | 43 |  |  | Place DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane. |
| R30 (1.14) incubate at room temperature (5 min) | by hand | 44 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |
| R31 (1.14) centrifuge to elute DNA (1 min, >=6000 x g) | by hand | 44 |  |  | Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA. |

## Labware and deck

| Name | Type | Where | Holds |
|---|---|---|---|
| tips | STF_L | TIP_CAR_480_A00 at rail 7, position 1 |  |
| tips_small | STF_L | TIP_CAR_480_A00 at rail 7, position 2 |  |
| waste | tip waste | the deck's tip waste |  |
| atl_buffer | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 1 | Buffer ATL (DNeasy Blood & Tissue Kit) |
| proteinase_k | SMP_CAR_32_EPIS_A00 | SMP_CAR_32_EPIS_A00 at rail 14, position 1 | Proteinase K (DNeasy Blood & Tissue Kit) |
| al_buffer | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 2 | Buffer AL (DNeasy Blood & Tissue Kit; contains guanidine hydrochloride, do not mix with bleach) |
| ethanol | RGT_CONT_50ml_A00 | RGT_CAR_5R60_A00 at rail 13, position 3 | 100% ethanol (molecular biology grade) |
| sample_1 | SMP_CAR_32_EPIL_A00 | SMP_CAR_32_EPIL_A00 at rail 15, position 1 |  |
| sample_2 | SMP_CAR_32_EPIL_A00 | SMP_CAR_32_EPIL_A00 at rail 15, position 2 |  |
| sample_3 | SMP_CAR_32_EPIL_A00 | SMP_CAR_32_EPIL_A00 at rail 15, position 3 |  |
| sample_4 | SMP_CAR_32_EPIL_A00 | SMP_CAR_32_EPIL_A00 at rail 15, position 4 |  |

## Reagents

| Labware | Loaded uL | Drawn uL | Left uL |
|---|---|---|---|
| atl_buffer | 1000 | 720 | 280 |
| proteinase_k | 200 | 80 | 120 |
| al_buffer | 1000 | 800 | 200 |
| ethanol | 1000 | 800 | 200 |

## Plate wells

_none_

## Files

- ir: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908.json`
- script: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908_plr.py`
- heal_log: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908_heal_log.json`
- ahc_layout: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908.ahc_layout.yaml`
- summary: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908_summary.md`
- report: `healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908_report.json`
