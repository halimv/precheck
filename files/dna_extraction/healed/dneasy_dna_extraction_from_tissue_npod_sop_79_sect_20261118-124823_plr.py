"""Compiled from protocol: DNeasy DNA extraction from tissue (nPOD SOP-79, section 1.0). Do not edit; recompile from the IR."""
import sys
from pathlib import Path

PLUGIN_ROOT = str(Path(__file__).resolve().parents[3] / 'plugin')  # this repo's precheck (files/dna_extraction/healed/ -> plugin/)
sys.path.insert(0, PLUGIN_ROOT)  # for pipeline.deck and the simulator

from pipeline.deck import reach
from pipeline.pipetting import aspirate, dispense, manual_step, tips_off, tips_on

async def run_protocol(lh, res):
    # step 1: Load minced tissue samples
    await manual_step(lh, 'Use 12-15 mg spleen or 25 mg pancreas per sample. Mince further with sterile scissors or scalpel to aid digestion. Place each tissue sample in its 1.5 ml well (A1-H1) of the lysis plate, standing in for a 1.5 ml microcentrifuge tube, and put the plate on the deck.', empties=[])
    # step 2: Pick up tips for Buffer ATL
    await tips_on(lh, [res["tips_300"].get_item("A1"), res["tips_300"].get_item("B1"), res["tips_300"].get_item("C1"), res["tips_300"].get_item("D1"), res["tips_300"].get_item("E1"), res["tips_300"].get_item("F1"), res["tips_300"].get_item("G1"), res["tips_300"].get_item("H1")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 3: Aspirate 180 µL Buffer ATL
    await aspirate(lh, [res["buffer_atl"]] * 8, vols=[180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["buffer_atl"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 4: Add 180 µL Buffer ATL to each sample
    await dispense(lh, [res["lysis_plate"].get_item("A1"), res["lysis_plate"].get_item("B1"), res["lysis_plate"].get_item("C1"), res["lysis_plate"].get_item("D1"), res["lysis_plate"].get_item("E1"), res["lysis_plate"].get_item("F1"), res["lysis_plate"].get_item("G1"), res["lysis_plate"].get_item("H1")], vols=[180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 5: Discard tips
    await tips_off(lh)
    # step 6: Pick up tips for proteinase K
    await tips_on(lh, [res["tips_300"].get_item("A2"), res["tips_300"].get_item("B2"), res["tips_300"].get_item("C2"), res["tips_300"].get_item("D2"), res["tips_300"].get_item("E2"), res["tips_300"].get_item("F2"), res["tips_300"].get_item("G2"), res["tips_300"].get_item("H2")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 7: Aspirate 20 µL proteinase K
    await aspirate(lh, [res["proteinase_k"]] * 8, vols=[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["proteinase_k"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 8: Add 20 µL proteinase K to each sample
    await dispense(lh, [res["lysis_plate"].get_item("A1"), res["lysis_plate"].get_item("B1"), res["lysis_plate"].get_item("C1"), res["lysis_plate"].get_item("D1"), res["lysis_plate"].get_item("E1"), res["lysis_plate"].get_item("F1"), res["lysis_plate"].get_item("G1"), res["lysis_plate"].get_item("H1")], vols=[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 9: Discard tips
    await tips_off(lh)
    # step 10: Vortex after proteinase K
    await manual_step(lh, 'Seal the lysis plate and mix thoroughly by vortexing.', empties=[])
    # step 11: Proteinase K digestion at 56°C
    await manual_step(lh, 'Incubate at 56°C in a hybridization oven with moderate rotation until tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours. If digestion is incomplete, continue 1-2 more hours.', empties=[])
    # step 12: Vortex lysate 15 s
    await manual_step(lh, 'Vortex 15 seconds, unseal the plate and return it to the deck.', empties=[])
    # step 13: Pick up tips for Buffer AL
    await tips_on(lh, [res["tips_300"].get_item("A3"), res["tips_300"].get_item("B3"), res["tips_300"].get_item("C3"), res["tips_300"].get_item("D3"), res["tips_300"].get_item("E3"), res["tips_300"].get_item("F3"), res["tips_300"].get_item("G3"), res["tips_300"].get_item("H3")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 14: Aspirate 200 µL Buffer AL
    await aspirate(lh, [res["buffer_al"]] * 8, vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["buffer_al"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 15: Add 200 µL Buffer AL to each sample
    await dispense(lh, [res["lysis_plate"].get_item("A1"), res["lysis_plate"].get_item("B1"), res["lysis_plate"].get_item("C1"), res["lysis_plate"].get_item("D1"), res["lysis_plate"].get_item("E1"), res["lysis_plate"].get_item("F1"), res["lysis_plate"].get_item("G1"), res["lysis_plate"].get_item("H1")], vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 16: Discard tips
    await tips_off(lh)
    # step 17: Vortex after Buffer AL
    await manual_step(lh, 'Seal the plate, vortex thoroughly, unseal and return it to the deck.', empties=[])
    # step 18: Pick up tips for ethanol
    await tips_on(lh, [res["tips_300"].get_item("A4"), res["tips_300"].get_item("B4"), res["tips_300"].get_item("C4"), res["tips_300"].get_item("D4"), res["tips_300"].get_item("E4"), res["tips_300"].get_item("F4"), res["tips_300"].get_item("G4"), res["tips_300"].get_item("H4")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 19: Aspirate 200 µL 100% ethanol
    await aspirate(lh, [res["ethanol"]] * 8, vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["ethanol"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 20: Add 200 µL 100% ethanol to each sample
    await dispense(lh, [res["lysis_plate"].get_item("A1"), res["lysis_plate"].get_item("B1"), res["lysis_plate"].get_item("C1"), res["lysis_plate"].get_item("D1"), res["lysis_plate"].get_item("E1"), res["lysis_plate"].get_item("F1"), res["lysis_plate"].get_item("G1"), res["lysis_plate"].get_item("H1")], vols=[200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 21: Discard tips
    await tips_off(lh)
    # step 22: Vortex after ethanol
    await manual_step(lh, 'Seal the plate, vortex again, unseal and return it to the deck.', empties=[])
    # step 23: Set up spin columns in 2 ml collection tubes
    await manual_step(lh, 'Place a DNeasy Mini spin column in a 2 ml collection tube at each of positions A1-H1 of the spin column rack, open the lids and put the rack on the deck.', empties=[])
    # step 24: Pick up tips for the lysate transfer
    await tips_on(lh, [res["tips_1000"].get_item("A1"), res["tips_1000"].get_item("B1"), res["tips_1000"].get_item("C1"), res["tips_1000"].get_item("D1"), res["tips_1000"].get_item("E1"), res["tips_1000"].get_item("F1"), res["tips_1000"].get_item("G1"), res["tips_1000"].get_item("H1")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 25: Aspirate all of the mixture (600 µL) from each sample
    await aspirate(lh, [res["lysis_plate"].get_item("A1"), res["lysis_plate"].get_item("B1"), res["lysis_plate"].get_item("C1"), res["lysis_plate"].get_item("D1"), res["lysis_plate"].get_item("E1"), res["lysis_plate"].get_item("F1"), res["lysis_plate"].get_item("G1"), res["lysis_plate"].get_item("H1")], vols=[600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 26: Pipette the mixture into each DNeasy Mini spin column
    await dispense(lh, [res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")], vols=[600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 27: Discard tips
    await tips_off(lh)
    # step 28: Centrifuge lysate through the columns
    await manual_step(lh, 'Close the spin columns and centrifuge at ≥6000 x g for 1 minute.', empties=[res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")])
    # step 29: Discard flow-through
    await manual_step(lh, 'Discard flow-through and collection tube.', empties=[])
    # step 30: New collection tubes for the AW1 wash
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 2 ml collection tube at positions A1-H1, open the lids and return the rack to the deck.', empties=[])
    # step 31: Pick up tips for Buffer AW1
    await tips_on(lh, [res["tips_1000"].get_item("A2"), res["tips_1000"].get_item("B2"), res["tips_1000"].get_item("C2"), res["tips_1000"].get_item("D2"), res["tips_1000"].get_item("E2"), res["tips_1000"].get_item("F2"), res["tips_1000"].get_item("G2"), res["tips_1000"].get_item("H2")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 32: Aspirate 500 µL Buffer AW1
    await aspirate(lh, [res["buffer_aw1"]] * 8, vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["buffer_aw1"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 33: Add 500 µL Buffer AW1 to each column
    await dispense(lh, [res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")], vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 34: Discard tips
    await tips_off(lh)
    # step 35: Centrifuge AW1 wash
    await manual_step(lh, 'Close the spin columns and centrifuge for 1 minute at ≥6000 x g.', empties=[res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")])
    # step 36: Discard AW1 flow-through
    await manual_step(lh, 'Discard flow-through and collection tube.', empties=[])
    # step 37: New collection tubes for the AW2 wash
    await manual_step(lh, 'Place each DNeasy column in a new 2 ml collection tube at positions A1-H1, open the lids and return the rack to the deck.', empties=[])
    # step 38: Pick up tips for Buffer AW2
    await tips_on(lh, [res["tips_1000"].get_item("A3"), res["tips_1000"].get_item("B3"), res["tips_1000"].get_item("C3"), res["tips_1000"].get_item("D3"), res["tips_1000"].get_item("E3"), res["tips_1000"].get_item("F3"), res["tips_1000"].get_item("G3"), res["tips_1000"].get_item("H3")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 39: Aspirate 500 µL Buffer AW2
    await aspirate(lh, [res["buffer_aw2"]] * 8, vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["buffer_aw2"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 40: Add 500 µL Buffer AW2 to each column
    await dispense(lh, [res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")], vols=[500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 41: Discard tips
    await tips_off(lh)
    # step 42: Dry the membrane
    await manual_step(lh, 'Close the spin columns and centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane.', empties=[res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")])
    # step 43: Discard AW2 flow-through
    await manual_step(lh, 'Discard flow-through and collection tube.', empties=[])
    # step 44: Transfer columns to 1.5 ml elution tubes
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube at positions A1-H1, open the lids and return the rack to the deck.', empties=[])
    # step 45: Pick up tips for TE buffer
    await tips_on(lh, [res["tips_300"].get_item("A5"), res["tips_300"].get_item("B5"), res["tips_300"].get_item("C5"), res["tips_300"].get_item("D5"), res["tips_300"].get_item("E5"), res["tips_300"].get_item("F5"), res["tips_300"].get_item("G5"), res["tips_300"].get_item("H5")], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 46: Aspirate 100 µL 1x Tris-EDTA
    await aspirate(lh, [res["te_buffer"]] * 8, vols=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7], **reach(res["te_buffer"], [0, 1, 2, 3, 4, 5, 6, 7]))
    # step 47: Add 100 µL 1x Tris-EDTA to the center of each spin column membrane
    await dispense(lh, [res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")], vols=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], use_channels=[0, 1, 2, 3, 4, 5, 6, 7])
    # step 48: Discard tips
    await tips_off(lh)
    # step 49: Room-temperature incubation before elution
    await manual_step(lh, 'Incubate at room temperature for 5 minutes.', empties=[])
    # step 50: Elute DNA
    await manual_step(lh, 'Close the spin columns and centrifuge for 1 minute at ≥6000 x g to elute DNA. Keep the 1.5 ml tubes containing the eluted DNA.', empties=[res["spin_column_rack"].get_item("A1"), res["spin_column_rack"].get_item("B1"), res["spin_column_rack"].get_item("C1"), res["spin_column_rack"].get_item("D1"), res["spin_column_rack"].get_item("E1"), res["spin_column_rack"].get_item("F1"), res["spin_column_rack"].get_item("G1"), res["spin_column_rack"].get_item("H1")])


# --- Standalone runner: python healed/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823_plr.py --backend chatterbox|star ---
DECK_CONFIG = 'decks/dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823.json'
INITIAL_VOLUMES_UL = {'buffer_atl': 2000, 'proteinase_k': 500, 'buffer_al': 2000, 'ethanol': 2000, 'buffer_aw1': 4500, 'buffer_aw2': 4500, 'te_buffer': 1100}


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
