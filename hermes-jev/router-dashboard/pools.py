#!/usr/bin/env python3
"""Jev's routing pools, read for display, and where the specialization axis is dead.

Pools are two-dimensional: tiers[tier][specialty] -> ["provider:model", ...]. Jev
answers both halves on every turn — how hard the work is, and what kind of work it
is — and jevkit/route.py `_pick` tries the specialty pool first, then general.

The kind question is bought on every turn. It only changes anything if the tier has
a pool named for one of the kinds Jev can answer. `vision` is not one of them: that
pool is chosen from the turn's images, not from Jev's answer. So a tier holding only
`general` and `vision` pays for an answer and discards it, which is the state this
module exists to make visible rather than leave as an invisible gap.

jevkit/route.py owns this contract. The constants below mirror it instead of
importing it, so that a half-finished edit to jevkit cannot blank the dashboard;
tests/test_pools.py fails when the two drift apart. Nothing here writes.
"""

from __future__ import annotations

import fnmatch
import json
import os
from typing import Any

TIERS = ("simple", "medium", "hard")
SPECIALTIES = ("general", "coding", "writing", "research", "vision")

#: The kinds of work Jev's answer can name (jevkit/route.py KIND). `vision` is
#: deliberately absent: images choose that pool, so it never redeems the question.
ANSWERABLE = ("coding", "writing", "research")

#: jevkit/route.py DEFAULT_CONFIG["exclude"]. A routing.json layer replaces it wholesale.
DEFAULT_EXCLUDE = ["*:free", "cloudflare-ai-gateway:*"]


def config_paths(hermes_root: str, profile_home: str) -> list:
    """Least specific first, mirroring jevkit.route.config_paths for one profile.

    route.config_paths answers for the process it runs in; the dashboard has to ask
    the same question per profile, so the layering is rebuilt here rather than called.
    """
    override = os.environ.get("JEV_ROUTING_CONFIG")
    if override:
        return [override]
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    paths = [os.path.join(base, "jev", "routing.json")]
    if os.path.isdir(hermes_root):
        paths.append(os.path.join(hermes_root, "jev", "routing.json"))
        if os.path.realpath(profile_home) != os.path.realpath(hermes_root):
            paths.append(os.path.join(profile_home, "jev", "routing.json"))
    return paths


def _read_layers(paths: list) -> dict:
    """Merge routing layers the way route.load_config does.

    A later layer replaces a whole tier it mentions and leaves alone the tiers it does
    not, so a profile can override just `hard` and still inherit the rest.
    """
    tiers: dict = {}
    exclude = list(DEFAULT_EXCLUDE)
    sources: list = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                layer = json.load(fh)
        except (OSError, ValueError):
            continue
        if not isinstance(layer, dict):
            continue
        sources.append(path)
        if isinstance(layer.get("tiers"), dict):
            for tier, pools in layer["tiers"].items():
                tiers[str(tier)] = pools if isinstance(pools, dict) else {}
        if "exclude" in layer:
            exclude = [str(p) for p in (layer.get("exclude") or [])]
    return {"tiers": tiers, "exclude": exclude, "sources": sources}


def _excluded(ref: str, patterns: list) -> bool:
    """route._pick skips these. A ref with no provider prefix is matched whole, because
    splitting it the way route does raised IndexError and blanked the page."""
    _, sep, bare = ref.partition(":")
    names = (ref, bare) if sep else (ref,)
    return any(fnmatch.fnmatch(name, pattern) for name in names for pattern in patterns)


def _cell(refs: Any, patterns: list) -> dict:
    models = []
    for ref in refs if isinstance(refs, list) else []:
        ref = str(ref)
        models.append({"ref": ref, "excluded": _excluded(ref, patterns)})
    usable = [m for m in models if not m["excluded"]]
    return {"models": models, "listed": len(models), "usable": len(usable)}


def _join(names: list) -> str:
    if len(names) <= 1:
        return "".join(names)
    return "%s and %s" % (", ".join(names[:-1]), names[-1])


def _higher(tier: str) -> list:
    """Tiers route._pick may fall up to. It never falls down, so the cheapest tier
    has the most cover and `hard` has none."""
    if tier not in TIERS:
        return []
    return list(TIERS[TIERS.index(tier) + 1:])


