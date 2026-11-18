"""Plate wells as starting liquids: initial_volumes_ul {"<plate>:A1:H1": uL per well}, AHC's target form."""
import json
from pathlib import Path

from pipeline.ahc_export import load_ahc_types, to_ahc_layout
from pipeline.deck import build_deck, loaded_wells
from pipeline.design_review import trace_mixtures
from pipeline.stage0_drafter import structural_errors

DECK = json.loads((Path(__file__).parent / "fixtures" / "serial_deck.json").read_text())


def test_keys_name_wells():
    assert loaded_wells("p:A1:H1") == ("p", [(1, r) for r in range(8)])
    assert loaded_wells("p:B3") == ("p", [(3, 1)])
    assert loaded_wells("p:col12")[1][-1] == (12, 7)
    assert loaded_wells("p:A1:B2") == ("p", [(1, 0), (1, 1), (2, 0), (2, 1)])
    assert loaded_wells("diluent") is None and loaded_wells("p:Z1") is None and loaded_wells("p:A13") is None


def test_build_deck_fills_each_well():
    _, res = build_deck(DECK, {"dilution_plate:A2:H2": 40, "diluent": 5000})
    plate = res["dilution_plate"]
    assert all(plate.get_item(f"{r}2").tracker.get_used_volume() == 40 for r in "ABCDEFGH")
    assert plate.get_item("A1").tracker.get_used_volume() == 0


def test_trace_and_drafter_and_ahc_export():
    ir = {"labware": {"tips": {"kind": "tip_rack"}, "dilution_plate": {"kind": "plate", "wells": 96},
                      "waste": {"kind": "waste"}},
          "reagents": {"dilution_plate": "stocks"},
          "initial_volumes_ul": {"dilution_plate:A2:H2": 40},
          "steps": [{"step": 1, "action": "tips_on", "labware": "tips", "column": 1, "channels": [0]},
                    {"step": 2, "action": "aspirate", "labware": "dilution_plate", "column": 2, "volume_ul": 10,
                     "channels": [0]},
                    {"step": 3, "action": "dispense", "labware": "dilution_plate", "column": 3, "volume_ul": 10,
                     "channels": [0]},
                    {"step": 4, "action": "tips_off", "labware": "waste", "channels": [0]}]}
    where, _ = trace_mixtures(ir, {"dilution_plate": "plate"})
    assert where[("dilution_plate", 3, 0)] == {"stocks": 10.0} and where[("dilution_plate", 2, 0)] == {"stocks": 30.0}
    assert not [e for e in structural_errors(ir) if "initial_volumes_ul" in e]
    bad = {**ir, "initial_volumes_ul": {"tips:A1": 5}}
    assert any("not a plate" in e for e in structural_errors(bad))
    layout, problems, _ = to_ahc_layout(DECK, load_ahc_types(), ir["initial_volumes_ul"])
    assert layout["liquids"] == {"dilution_plate:A2:H2": 40} and not [p for p in problems if "dilution_plate" in p]
