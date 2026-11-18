"""The deck as the scientist reviews it: every carrier on its rails, the labware in its sites, and what to look at.

`deck_view` is what the Check and Execute pages draw. Each labware says its role in the protocol (tips, a source
loaded before the run, the output, an intermediate, waste), what it holds, the drafting assumptions that are about it
(drawn yellow) and the potential problems found with it (drawn red: liquid too shallow for a tip, a well over its fill
limit, labware AHC cannot load), and a photo of that kind of labware with a link to the product
(config/labware_images.json). Assumptions that name no labware are listed under the deck.

Matching an assumption or a problem to labware is by text: the labware's ID ("spin_column_rack" also matches "spin
column"), the reagent it holds ("Proteinase K"), or its type. It is a reading aid, not a check.
"""

import functools
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

from pipeline.deck import ROOT, build_deck, loaded_wells
from pipeline.venus_layout import RAIL_MM

GENERIC = {"plate", "plates", "rack", "racks", "tip", "tips", "buffer", "the", "reagent", "container", "trough",
           "tube", "tubes", "carrier", "small", "large", "well", "wells", "uL", "ul", "ml", "mL", "and", "of"}
SKIP_AREAS = {"deck", "run", "fidelity", "manual", "drafting", "repair"}  # "must" items that are not about labware


@functools.lru_cache(maxsize=1)
def _images(root: str) -> Dict[str, Any]:
    path = Path(root) / "config" / "labware_images.json"
    return json.loads(path.read_text()) if path.exists() else {"rules": [], "photos": {}}


def image_for(type_name: Optional[str], kind: str, root: Path = ROOT) -> Optional[Dict[str, Any]]:
    """A photo of this kind of labware (Wikimedia Commons, linked) and the product's page where one is known."""
    cfg = _images(str(root))
    for rule in cfg.get("rules", []):
        if rule.get("kind") and rule["kind"] != kind:
            continue
        if re.search(rule["match"], type_name or "", re.IGNORECASE):
            photo = cfg["photos"].get(rule.get("photo"), {})
            file = urllib.parse.quote(photo.get("file", ""))
            return {"name": rule.get("name"), "product_page": rule.get("product_page"),
                    "src": cfg["commons"].format(file=file) if photo else None,
                    "page": cfg["commons_page"].format(file=file) if photo else None,
                    "caption": photo.get("caption"), "license": photo.get("license"), "credit": photo.get("credit")}
    return None