def grid_for(hermes_root: str, profile_home: str) -> dict:
    """One profile's effective pools as a tier x specialty grid, with the gaps named."""
    layers = _read_layers(config_paths(hermes_root, profile_home))
    patterns, raw = layers["exclude"], layers["tiers"]

    grid: dict = {}
    for tier in TIERS:
        pools = raw.get(tier)
        pools = pools if isinstance(pools, dict) else {}
        grid[tier] = {name: _cell(pools.get(name), patterns) for name in SPECIALTIES}
        # A pool named something route.py never looks for is dead weight; show it so the
        # typo is visible rather than silently ignored on every turn.
        for name, refs in pools.items():
            if name not in SPECIALTIES:
                grid[tier][str(name)] = _cell(refs, patterns)

    def usable(tier: str, names) -> int:
        return sum(grid[tier].get(n, {}).get("usable", 0) for n in names)

    dead = [t for t in TIERS if usable(t, SPECIALTIES) and not usable(t, ANSWERABLE)]
    dead_cells = _dead_cells(grid, dead)
    empty = [t for t in TIERS if not usable(t, SPECIALTIES)]
    configured = any(usable(t, SPECIALTIES) for t in TIERS)

    shadowed = []
    for tier in TIERS:
        for name in SPECIALTIES:
            cell = grid[tier][name]
            if cell["listed"] and not cell["usable"]:
                shadowed.append((tier, name, cell["listed"]))

    unknown = sorted({n for t in TIERS for n in grid[t] if n not in SPECIALTIES})
    # A mistyped tier name reads as an empty tier, which is a confusing symptom rather
    # than the cause; name the key routing is ignoring so the typo is the finding.
    stray = sorted(t for t in raw if t not in TIERS)

    return {
        "sources": layers["sources"],
        "exclude": patterns,
        "tiers": grid,
        "dead_tiers": dead,
        "dead_cells": dead_cells,
        "empty_tiers": empty,
        "unknown_pools": unknown,
        "unknown_tiers": stray,
        "configured": configured,
        "warnings": _warnings(configured, dead, empty, shadowed, unknown, stray, dead_cells),
    }


def _lead(cell: dict) -> str:
    for model in cell.get("models", []):
        if not model["excluded"]:
            return model["ref"]
    return ""


def _dead_cells(grid: dict, dead_tiers: list) -> list:
    """Specialty cells that resolve to the same lead as `general` in their tier.

    A tier could hold a coding pool and still be no better than one that does not, when
    that pool leads with the model general already leads with. The tier-level warning
    missed this and `jev doctor` (jevkit/route.py `specialty_cells`) did not, so the two
    disagreed about the same file. Tiers already reported dead as a whole are skipped
    here so one fault is not said twice.
    """
    cells = []
    for tier in TIERS:
        if tier in dead_tiers:
            continue
        general = _lead(grid[tier].get("general", {}))
        if not general:
            continue
        for name in ANSWERABLE:
            lead = _lead(grid[tier].get(name, {})) or general      # an empty pool falls through to general
            if lead == general:
                cells.append({"tier": tier, "specialty": name, "model": lead,
                              "listed": bool(_lead(grid[tier].get(name, {})))})
    return cells


