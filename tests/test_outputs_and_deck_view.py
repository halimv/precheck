"""Any protocol's output, the deck view the pages draw, and precheck alone (PyLabRobot's catalog).

Fixtures: tests/fixtures/serial_passing.json (a dilution series on a plate) and files/dna_extraction/ (an nPOD DNA
extraction: one version ends with spin columns centrifuged off the deck, the other with four sample tubes)."""
import json
import warnings
from pathlib import Path

import pytest

from pipeline import deck_builder, plr_catalog
from pipeline.deck import INSTRUMENT_DECK, ROOT, build_deck, load_deck_config
from pipeline.deck_view import deck_view, image_for
from pipeline.design_review import review
from pipeline.summary import review_items

warnings.simplefilter("ignore")
REPO = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
DNA = REPO / "files" / "dna_extraction"
FULL = "dneasy_dna_extraction_from_tissue_npod_sop_79_sect_20261118-124823"
TUBES = "npod_dneasy_dna_extraction_from_tissue_lysis_reage_20261118-124908"


def dna(stem):
    protocol = json.loads((DNA / "healed" / f"{stem}.json").read_text())
    return protocol, load_deck_config(str(DNA / protocol["deck_config"]))


def serial():
    return json.loads((FIXTURES / "serial_passing.json").read_text()), json.loads((FIXTURES / "serial_deck.json").read_text())


# --- the output ---

def test_a_dilution_series_output_is_its_plate_and_reads_as_a_series():
    r = review(*serial())
    assert [o["labware"] for o in r["outputs"]] == ["dilution_plate"]
    assert len(r["outputs"][0]["wells"]) == 48 and r["series"]


def test_an_output_taken_off_the_deck_by_hand_is_what_it_held_just_before():
    r = review(*dna(FULL))
    (out,) = r["outputs"]
    assert out["labware"] == "spin_column_rack" and "elute" in out["leaves_deck"]
    assert [w["well"] for w in out["wells"]] == [f"{row}1" for row in "ABCDEFGH"]
    assert all(w["ul"] == 100 for w in out["wells"]) and not r["series"]


def test_sample_tubes_are_the_output_in_order_and_reagent_sources_are_not():
    r = review(*dna(TUBES))
    assert [o["labware"] for o in r["outputs"]] == ["sample_1", "sample_2", "sample_3", "sample_4"]
    assert all(o["total_ul"] == 600 for o in r["outputs"])


def test_the_protocol_can_name_its_output():
    protocol, deck = serial()
    protocol["outputs"] = ["dilution_plate"]
    (out,) = review(protocol, deck)["outputs"]
    assert out["named_by_protocol"]


# --- the deck view ---

def _report(protocol, deck, target="lab"):
    r = {"review": review(protocol, deck), "target": target, "suggestions": [], "ahc": {"not_on_layout": []}}
    r["needs_review"] = [{"severity": "must", "area": "liquid", "item": "'buffer_atl' starts 1.6 mm deep and ends 0.4 mm deep",
                          "detail": "Below about 2 mm a tip draws air."},
                         {"severity": "must", "area": "AHC", "item": "AHC cannot load this item",
                          "detail": "spin_column_rack (HAM_DWP_96x08mL) on PLT_CAR_L5_DWP_0001 is not labware AHC accepts"}]
    return r


def test_the_deck_view_marks_problems_red_assumptions_yellow_and_the_output():
    protocol, deck = dna(FULL)
    view = deck_view(protocol, deck, _report(protocol, deck))
    items = {i["id"]: i for c in view["carriers"] for i in c["labware"]}
    assert items["buffer_atl"]["status"] == "issue" and items["spin_column_rack"]["status"] == "issue"
    assert items["spin_column_rack"]["role"] == "output" and items["buffer_al"]["role"] == "source"
    assert items["tips_300"]["role"] == "tips" and items["tips_300"]["status"] == "used"
    assert any("spin column" in a.lower() for a in items["spin_column_rack"]["assumptions"])
    assert view["general_assumptions"]  # "Filter tips are used throughout" names no one labware
    carrier = next(c for c in view["carriers"] if any(i["id"] == "buffer_atl" for i in c["labware"]))
    assert carrier["status"] == "issue"


