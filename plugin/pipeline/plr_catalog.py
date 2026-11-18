"""PyLabRobot's own labware catalog, for precheck alone (no lab, no VENUS library).

The lab mode builds a deck from VENUS's library: the labware this lab owns, on the deck that is on its STARlet, so
AHC can run it. Precheck alone builds it from what PyLabRobot ships for the Hamilton STAR instead: every Hamilton tip
rack, 96-well plate, trough and tube PyLabRobot has a model of, on Hamilton carriers PyLabRobot can place. A protocol
checked this way is checked on a real STAR model with real labware geometry, but not on any particular lab's deck.

Entries have the shape deck_builder's VENUS catalog has (`venus_type` is the PyLabRobot factory name, `build` is
"plr"), so the deck builder resolves needs from either one the same way. Carriers say what their sites hold (`holds`),
since PyLabRobot's tip-carrier sites are smaller than the racks they take. A tube is offered once, on the tube carrier
whose sites fit it best (`carrier_factory`).
"""

import functools
import inspect
import re
import warnings
from typing import Any, Dict, List, Optional, Tuple

RAIL_MM = 22.5
CARRIER_NAMES = re.compile(r"^(PLT_CAR|TIP_CAR|Trough_CAR|Tube_CAR|hamilton_tube_carrier)", re.IGNORECASE)
TIP_RACKS = re.compile(r"^hamilton_96_tiprack_", re.IGNORECASE)  # the STAR picks up Hamilton CO-RE tips only
CATEGORY = {"tip_rack": "Tip carriers", "plate": "Plate carriers", "reservoir": "Reagent carriers", "tube": "Tube carriers"}
TUBE_FIT_MM = (2.5, 1.5)  # a tube fits a site up to this much narrower, or this much wider (a sprung clip)


def _factories() -> List[Tuple[str, Any]]:
    import pylabrobot.resources as plr

    out = []
    for name in sorted(dir(plr)):
        fn = getattr(plr, name)
        if name.startswith("_") or not inspect.isfunction(fn):
            continue
        try:
            if list(inspect.signature(fn).parameters)[:1] != ["name"]:
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                out.append((name, fn(name="x")))
        except Exception:  # noqa: BLE001  factories that need more than a name are not deck labware
            continue
    return out


def _capacity(name: str, geometric: float) -> float:
    """A well's or container's volume: PyLabRobot's, from its geometry, but never more than the volume the product
    is sold as when its factory name says it ("eppendorf_96_wellplate_500ul_Vb": 500 uL, though the geometry holds
    more)."""
    m = re.search(r"(\d+(?:[._]\d+)?)\s*(ul|ml)(?![a-z])", name, re.IGNORECASE)
    if not m:
        return round(geometric, 1)
    nominal = float(m.group(1).replace("_", ".")) * (1000.0 if m.group(2).lower() == "ml" else 1.0)
    return round(min(geometric, nominal), 1)


def _entry(name: str, kind: str, resource: Any, **extra: Any) -> Dict[str, Any]:
    return {"venus_type": name, "venus_file": None, "category": extra.pop("category", ""), "kind": kind,
            "description": extra.pop("description", ""), "barcode": "", "part_number": None, "checked": True,
            "size": [round(resource.get_size_x(), 2), round(resource.get_size_y(), 2), round(resource.get_size_z(), 2)],
            "factory": name, "build": "plr", **extra}