def _warnings(configured: bool, dead: list, empty: list, shadowed: list, unknown: list, stray: list,
              dead_cells: Any = None) -> list:
    """Plain sentences for the page. The dead-axis one is the point of this module: it
    names money spent on a question whose answer is thrown away."""
    out = []
    if not configured:
        out.append({
            "level": "dead",
            "text": "No routing pools are configured, so Jev keeps whatever model this profile is already on. "
                    "Run `jev models suggest --write` to make a starting set.",
        })
        return out
    if len(dead) == len(TIERS):
        out.append({
            "level": "dead",
            "text": "Jev is asked what kind of work this is on every turn, but no tier has a coding, writing or "
                    "research pool, so the answer is always discarded. That question costs money and changes "
                    "nothing until at least one specialist pool exists.",
        })
    elif dead:
        out.append({
            "level": "dead",
            "text": "Jev is asked what kind of work this is, but the %s tier%s no coding, writing or research "
                    "pool, so the answer is discarded on those turns." % (
                        _join(dead), " has" if len(dead) == 1 else "s have"),
        })
    # Level "cell", not "dead": a tier with a working coding pool is specialised, and a
    # missing writing pool there is a choice rather than a fault. It is still named, because
    # `jev doctor` names it and two views of one file must not disagree.
    same = ["%s / %s" % (c["tier"], c["specialty"]) for c in (dead_cells or []) if c["listed"]]
    missing = ["%s / %s" % (c["tier"], c["specialty"]) for c in (dead_cells or []) if not c["listed"]]
    if same:
        out.append({
            "level": "cell",
            "text": "%s lead%s with the same model general leads with in that tier, so Jev's answer about the "
                    "kind of work cannot change the pick there. Put a different model first." % (
                        _join(same), "s" if len(same) == 1 else ""),
        })
    if missing:
        out.append({
            "level": "cell",
            "text": "%s %s no usable pool and fall%s through to general. Fine if that is the intent; "
                    "`jev doctor` lists the same cells." % (
                        _join(missing), "has" if len(missing) == 1 else "have", "s" if len(missing) == 1 else ""),
        })
    for tier in empty:
        higher = _higher(tier)
        out.append({
            "level": "empty",
            "text": "The %s tier has no usable models, so %s turns %s." % (
                tier, tier,
                "fall through to the %s pools, which cost more" % _join(higher) if higher
                else "keep the model they were already on"),
        })
    for tier, name, listed in shadowed:
        out.append({
            "level": "excluded",
            "text": "%s / %s lists %d model%s, but the exclude patterns remove all of them, so the pool is "
                    "empty in practice." % (tier, name, listed, "" if listed == 1 else "s"),
        })
    if unknown:
        out.append({
            "level": "unknown",
            "text": "Routing never looks at the pool%s named %s; only %s are used." % (
                "" if len(unknown) == 1 else "s", _join(unknown), _join(list(SPECIALTIES))),
        })
    if stray:
        out.append({
            "level": "unknown",
            "text": "Routing never looks at the tier%s named %s; only %s are used, so those models are never "
                    "picked." % ("" if len(stray) == 1 else "s", _join(stray), _join(list(TIERS))),
        })
    return out


def tier_grid(hermes_home: str, homes: list) -> dict:
    """The whole page payload: one grid per profile, plus the axis vocabulary."""
    profiles = []
    for name, home in homes:
        grid = grid_for(hermes_home, home)
        profiles.append({"name": name, "home": home, **grid})
    return {
        "tiers": list(TIERS),
        "specialties": list(SPECIALTIES),
        "answerable": list(ANSWERABLE),
        "profiles": profiles,
    }


# ------------------------------------------------------------------ provenance


def _search_order(tier: str, specialty: str, has_images: bool = False) -> list:
    """The (tier, pool) pairs route._pick would walk, most likely first.

    _pick never falls down a tier, and inside one it tries the specialty pool before
    general. Vision comes FIRST when the turn carried images, exactly as _pick does.

    That used to be unknowable here: the decision log did not record whether a turn had
    images, so vision was checked last and a model listed in both `vision` and `general`
    was attributed to `general` — a quiet wrong answer. `has_images` is now carried
    through route() into the log line, so this mirrors _pick instead of guessing.
    """
    order: list = []
    tiers = TIERS[TIERS.index(tier):] if tier in TIERS else (tier,)
    lead = ("vision",) if has_images else ()
    tail = () if has_images else ("vision",)
    for candidate in tiers:
        for name in lead + (specialty, "general") + tail:
            if (candidate, name) not in order:
                order.append((candidate, name))
    return order


def locate(grid: dict, tier: str, specialty: str, ref: str, has_images: bool = False) -> dict:
    """Which pool a routed model came from, and whether the specialty answer chose it.

    `earned` is the honest answer to "is the specialization axis worth its money":
    True when the model came from the pool Jev named, False when Jev named a specialty
    and the model came from somewhere else anyway, None when Jev said `general` and
    there was nothing to earn.
    """
    specialty = specialty or "general"
    for candidate_tier, name in _search_order(tier, specialty, has_images):
        cell = (grid.get(candidate_tier) or {}).get(name) or {}
        if any(m.get("ref") == ref for m in cell.get("models") or []):
            return {
                "found": True,
                "tier": candidate_tier,
                "specialty": name,
                "asked": specialty,
                "earned": (name == specialty) if specialty in ANSWERABLE else None,
                "fell_up": candidate_tier != tier,
            }
    return {"found": False, "tier": tier, "specialty": None, "asked": specialty,
            "earned": None, "fell_up": False}