def test_every_kind_of_labware_has_a_photo_with_its_license():
    for type_name, kind in [("TIP_CAR_480_A00", "carrier"), ("STF_L", "tip_rack"), ("Cos_96_PCR", "plate"),
                            ("RGT_CONT_50ml_A00", "container"), ("cor_falcon_tube_15mL_Vb", "container"),
                            ("Eppendorf_DNA_LoBind_1_5ml_Vb", "container")]:
        image = image_for(type_name, kind)
        assert image and image["src"].startswith("https://commons.wikimedia.org/") and image["license"]
    assert "trough" in image_for("RGT_CONT_50ml_A00", "container")["name"].lower()  # not a 50 mL tube


# --- precheck alone: PyLabRobot's catalog ---

def test_the_plr_catalog_offers_hamilton_labware_with_conservative_volumes():
    entries = plr_catalog.catalog()
    kinds = {e["kind"] for e in entries}
    assert {"carrier", "tip_rack", "plate", "reservoir", "tube_rack"} <= kinds
    by = {e["venus_type"]: e for e in entries}
    assert by["eppendorf_96_wellplate_500ul_Vb"]["capacity_ul"] <= 500  # sold as 500 uL, whatever the geometry
    assert all(e["venus_type"].startswith("hamilton_96_tiprack_") for e in entries if e["kind"] == "tip_rack")


def test_precheck_alone_builds_a_deck_from_pylabrobot_on_an_empty_star_deck():
    protocol, _ = dna(FULL)
    base = plr_catalog.starting_deck(INSTRUMENT_DECK, "plr")
    assert base["catalog"] == "plr" and not base["carriers"]
    resolution = deck_builder.resolve(protocol["labware"], base, name="dna")
    assert resolution.ok, resolution.unresolved
    assert resolution.deck_config["catalog"] == "plr"
    assert all(c.get("build") != "venus" for c in resolution.deck_config["carriers"])
    build_deck(resolution.deck_config)


def test_a_tube_need_goes_on_a_pylabrobot_tube_carrier():
    base = plr_catalog.base_deck(load_deck_config(str(ROOT / INSTRUMENT_DECK)))
    needs = {"tips": {"kind": "tip_rack", "tip_volume_ul": 1000}, "sample": {"kind": "tube", "min_capacity_ul": 10000},
             "waste": {"kind": "waste"}}
    resolution = deck_builder.resolve(needs, base)
    assert resolution.ok, resolution.unresolved
    spec = resolution.deck_config["labware"]["sample"]
    carrier = next(c for c in resolution.deck_config["carriers"] if c["name"] == spec["carrier"])
    tube = next(e for e in plr_catalog.catalog() if e["venus_type"] == spec["factory"])
    assert tube["kind"] == "tube_rack" and tube["capacity_ul"] >= 10000
    assert carrier["factory"].lower().startswith(("tube_car", "hamilton_tube_carrier"))
    build_deck(resolution.deck_config, {"sample": 5000})


def test_a_revision_keeps_the_target_of_the_protocol_it_revises(tmp_path, monkeypatch):
    from pipeline import paths
    monkeypatch.setattr(paths, "WORK", tmp_path)
    (tmp_path / "decks").mkdir()
    (tmp_path / "decks" / "d.json").write_text(json.dumps({**plr_catalog.starting_deck(INSTRUMENT_DECK, "plr")}))
    assert plr_catalog.starting_deck(INSTRUMENT_DECK, "lab", {"deck_config": "decks/d.json"})["catalog"] == "plr"


def test_precheck_alone_does_not_ask_for_ahc():
    protocol, deck = dna(FULL)
    r = review(protocol, deck)
    ahc = {"not_on_layout": ["lysis_plate is not labware AHC accepts"], "differs_from_venus": ["carrier differs"]}
    lab = review_items(protocol, [], r, [], ahc, target="lab")
    alone = review_items(protocol, [], r, [], ahc, target="plr")
    assert any(i["area"] == "AHC" for i in lab) and not any(i["area"] == "AHC" for i in alone)