def _words(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _mentions(text: str, lid: str, aliases: List[str]) -> bool:
    """Whether `text` is about labware `lid`: its ID, its ID's distinctive words (each the start of a word in the
    text, so "spin_column_rack" matches "spin columns"), or one of its aliases (the reagent it holds, its type)."""
    low = text.lower()
    if re.search(rf"(?<![a-z0-9_]){re.escape(lid.lower())}(?![a-z0-9_])", low):
        return True
    words = _words(text)
    key = [w for w in lid.lower().split("_") if w not in GENERIC and len(w) > 1 and not w.isdigit()]
    if key and all(any(t.startswith(k) for t in words) for k in key):
        return True
    return any(a and len(a) > 3 and a.lower() in low for a in aliases)


def _reagent_core(name: Optional[str]) -> Optional[str]:
    """ "Buffer ATL (DNeasy Blood & Tissue Kit)" -> "Buffer ATL"."""
    return re.split(r"\s*[(;,]", name)[0].strip() if name else None


def _roles(protocol: Dict[str, Any], kinds: Dict[str, str], outputs: List[str]) -> Dict[str, str]:
    loaded = {(loaded_wells(k) or (k,))[0] for k in (protocol.get("initial_volumes_ul") or {})}
    into = {s.get("labware") for s in protocol.get("steps", []) if s.get("action") == "dispense"}
    roles = {}
    for lid, kind in kinds.items():
        roles[lid] = ("tips" if kind == "tip_rack" else "waste" if kind == "trash" else "output" if lid in outputs
                      else "source" if lid in loaded and lid not in into else "intermediate" if lid in into
                      else "source" if lid in loaded else "")
    return roles


def deck_view(protocol: Dict[str, Any], deck_config: Dict[str, Any], report: Optional[Dict[str, Any]] = None,
              root: Path = ROOT) -> Dict[str, Any]:
    report = report or {}
    review = report.get("review") or {}
    target = report.get("target") or ("plr" if deck_config.get("catalog") == "plr" else "lab")
    deck, res = build_deck(deck_config, protocol.get("initial_volumes_ul"))
    kinds = {lid: spec["kind"] for lid, spec in deck_config["labware"].items()}
    used = {s.get("labware") for s in protocol.get("steps", [])}
    outputs = [o["labware"] for o in review.get("outputs", [])]
    roles = _roles(protocol, kinds, outputs)
    reagents = protocol.get("reagents", {})
    final = {o["labware"]: o for o in review.get("outputs", [])}

    # what to flag: problems ("must" items about labware, wells over their limits) and assumptions
    problems = [f"{i['item']}: {i['detail']}" if i.get("detail") else i["item"]
                for i in report.get("needs_review", []) if i.get("severity") == "must" and i.get("area") not in SKIP_AREAS]
    for w in review.get("wells", []):
        problems += [f"{w['plate']} column {w['column']}: {f}" for f in w.get("flags", [])]
    assumptions = list(review.get("assumptions") or protocol.get("assumptions") or [])
    matched_assumptions = set()

    def labware_item(lid: str, spec: Dict[str, Any], carrier: Dict[str, Any], n_sites: int) -> Dict[str, Any]:
        type_name = spec.get("venus_type") or spec.get("factory")
        aliases = [_reagent_core(reagents.get(lid)), type_name, spec.get("venus_id")]
        mine_a = [a for a in assumptions if _mentions(a, lid, aliases)]
        matched_assumptions.update(mine_a)
        mine_p = [p for p in problems if _mentions(p, lid, [type_name, spec.get("venus_id")])]
        item = {
            "id": lid, "slot": spec.get("slot"), "position": n_sites - spec["slot"] if "slot" in spec else None,
            "type": type_name, "kind": spec["kind"], "used": lid in used, "added": bool(spec.get("venus") or carrier.get("added")) and lid in used,
            "role": roles.get(lid, ""), "holds": reagents.get(lid),
            "loaded_ul": (protocol.get("initial_volumes_ul") or {}).get(lid),
            "assumptions": mine_a, "issues": mine_p,
            "status": "issue" if mine_p else "assumption" if mine_a else ("used" if lid in used else "idle"),
            "image": image_for(type_name, spec["kind"], root),
        }
        if lid in final:
            o = final[lid]
            item["final"] = {"wells": len(o["wells"]), "total_ul": o["total_ul"], "leaves_deck": o.get("leaves_deck")}
        r = res.get(lid)
        if r is not None and spec["kind"] == "plate":
            item["capacity_ul"] = round(r.get_item("A1").max_volume, 1)
        elif r is not None and spec["kind"] == "container":
            item["capacity_ul"] = round(getattr(r, "max_volume", 0) or 0, 1) or None
        return item

    carriers = []
    for spec in deck_config["carriers"]:
        resource = next((c for c in deck.children if c.name == spec["name"]), None)
        if resource is None:
            continue
        n_sites = len(getattr(resource, "sites", {}) or {})
        on_it = sorted(((lid, ls) for lid, ls in deck_config["labware"].items() if ls.get("carrier") == spec["name"]),
                       key=lambda kv: -kv[1].get("slot", 0))  # rear-most first, as the deck is seen from the front
        items = [labware_item(lid, ls, spec, n_sites) for lid, ls in on_it]
        type_name = spec.get("venus_type") or spec.get("factory")
        own_p = [p for p in problems if spec["name"] in p and not any(p in i["issues"] for i in items)]
        status = ("issue" if own_p or any(i["status"] == "issue" for i in items)
                  else "assumption" if any(i["status"] == "assumption" for i in items)
                  else "used" if any(i["used"] for i in items) else "idle")
        carriers.append({
            "name": spec["name"], "type": type_name, "rails": spec["rails"],
            "width": max(1, round(resource.get_size_x() / RAIL_MM)), "sites": n_sites, "added": bool(spec.get("added")),
            "issues": own_p, "status": status, "labware": items, "image": image_for(type_name, "carrier", root),
        })
    trash = [lid for lid, k in kinds.items() if k == "trash"]
    return {
        "target": target, "num_rails": getattr(deck, "num_rails", 30), "carriers": carriers,
        "waste": trash[0] if trash else None,
        "general_assumptions": [a for a in assumptions if a not in matched_assumptions],
        "unplaced_issues": [p for p in problems if not any(p in i["issues"] for c in carriers for i in c["labware"])
                            and not any(p in c["issues"] for c in carriers)],
    }
