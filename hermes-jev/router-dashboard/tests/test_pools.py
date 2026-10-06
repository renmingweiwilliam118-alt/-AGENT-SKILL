"""Tests for pools: the tier x specialty grid, and naming a dead specialization axis."""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pools  # noqa: E402

GENERAL_ONLY = {
    "tiers": {
        "simple": {"general": ["openrouter:cheap/one"], "vision": ["openrouter:sees/one"]},
        "medium": {"general": ["openrouter:mid/one"], "vision": ["openrouter:sees/two"]},
        "hard": {"general": ["openrouter:big/one"], "vision": ["openrouter:sees/three"]},
    }
}


def write(path, blob):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(blob, fh)


class _Home(unittest.TestCase):
    """A user's own ~/.config/jev/routing.json must not leak into these results."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.xdg = os.path.join(self.home, "xdg")
        os.makedirs(self.xdg)
        env = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": self.xdg}, clear=False)
        env.start()
        os.environ.pop("JEV_ROUTING_CONFIG", None)
        self.addCleanup(env.stop)
        self.addCleanup(self.tmp.cleanup)

    def shared(self, blob):
        write(os.path.join(self.home, "jev", "routing.json"), blob)

    def grid(self, profile=None):
        home = os.path.join(self.home, "profiles", profile) if profile else self.home
        return pools.grid_for(self.home, home)


class PoolGridTests(_Home):
    def test_every_tier_and_specialty_has_a_cell_even_when_unconfigured(self):
        self.shared(GENERAL_ONLY)
        grid = self.grid()["tiers"]
        self.assertEqual(sorted(grid), sorted(pools.TIERS))
        for tier in pools.TIERS:
            self.assertEqual(sorted(grid[tier]), sorted(pools.SPECIALTIES))
            self.assertEqual(grid[tier]["coding"]["listed"], 0)
        self.assertEqual([m["ref"] for m in grid["simple"]["general"]["models"]], ["openrouter:cheap/one"])

    def test_a_tier_with_only_general_and_vision_is_a_dead_axis(self):
        self.shared(GENERAL_ONLY)
        out = self.grid()
        self.assertEqual(out["dead_tiers"], list(pools.TIERS))
        self.assertEqual(out["empty_tiers"], [])

    def test_dead_axis_warning_says_the_kind_answer_is_discarded(self):
        self.shared(GENERAL_ONLY)
        text = " ".join(w["text"] for w in self.grid()["warnings"] if w["level"] == "dead")
        self.assertIn("what kind of work this is", text)
        self.assertIn("discarded", text)

    def test_a_tier_with_a_specialist_pool_is_not_dead(self):
        blob = json.loads(json.dumps(GENERAL_ONLY))
        blob["tiers"]["medium"]["coding"] = ["openrouter:codes/well"]
        self.shared(blob)
        out = self.grid()
        self.assertEqual(out["dead_tiers"], ["simple", "hard"])
        text = " ".join(w["text"] for w in out["warnings"] if w["level"] == "dead")
        self.assertIn("simple and hard tiers have", text)

    def test_no_dead_axis_warning_when_every_tier_specialises(self):
        blob = json.loads(json.dumps(GENERAL_ONLY))
        for tier in pools.TIERS:
            blob["tiers"][tier]["coding"] = ["openrouter:codes/well"]
        self.shared(blob)
        out = self.grid()
        self.assertEqual(out["dead_tiers"], [])
        self.assertEqual([w for w in out["warnings"] if w["level"] == "dead"], [])

    def test_empty_tier_is_reported_separately_from_a_dead_axis(self):
        blob = json.loads(json.dumps(GENERAL_ONLY))
        blob["tiers"]["medium"] = {}
        self.shared(blob)
        out = self.grid()
        self.assertEqual(out["empty_tiers"], ["medium"])
        self.assertNotIn("medium", out["dead_tiers"])
        text = " ".join(w["text"] for w in out["warnings"] if w["level"] == "empty")
        self.assertIn("The medium tier has no usable models", text)
        self.assertIn("hard", text)  # it falls up, and that costs more

    def test_empty_hard_tier_says_the_turn_keeps_its_model(self):
        blob = json.loads(json.dumps(GENERAL_ONLY))
        blob["tiers"]["hard"] = {}
        self.shared(blob)
        text = " ".join(w["text"] for w in self.grid()["warnings"] if w["level"] == "empty")
        self.assertIn("keep the model they were already on", text)

    def test_a_pool_removed_entirely_by_exclude_patterns_reads_as_empty(self):
        self.shared({"exclude": ["openrouter:cheap/*", "openrouter:sees/one"], "tiers": GENERAL_ONLY["tiers"]})
        out = self.grid()
        cell = out["tiers"]["simple"]["general"]
        self.assertEqual((cell["listed"], cell["usable"]), (1, 0))
        self.assertTrue(cell["models"][0]["excluded"])
        self.assertIn("simple", out["empty_tiers"])      # every model in the tier was excluded
        text = " ".join(w["text"] for w in out["warnings"] if w["level"] == "excluded")
        self.assertIn("simple / general lists 1 model, but the exclude patterns remove all of them", text)

    def test_a_tier_that_still_has_a_vision_pool_is_dead_not_empty(self):
        self.shared({"exclude": ["openrouter:cheap/*"], "tiers": GENERAL_ONLY["tiers"]})
        out = self.grid()
        self.assertNotIn("simple", out["empty_tiers"])
        self.assertIn("simple", out["dead_tiers"])

    def test_exclude_matches_the_bare_model_id_as_route_does(self):
        self.shared({"exclude": ["*/one:free"], "tiers": {"simple": {"general": ["openrouter:cheap/one:free"]}}})
        self.assertTrue(self.grid()["tiers"]["simple"]["general"]["models"][0]["excluded"])

    def test_a_ref_with_no_provider_prefix_does_not_crash(self):
        self.shared({"tiers": {"simple": {"general": ["bare-model-id"]}}})
        self.assertEqual(self.grid()["tiers"]["simple"]["general"]["usable"], 1)

    def test_a_profile_overrides_one_tier_and_inherits_the_rest(self):
        self.shared(GENERAL_ONLY)
        write(os.path.join(self.home, "profiles", "wiki", "jev", "routing.json"),
              {"tiers": {"hard": {"research": ["openrouter:deep/one"]}}})
        wiki = self.grid("wiki")["tiers"]
        self.assertEqual([m["ref"] for m in wiki["hard"]["research"]["models"]], ["openrouter:deep/one"])
        self.assertEqual(wiki["hard"]["general"]["listed"], 0)          # the tier was replaced, not merged
        self.assertEqual(wiki["simple"]["general"]["listed"], 1)        # other tiers still inherited
        self.assertEqual(self.grid("wiki")["dead_tiers"], ["simple", "medium"])

    def test_unknown_pool_name_is_shown_rather_than_silently_ignored(self):
        self.shared({"tiers": {"simple": {"general": ["openrouter:cheap/one"], "codeing": ["openrouter:typo/one"]}}})
        out = self.grid()
        self.assertEqual(out["unknown_pools"], ["codeing"])
        self.assertIn("codeing", out["tiers"]["simple"])
        text = " ".join(w["text"] for w in out["warnings"] if w["level"] == "unknown")
        self.assertIn("Routing never looks at the pool named codeing", text)

    def test_unknown_tier_name_is_named_rather_than_read_as_an_empty_tier(self):
        blob = json.loads(json.dumps(GENERAL_ONLY))
        blob["tiers"]["mediumm"] = blob["tiers"].pop("medium")
        self.shared(blob)
        out = self.grid()
        self.assertEqual(out["unknown_tiers"], ["mediumm"])
        text = " ".join(w["text"] for w in out["warnings"] if w["level"] == "unknown")
        self.assertIn("Routing never looks at the tier named mediumm", text)

    def test_no_config_anywhere_says_there_are_no_pools(self):
        out = self.grid()
        self.assertFalse(out["configured"])
        self.assertEqual(out["sources"], [])
        self.assertIn("No routing pools are configured", out["warnings"][0]["text"])

    def test_unreadable_config_is_skipped_not_fatal(self):
        os.makedirs(os.path.join(self.home, "jev"), exist_ok=True)
        with open(os.path.join(self.home, "jev", "routing.json"), "w", encoding="utf-8") as fh:
            fh.write("{ not json")
        self.assertFalse(self.grid()["configured"])

    def test_env_override_replaces_every_other_layer(self):
        self.shared(GENERAL_ONLY)
        other = os.path.join(self.home, "elsewhere.json")
        write(other, {"tiers": {"simple": {"coding": ["openrouter:only/one"]}}})
        with mock.patch.dict(os.environ, {"JEV_ROUTING_CONFIG": other}):
            grid = self.grid()
        self.assertEqual(grid["sources"], [other])
        self.assertEqual(grid["tiers"]["simple"]["general"]["listed"], 0)

    def test_tier_grid_covers_every_profile_home(self):
        self.shared(GENERAL_ONLY)
        homes = [("default", self.home), ("wiki", os.path.join(self.home, "profiles", "wiki"))]
        out = pools.tier_grid(self.home, homes)
        self.assertEqual([p["name"] for p in out["profiles"]], ["default", "wiki"])
        self.assertEqual(out["tiers"], list(pools.TIERS))
        self.assertEqual(out["answerable"], list(pools.ANSWERABLE))


class DeadCellTests(_Home):
    """The page and `jev doctor` read the same file, so they must name the same cells."""

    def test_a_specialty_pool_that_leads_with_generals_model_is_reported_dead(self):
        self.shared({"tiers": {"medium": {"general": ["or:glm", "or:deepseek"],
                                          "coding": ["or:glm", "or:kimi"],
                                          "research": ["or:grok"]}}})
        grid = self.grid()
        self.assertEqual(grid["dead_tiers"], [])
        dead = {(c["tier"], c["specialty"]) for c in grid["dead_cells"]}
        self.assertEqual(dead, {("medium", "coding"), ("medium", "writing")})     # writing has no pool -> general
        texts = [w["text"] for w in grid["warnings"] if w["level"] == "cell"]
        self.assertTrue(any("medium / coding" in text and "same model" in text for text in texts))
        self.assertTrue(any("medium / writing" in text and "falls through" in text for text in texts))

    def test_the_page_agrees_with_jev_doctor_on_the_same_config(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
        from jevkit import route
        config = {"tiers": {"simple": {"general": ["or:a"], "coding": ["or:a"], "writing": ["or:w"]},
                            "hard": {"general": ["or:h"], "coding": ["or:free-model:free", "or:h"],
                                     "research": ["or:r"]}}}
        self.shared(config)
        merged = dict(route.DEFAULT_CONFIG, **config)
        doctor = {(c["tier"], c["specialty"]) for c in route.specialty_cells(merged) if c["dead"]}
        page = {(c["tier"], c["specialty"]) for c in self.grid()["dead_cells"]}
        self.assertEqual(page, doctor)

    def test_a_tier_already_reported_dead_is_not_reported_again_cell_by_cell(self):
        self.shared({"tiers": {"simple": {"general": ["or:a"]}}})
        grid = self.grid()
        self.assertEqual(grid["dead_tiers"], ["simple"])
        self.assertEqual([c for c in grid["dead_cells"] if c["tier"] == "simple"], [])


class ProvenanceTests(unittest.TestCase):
    """`locate` answers the question the live view exists for: did the specialty pool
    actually choose this model, or was the answer bought and thrown away?"""

    def setUp(self):
        def cell(*refs):
            return {"models": [{"ref": r, "excluded": False} for r in refs], "listed": len(refs), "usable": len(refs)}
        self.grid = {
            "simple": {"general": cell("openrouter:cheap/one"), "coding": cell(), "vision": cell()},
            "medium": {"general": cell("openrouter:mid/one"), "coding": cell("openrouter:codes/well"),
                       "vision": cell("openrouter:sees/one")},
            "hard": {"general": cell("openrouter:big/one"), "coding": cell(), "vision": cell()},
        }

    def test_specialty_pool_is_credited_when_it_chose_the_model(self):
        out = pools.locate(self.grid, "medium", "coding", "openrouter:codes/well")
        self.assertTrue(out["found"])
        self.assertEqual((out["tier"], out["specialty"]), ("medium", "coding"))
        self.assertIs(out["earned"], True)
        self.assertFalse(out["fell_up"])

    def test_general_fallback_is_named_when_the_specialty_pool_was_empty(self):
        out = pools.locate(self.grid, "hard", "coding", "openrouter:big/one")
        self.assertEqual((out["tier"], out["specialty"]), ("hard", "general"))
        self.assertIs(out["earned"], False)

    def test_a_general_answer_claims_no_specialty_credit_either_way(self):
        out = pools.locate(self.grid, "simple", "general", "openrouter:cheap/one")
        self.assertEqual(out["specialty"], "general")
        self.assertIsNone(out["earned"])

    def test_falling_up_to_a_dearer_tier_is_visible(self):
        out = pools.locate(self.grid, "simple", "coding", "openrouter:codes/well")
        self.assertEqual((out["tier"], out["specialty"]), ("medium", "coding"))
        self.assertTrue(out["fell_up"])

    def test_a_model_no_longer_in_any_pool_is_not_guessed_at(self):
        out = pools.locate(self.grid, "medium", "coding", "openrouter:gone/away")
        self.assertFalse(out["found"])
        self.assertIsNone(out["specialty"])

    def test_vision_pool_is_recognised_as_the_source(self):
        out = pools.locate(self.grid, "medium", "coding", "openrouter:sees/one")
        self.assertEqual(out["specialty"], "vision")
        self.assertIs(out["earned"], False)


class ContractDriftTests(unittest.TestCase):
    """The dashboard copies route.py's axis rather than importing it, so a copy that has
    gone stale must fail here rather than quietly mis-report the grid."""

    def test_axis_matches_jevkit_route(self):
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        try:
            from jevkit import route
        except Exception as exc:  # jevkit is not on the path in a dashboard-only install
            self.skipTest("jevkit not importable: %s" % exc)
        self.assertEqual(pools.TIERS, route.TIERS)
        self.assertEqual(set(pools.SPECIALTIES), set(route.SPECIALTIES))
        self.assertEqual(set(pools.ANSWERABLE), set(route.KIND) - {"general"})
        self.assertEqual(pools.DEFAULT_EXCLUDE, route.DEFAULT_CONFIG["exclude"])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class VisionProvenanceTests(unittest.TestCase):
    """A model in both `vision` and `general` used to be blamed on `general`.

    The decision log did not record whether the turn carried images, so provenance
    checked the vision pool last and quietly gave the wrong answer for every image turn.
    `has_images` now rides along in the log line, so this mirrors route._pick.
    """

    CELL = {"models": [{"ref": "openrouter:m", "excluded": False}]}
    GRID = {"medium": {"general": CELL, "vision": CELL,
                       "coding": {"models": []}, "writing": {"models": []},
                       "research": {"models": []}}}

    def test_an_image_turn_is_credited_to_the_vision_pool(self):
        found = pools.locate(self.GRID, "medium", "general", "openrouter:m", True)
        self.assertEqual(found["specialty"], "vision")

    def test_a_text_turn_with_the_same_model_is_credited_to_general(self):
        found = pools.locate(self.GRID, "medium", "general", "openrouter:m", False)
        self.assertEqual(found["specialty"], "general")

    def test_the_search_order_matches_pick_for_an_image_turn(self):
        order = pools._search_order("medium", "coding", True)
        self.assertEqual(order[0], ("medium", "vision"))
        self.assertEqual(order[1], ("medium", "coding"))

    def test_the_search_order_leaves_vision_last_without_images(self):
        order = pools._search_order("medium", "coding", False)
        self.assertEqual(order[0], ("medium", "coding"))
        self.assertIn(("medium", "vision"), order[2:])
