"""Compiled from protocol: nPOD DNeasy DNA extraction from tissue (lysis reagent additions). Do not edit; recompile from the IR."""
import sys
from pathlib import Path

PLUGIN_ROOT = str(Path(__file__).resolve().parents[3] / 'plugin')  # this repo's precheck (files/dna_extraction/healed/ -> plugin/)
sys.path.insert(0, PLUGIN_ROOT)  # for pipeline.deck and the simulator

from pipeline.deck import reach
from pipeline.pipetting import aspirate, dispense, manual_step, tips_off, tips_on

async def run_protocol(lh, res):
    # step 1: Pick up 4 fresh 300 uL filter tips for Buffer ATL
    await tips_on(lh, [res["tips"].get_item("A1"), res["tips"].get_item("B1"), res["tips"].get_item("C1"), res["tips"].get_item("D1")], use_channels=[0, 1, 2, 3])
    # step 2: Draw 180 uL Buffer ATL into each tip
    await aspirate(lh, [res["atl_buffer"]] * 4, vols=[180.0, 180.0, 180.0, 180.0], use_channels=[0, 1, 2, 3], **reach(res["atl_buffer"], [0, 1, 2, 3]))
    # step 3: Add 180 uL Buffer ATL to sample 1
    await dispense(lh, [res["sample_1"]] * 1, vols=[180.0], use_channels=[0], **reach(res["sample_1"], [0]))
    # step 4: Add 180 uL Buffer ATL to sample 2
    await dispense(lh, [res["sample_2"]] * 1, vols=[180.0], use_channels=[1], **reach(res["sample_2"], [1]))
    # step 5: Add 180 uL Buffer ATL to sample 3
    await dispense(lh, [res["sample_3"]] * 1, vols=[180.0], use_channels=[2], **reach(res["sample_3"], [2]))
    # step 6: Add 180 uL Buffer ATL to sample 4
    await dispense(lh, [res["sample_4"]] * 1, vols=[180.0], use_channels=[3], **reach(res["sample_4"], [3]))
    # step 7: Discard the ATL tips
    await tips_off(lh)
    # step 8: Pick up 4 fresh 50 uL filter tips for proteinase K
    await tips_on(lh, [res["tips_small"].get_item("A1"), res["tips_small"].get_item("B1"), res["tips_small"].get_item("C1"), res["tips_small"].get_item("D1")], use_channels=[0, 1, 2, 3])
    # step 9: Draw 20 uL proteinase K (channel 0)
    await aspirate(lh, [res["proteinase_k"]] * 1, vols=[20.0], use_channels=[0], **reach(res["proteinase_k"], [0]))
    # step 10: Draw 20 uL proteinase K (channel 1)
    await aspirate(lh, [res["proteinase_k"]] * 1, vols=[20.0], use_channels=[1], **reach(res["proteinase_k"], [1]))
    # step 11: Draw 20 uL proteinase K (channel 2)
    await aspirate(lh, [res["proteinase_k"]] * 1, vols=[20.0], use_channels=[2], **reach(res["proteinase_k"], [2]))
    # step 12: Draw 20 uL proteinase K (channel 3)
    await aspirate(lh, [res["proteinase_k"]] * 1, vols=[20.0], use_channels=[3], **reach(res["proteinase_k"], [3]))
    # step 13: Add 20 uL proteinase K to sample 1
    await dispense(lh, [res["sample_1"]] * 1, vols=[20.0], use_channels=[0], **reach(res["sample_1"], [0]))
    # step 14: Add 20 uL proteinase K to sample 2
    await dispense(lh, [res["sample_2"]] * 1, vols=[20.0], use_channels=[1], **reach(res["sample_2"], [1]))
    # step 15: Add 20 uL proteinase K to sample 3
    await dispense(lh, [res["sample_3"]] * 1, vols=[20.0], use_channels=[2], **reach(res["sample_3"], [2]))
    # step 16: Add 20 uL proteinase K to sample 4
    await dispense(lh, [res["sample_4"]] * 1, vols=[20.0], use_channels=[3], **reach(res["sample_4"], [3]))
    # step 17: Discard the proteinase K tips
    await tips_off(lh)
    # step 18: Vortex after adding proteinase K
    await manual_step(lh, 'Cap sample tubes 1-4, take them off the deck and mix thoroughly by vortexing.', empties=[])
    # step 19: Proteinase K lysis at 56°C
    await manual_step(lh, 'Incubate sample tubes 1-4 at 56°C in a hybridization oven with moderate rotation until the tissue is completely lysed. Vortex well every 30 minutes. Check level of digestion at 2 hours; if digestion is incomplete, continue 1-2 more hours. Then put the tubes back in their deck positions, uncapped.', empties=[])
    # step 20: Vortex lysate 15 s before Buffer AL
    await manual_step(lh, 'Take sample tubes 1-4 off the deck, vortex each for 15 seconds, then put them back in their deck positions, uncapped.', empties=[])
    # step 21: Pick up 4 fresh 300 uL filter tips for Buffer AL
    await tips_on(lh, [res["tips"].get_item("A2"), res["tips"].get_item("B2"), res["tips"].get_item("C2"), res["tips"].get_item("D2")], use_channels=[0, 1, 2, 3])
    # step 22: Draw 200 uL Buffer AL into each tip
    await aspirate(lh, [res["al_buffer"]] * 4, vols=[200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3], **reach(res["al_buffer"], [0, 1, 2, 3]))
    # step 23: Add 200 uL Buffer AL to sample 1
    await dispense(lh, [res["sample_1"]] * 1, vols=[200.0], use_channels=[0], **reach(res["sample_1"], [0]))
    # step 24: Add 200 uL Buffer AL to sample 2
    await dispense(lh, [res["sample_2"]] * 1, vols=[200.0], use_channels=[1], **reach(res["sample_2"], [1]))
    # step 25: Add 200 uL Buffer AL to sample 3
    await dispense(lh, [res["sample_3"]] * 1, vols=[200.0], use_channels=[2], **reach(res["sample_3"], [2]))
    # step 26: Add 200 uL Buffer AL to sample 4
    await dispense(lh, [res["sample_4"]] * 1, vols=[200.0], use_channels=[3], **reach(res["sample_4"], [3]))
    # step 27: Discard the AL tips
    await tips_off(lh)
    # step 28: Vortex thoroughly after Buffer AL
    await manual_step(lh, 'Cap sample tubes 1-4, take them off the deck and vortex thoroughly, then put them back in their deck positions, uncapped.', empties=[])
    # step 29: Pick up 4 fresh 300 uL filter tips for ethanol
    await tips_on(lh, [res["tips"].get_item("A3"), res["tips"].get_item("B3"), res["tips"].get_item("C3"), res["tips"].get_item("D3")], use_channels=[0, 1, 2, 3])
    # step 30: Draw 200 uL 100% ethanol into each tip
    await aspirate(lh, [res["ethanol"]] * 4, vols=[200.0, 200.0, 200.0, 200.0], use_channels=[0, 1, 2, 3], **reach(res["ethanol"], [0, 1, 2, 3]))
    # step 31: Add 200 uL 100% ethanol to sample 1
    await dispense(lh, [res["sample_1"]] * 1, vols=[200.0], use_channels=[0], **reach(res["sample_1"], [0]))
    # step 32: Add 200 uL 100% ethanol to sample 2
    await dispense(lh, [res["sample_2"]] * 1, vols=[200.0], use_channels=[1], **reach(res["sample_2"], [1]))
    # step 33: Add 200 uL 100% ethanol to sample 3
    await dispense(lh, [res["sample_3"]] * 1, vols=[200.0], use_channels=[2], **reach(res["sample_3"], [2]))
    # step 34: Add 200 uL 100% ethanol to sample 4
    await dispense(lh, [res["sample_4"]] * 1, vols=[200.0], use_channels=[3], **reach(res["sample_4"], [3]))
    # step 35: Discard the ethanol tips
    await tips_off(lh)
    # step 36: Vortex after ethanol
    await manual_step(lh, 'Cap sample tubes 1-4, take them off the deck and vortex again.', empties=[])
    # step 37: Load lysate onto DNeasy Mini spin columns
    await manual_step(lh, 'For each of samples 1-4, place a DNeasy Mini spin column in a 2 ml collection tube and pipette all of the mixture (about 600 µl) into it.', empties=[])
    # step 38: First spin
    await manual_step(lh, 'Centrifuge the spin columns at ≥6000 x g for 1 minute. Discard flow-through and collection tube.', empties=[])
    # step 39: Buffer AW1 wash
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 2 ml collection tube and add 500 µl Buffer AW1 to the column.', empties=[])
    # step 40: AW1 spin
    await manual_step(lh, 'Centrifuge for 1 minute at ≥6000 x g. Discard flow-through and collection tube.', empties=[])
    # step 41: Buffer AW2 wash
    await manual_step(lh, 'Place each DNeasy column in a new 2 ml collection tube and add 500 µl Buffer AW2.', empties=[])
    # step 42: Dry the membrane
    await manual_step(lh, 'Centrifuge for 3 minutes at 20,000 x g to dry the DNeasy membrane. Discard flow-through and collection tube.', empties=[])
    # step 43: Add elution buffer
    await manual_step(lh, 'Place each DNeasy Mini spin column in a new 1.5 ml microcentrifuge tube and add 100 µl 1x Tris-EDTA buffer to the center of the spin column membrane.', empties=[])
    # step 44: Elute DNA
    await manual_step(lh, 'Incubate at room temperature for 5 minutes and then centrifuge for 1 minute at ≥6000 x g to elute DNA.', empties=[])


# --- Standalone runner: python healed/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908_plr.py --backend chatterbox|star ---
DECK_CONFIG = 'decks/npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908.json'
INITIAL_VOLUMES_UL = {'atl_buffer': 1000, 'proteinase_k': 200, 'al_buffer': 1000, 'ethanol': 1000}


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
