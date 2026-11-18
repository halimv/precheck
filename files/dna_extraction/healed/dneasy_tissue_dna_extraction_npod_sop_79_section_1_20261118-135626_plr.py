"""Compiled from protocol: DNeasy tissue DNA extraction (nPOD SOP-79, section 1.0). Do not edit; recompile from the IR."""
import sys
from pathlib import Path

PLUGIN_ROOT = str(Path(__file__).resolve().parents[3] / 'plugin')  # this repo's precheck (files/dna_extraction/healed/ -> plugin/)
sys.path.insert(0, PLUGIN_ROOT)  # for pipeline.deck and the simulator

from pipeline.pipetting import aspirate, dispense, manual_step, tips_off, tips_on

async def run_protocol(lh, res):
    # step 1: Prepare tissue samples in 1.5 ml tubes
    await manual_step(lh, 'Place tissue in a 1.5 ml microcentrifuge tube for each of the 8 samples. Use 12-15 mg spleen or 25 mg pancreas. Mince further with sterile scissors or scalpel to aid digestion. Put the open tubes in positions A1-H1 of the lysis tube rack on the deck.', empties=[])
    # step 2: Pick up tips for Buffer ATL
    await tips_on(lh, [res["tips_300"].get_item("A1"), res["tips_300"].get_item("B1"), res["tips_300"].get_item("C1"), res["tips_300"].get_item("D1"), res["tips_300"].get_item("E1"), res["tips_300"].get_item("F1"), res["tips_300"].get_item("G1"), res["tips_300"].get_item("H1")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 3: Aspirate 180 uL Buffer ATL
    await aspirate(lh, [res["buffer_atl"]] * 8, vols=[180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 4: Add 180 uL Buffer ATL to each sample
    await dispense(lh, [res["lysis_tubes"].get_item("A1"), res["lysis_tubes"].get_item("B1"), res["lysis_tubes"].get_item("C1"), res["lysis_tubes"].get_item("D1"), res["lysis_tubes"].get_item("E1"), res["lysis_tubes"].get_item("F1"), res["lysis_tubes"].get_item("G1"), res["lysis_tubes"].get_item("H1")], vols=[180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 5: Discard tips
    await tips_off(lh)
    # step 6: Pick up tips for proteinase K
    await tips_on(lh, [res["tips_50"].get_item("A1"), res["tips_50"].get_item("B1"), res["tips_50"].get_item("C1"), res["tips_50"].get_item("D1"), res["tips_50"].get_item("E1"), res["tips_50"].get_item("F1"), res["tips_50"].get_item("G1"), res["tips_50"].get_item("H1")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 7: Drop the unused 50 uL tips mounted in step 6 into waste so 300 uL tips can be mounted for the proteinase K aspiration.
    await tips_off(lh)
    # step 8: Pick up a fresh 300 uL filter tip column (column 5, unused so far) for the 20 uL proteinase K transfer.
    await tips_on(lh, [res["tips_300"].get_item("A5"), res["tips_300"].get_item("B5"), res["tips_300"].get_item("C5"), res["tips_300"].get_item("D5"), res["tips_300"].get_item("E5"), res["tips_300"].get_item("F5"), res["tips_300"].get_item("G5"), res["tips_300"].get_item("H5")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 9: Aspirate 20 uL proteinase K per channel using the 300 uL tips, unchanged volume and reagent.
    await aspirate(lh, [res["proteinase_k"]] * 8, vols=[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 10: Add 20 uL proteinase K to each sample
    await dispense(lh, [res["lysis_tubes"].get_item("A1"), res["lysis_tubes"].get_item("B1"), res["lysis_tubes"].get_item("C1"), res["lysis_tubes"].get_item("D1"), res["lysis_tubes"].get_item("E1"), res["lysis_tubes"].get_item("F1"), res["lysis_tubes"].get_item("G1"), res["lysis_tubes"].get_item("H1")], vols=[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 11: Discard tips
    await tips_off(lh)
    # step 12: Vortex after proteinase K
    await manual_step(lh, 'Cap the tubes, mix thoroughly by vortexing, then return the open tubes to positions A1-H1 on the deck.', empties=[])
    # step 13: Proteinase K lysis at 56 °C
    await manual_step(lh, 'Incubate the capped tubes at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours; if digestion is incomplete, continue 1-2 more hours. Then return the tubes to positions A1-H1 on the deck.', empties=[])
    # step 14: Vortex lysate 15 s
    await manual_step(lh, 'Vortex the capped tubes 15 seconds, then return the open tubes to positions A1-H1 on the deck.', empties=[])
    # step 15: Pick up tips for Buffer AL
    await tips_on(lh, [res["tips_300"].get_item("A2"), res["tips_300"].get_item("B2"), res["tips_300"].get_item("C2"), res["tips_300"].get_item("D2"), res["tips_300"].get_item("E2"), res["tips_300"].get_item("F2"), res["tips_300"].get_item("G2"), res["tips_300"].get_item("H2")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 16: Aspirate 200 uL Buffer AL
    await aspirate(lh, [res["buffer_al"]] * 8, vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 17: Add 200 uL Buffer AL to each sample
    await dispense(lh, [res["lysis_tubes"].get_item("A1"), res["lysis_tubes"].get_item("B1"), res["lysis_tubes"].get_item("C1"), res["lysis_tubes"].get_item("D1"), res["lysis_tubes"].get_item("E1"), res["lysis_tubes"].get_item("F1"), res["lysis_tubes"].get_item("G1"), res["lysis_tubes"].get_item("H1")], vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 18: Discard tips
    await tips_off(lh)
    # step 19: Vortex after Buffer AL
    await manual_step(lh, 'Cap the tubes and vortex thoroughly, then return the open tubes to positions A1-H1 on the deck.', empties=[])
    # step 20: Pick up tips for ethanol
    await tips_on(lh, [res["tips_300"].get_item("A3"), res["tips_300"].get_item("B3"), res["tips_300"].get_item("C3"), res["tips_300"].get_item("D3"), res["tips_300"].get_item("E3"), res["tips_300"].get_item("F3"), res["tips_300"].get_item("G3"), res["tips_300"].get_item("H3")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 21: Aspirate 200 uL 100% ethanol
    await aspirate(lh, [res["ethanol"]] * 8, vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 22: Add 200 uL 100% ethanol to each sample
    await dispense(lh, [res["lysis_tubes"].get_item("A1"), res["lysis_tubes"].get_item("B1"), res["lysis_tubes"].get_item("C1"), res["lysis_tubes"].get_item("D1"), res["lysis_tubes"].get_item("E1"), res["lysis_tubes"].get_item("F1"), res["lysis_tubes"].get_item("G1"), res["lysis_tubes"].get_item("H1")], vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 23: Discard tips
    await tips_off(lh)
    # step 24: Vortex after ethanol
    await manual_step(lh, 'Cap the tubes and vortex again, then return the open tubes to positions A1-H1 on the deck.', empties=[])
    # step 25: Set up spin columns in 2 ml collection tubes
    await manual_step(lh, 'Place 8 DNeasy Mini spin columns, each in a 2 ml collection tube, in positions A1-H1 of the spin column rack on the deck, lids open.', empties=[])
    # step 26: Pick up tips for lysate transfer
    await tips_on(lh, [res["tips_1000"].get_item("A1"), res["tips_1000"].get_item("B1"), res["tips_1000"].get_item("C1"), res["tips_1000"].get_item("D1"), res["tips_1000"].get_item("E1"), res["tips_1000"].get_item("F1"), res["tips_1000"].get_item("G1"), res["tips_1000"].get_item("H1")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 27: Aspirate the whole mixture (600 uL) from each sample tube
    await aspirate(lh, [res["lysis_tubes"].get_item("A1"), res["lysis_tubes"].get_item("B1"), res["lysis_tubes"].get_item("C1"), res["lysis_tubes"].get_item("D1"), res["lysis_tubes"].get_item("E1"), res["lysis_tubes"].get_item("F1"), res["lysis_tubes"].get_item("G1"), res["lysis_tubes"].get_item("H1")], vols=[600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 28: Pipette the mixture into each DNeasy Mini spin column
    await dispense(lh, [res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")], vols=[600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 29: Discard tips
    await tips_off(lh)
    # step 30: Bind DNA to column
    await manual_step(lh, 'Close the spin columns, centrifuge at ≥6000 x g for 1 minute. Discard flow-through and collection tube.', empties=[res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")])
    # step 31: New collection tubes before AW1
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 2 ml collection tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.', empties=[])
    # step 32: Pick up tips for Buffer AW1
    await tips_on(lh, [res["tips_1000"].get_item("A2"), res["tips_1000"].get_item("B2"), res["tips_1000"].get_item("C2"), res["tips_1000"].get_item("D2"), res["tips_1000"].get_item("E2"), res["tips_1000"].get_item("F2"), res["tips_1000"].get_item("G2"), res["tips_1000"].get_item("H2")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 33: Aspirate 500 uL Buffer AW1
    await aspirate(lh, [res["buffer_aw1"]] * 8, vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 34: Add 500 uL Buffer AW1 to each column
    await dispense(lh, [res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")], vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 35: Discard tips
    await tips_off(lh)
    # step 36: AW1 wash spin
    await manual_step(lh, 'Close the spin columns, centrifuge for 1 minute at ≥6000 x g. Discard flow-through and collection tube.', empties=[res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")])
    # step 37: New collection tubes before AW2
    await manual_step(lh, 'Place each DNeasy column in a new 2 ml collection tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.', empties=[])
    # step 38: Pick up tips for Buffer AW2
    await tips_on(lh, [res["tips_1000"].get_item("A3"), res["tips_1000"].get_item("B3"), res["tips_1000"].get_item("C3"), res["tips_1000"].get_item("D3"), res["tips_1000"].get_item("E3"), res["tips_1000"].get_item("F3"), res["tips_1000"].get_item("G3"), res["tips_1000"].get_item("H3")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 39: Aspirate 500 uL Buffer AW2
    await aspirate(lh, [res["buffer_aw2"]] * 8, vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 40: Add 500 uL Buffer AW2 to each column
    await dispense(lh, [res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")], vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 41: Discard tips
    await tips_off(lh)
    # step 42: Dry membrane spin
    await manual_step(lh, 'Close the spin columns, centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. Discard flow-through and collection tube.', empties=[res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")])
    # step 43: Columns into new 1.5 ml elution tubes
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and return them, lids open, to positions A1-H1 of the spin column rack on the deck.', empties=[])
    # step 44: Pick up tips for TE
    await tips_on(lh, [res["tips_300"].get_item("A4"), res["tips_300"].get_item("B4"), res["tips_300"].get_item("C4"), res["tips_300"].get_item("D4"), res["tips_300"].get_item("E4"), res["tips_300"].get_item("F4"), res["tips_300"].get_item("G4"), res["tips_300"].get_item("H4")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 45: Aspirate 100 uL 1x Tris-EDTA
    await aspirate(lh, [res["te_buffer"]] * 8, vols=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 46: Add 100 uL 1x Tris-EDTA buffer to the center of each spin column membrane
    await dispense(lh, [res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")], vols=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 47: Discard tips
    await tips_off(lh)
    # step 48: Elution buffer incubation
    await manual_step(lh, 'Incubate at room temperature for 5 minutes.', empties=[])
    # step 49: Elute DNA
    await manual_step(lh, 'Close the spin columns and centrifuge for 1 minute at ≥6000 x g to elute DNA. Keep the 1.5 ml tubes with the eluted DNA and discard the spin columns.', empties=[res["spin_columns"].get_item("A1"), res["spin_columns"].get_item("B1"), res["spin_columns"].get_item("C1"), res["spin_columns"].get_item("D1"), res["spin_columns"].get_item("E1"), res["spin_columns"].get_item("F1"), res["spin_columns"].get_item("G1"), res["spin_columns"].get_item("H1")])


# --- Standalone runner: python healed/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626_plr.py --backend chatterbox|star ---
DECK_CONFIG = 'decks/dneasy_tissue_dna_extraction_npod_sop_79_section_1_20261118-135626.json'
INITIAL_VOLUMES_UL = {'buffer_atl': 2000, 'proteinase_k': 1000, 'buffer_al': 2500, 'ethanol': 2500, 'buffer_aw1': 5000, 'buffer_aw2': 5000, 'te_buffer': 1200}


def _deck_path(name):
    # A deck config named relative to the working folder this script is in, or to precheck itself.
    for root in (Path(__file__).resolve().parents[1], Path(PLUGIN_ROOT)):
        if (root / name).exists():
            return root / name
    raise FileNotFoundError(f"{name} is in neither this folder nor {PLUGIN_ROOT}")


async def _main(backend_name):
    from pylabrobot.resources import set_tip_tracking, set_volume_tracking
    from pipeline.deck import build_deck, load_deck_config, machines
    from pipeline.instrument import firmware_configuration
    from pipeline.pipetting import close_device, open_device

    set_tip_tracking(True)
    set_volume_tracking(True)
    deck_config = load_deck_config(str(_deck_path(DECK_CONFIG)))
    deck, res = build_deck(deck_config, INITIAL_VOLUMES_UL)
    lh = await open_device(deck, backend_name, firmware_configuration(deck_config))
    for machine in machines(res):
        await machine.setup()
    try:
        await run_protocol(lh, res)
    finally:
        for machine in machines(res):
            await machine.stop()
        await close_device(lh)


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["chatterbox", "star"], default="chatterbox")
    args = parser.parse_args()
    if args.backend == "star":
        answer = input("Run on the real STARlet? The deck must match the setup checklist "
                       "(demo/server.py -> Execute). Type 'run' to continue: ")
        if answer.strip().lower() != "run":
            sys.exit("Not run.")
        from pipeline.pipetting import set_manual_handler

        # A step the robot cannot do waits here until the operator has done it by hand.
        set_manual_handler(lambda instruction: input(f"\nMANUAL STEP (the robot waits): {instruction}\n"
                                                     "Press Enter once it is done: "))
    asyncio.run(_main(args.backend))