@functools.lru_cache(maxsize=1)
def _catalog() -> Tuple[Dict[str, Any], ...]:
    from pylabrobot.resources import Plate, TipRack, Trough, Tube
    from pylabrobot.resources.carrier import PlateCarrier, TipCarrier, TroughCarrier, TubeCarrier

    from pipeline.setup_guide import nominal_tip_ul

    made = _factories()
    entries: List[Dict[str, Any]] = []
    tube_carriers = []
    for name, r in made:
        holds = next((k for cls, k in ((TipCarrier, "tip_rack"), (PlateCarrier, "plate"), (TroughCarrier, "reservoir"),
                                       (TubeCarrier, "tube")) if isinstance(r, cls)), None)
        if holds and CARRIER_NAMES.match(name):
            sites = [{"position": len(r.sites) - i, "dx": round(r.sites[i].get_size_x(), 2),
                      "dy": round(r.sites[i].get_size_y(), 2), "holds": holds} for i in sorted(r.sites)]  # front first
            entries.append(_entry(name, "carrier", r, category=CATEGORY[holds], sites=sites, holds=holds,
                                  tracks=max(1, round(r.get_size_x() / RAIL_MM)), label=None,
                                  description=f"PyLabRobot {CATEGORY[holds][:-1].lower()}, {len(sites)} sites"))
            if holds == "tube":
                tube_carriers.append(entries[-1])
        elif isinstance(r, TipRack) and TIP_RACKS.match(name):
            tip = r.get_item("A1").get_tip()
            entries.append(_entry(name, "tip_rack", r, tip_volume_ul=nominal_tip_ul(name, tip.maximal_volume),
                                  filter=bool(tip.has_filter), description="PyLabRobot Hamilton tip rack"))
        elif isinstance(r, Plate) and r.num_items == 96 and "lid" not in name.lower():
            entries.append(_entry(name, "plate", r, capacity_ul=_capacity(name, r.get_item("A1").max_volume), rows=8,
                                  columns=12, description="PyLabRobot 96-well plate"))
        elif isinstance(r, Trough):
            entries.append(_entry(name, "reservoir", r, capacity_ul=_capacity(name, r.max_volume), rows=1, columns=1,
                                  channels_at_once=max(1, min(8, int(r.get_size_y() // 9))),
                                  description="PyLabRobot trough"))
    for name, r in made:  # a tube, on the tube carrier whose sites fit it best
        if not isinstance(r, Tube):
            continue
        best: Optional[Tuple[float, Dict[str, Any]]] = None
        for c in tube_carriers:
            site = c["sites"][0]["dx"]
            if site - TUBE_FIT_MM[0] <= r.get_size_x() <= site + TUBE_FIT_MM[1]:
                gap = abs(site - r.get_size_x())
                if best is None or gap < best[0]:
                    best = (gap, c)
        if best:
            c = best[1]
            entries.append(_entry(name, "tube_rack", r, capacity_ul=_capacity(name, r.max_volume), rows=1, columns=1,
                                  carrier_factory=c["venus_type"], positions=len(c["sites"]), tracks=c["tracks"],
                                  description=f"PyLabRobot tube, in a {c['venus_type']}"))
    return tuple(entries)


def catalog() -> List[Dict[str, Any]]:
    """Every Hamilton carrier, tip rack, 96-well plate, trough and tube PyLabRobot has a model of."""
    return list(_catalog())


def site_fits(site: Dict[str, Any], entry: Dict[str, Any]) -> bool:
    """A PyLabRobot carrier's site takes labware of the kind it holds; a plate or trough must also match its
    footprint (tip racks sit over a smaller holder)."""
    want = {"tip_rack": "tip_rack", "plate": "plate", "reservoir": "reservoir"}.get(entry["kind"])
    if site.get("holds") != want:
        return False
    if want == "tip_rack":
        return True
    return abs(site["dx"] - entry["size"][0]) <= 2.0 and abs(site["dy"] - entry["size"][1]) <= 2.0


def base_deck(lab_deck: Dict[str, Any]) -> Dict[str, Any]:
    """An empty STAR deck of the lab's instrument (its rails and tip waste, nothing on it): what precheck alone
    builds on. The deck config says its catalog is PyLabRobot's, so revisions build from the same one."""
    trash = {lid: spec for lid, spec in lab_deck["labware"].items() if spec["kind"] == "trash"}
    return {"description": "An empty STAR deck: precheck alone builds the protocol's deck from PyLabRobot's catalog.",
            "deck": lab_deck["deck"], "instrument": lab_deck.get("instrument"), "source": {"catalog": "pylabrobot"},
            "carriers": [], "labware": trash, "catalog": "plr"}


TARGETS = ("lab", "plr")  # precheck with the lab's labware (and AHC), or precheck alone on PyLabRobot's catalog


def starting_deck(deck_file: str, target: str = "lab", previous: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """The deck a draft is built on: the lab's (the instrument's .lay, `deck_file`) or, for precheck alone, an empty
    STAR deck filled from PyLabRobot's catalog. A revision keeps the target of the protocol it revises
    (`previous`)."""
    from pipeline.deck import ROOT, deck_config_for, load_deck_config

    if previous is not None:
        try:
            target = "plr" if deck_config_for(previous, ROOT).get("catalog") == "plr" else "lab"
        except Exception:  # noqa: BLE001  its deck file is gone: keep the target asked for
            pass
    if target not in TARGETS:
        raise ValueError(f"target must be one of {', '.join(TARGETS)}")
    lab = load_deck_config(str(ROOT / deck_file))
    return base_deck(lab) if target == "plr" else lab


def target_of(deck_config: Dict[str, Any]) -> str:
    return "plr" if deck_config.get("catalog") == "plr" else "lab"
