"""Tests for the dashboard HTTP surface (real server on an ephemeral port)."""
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import routing_store as rs  # noqa: E402
import server as srv  # noqa: E402

CFG = """\
model:
  default: deepseek/deepseek-v4.1-flash
  provider: openrouter
auxiliary:
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash-0731
"""


class ServerTestCase(unittest.TestCase):
    token = None

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.home = cls.tmp.name
        with open(os.path.join(cls.home, "config.yaml"), "w", encoding="utf-8") as fh:
            fh.write(CFG)
        os.makedirs(os.path.join(cls.home, "profiles", "wiki"), exist_ok=True)
        with open(os.path.join(cls.home, "profiles", "wiki", "config.yaml"), "w", encoding="utf-8") as fh:
            fh.write(CFG)
        cfg = srv.Config(cls.home, cls.token)
        cls.httpd = srv.make_server("127.0.0.1", 0, cfg)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    def call(self, path, body=None, token=None):
        url = "http://127.0.0.1:%d%s" % (self.port, path)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET")
        if data:
            req.add_header("Content-Type", "application/json")
        if token:
            req.add_header("X-Dashboard-Token", token)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode())

    def test_health_and_auth_mode(self):
        code, body = self.call("/api/health")
        self.assertEqual(code, 200)
        self.assertTrue(body["ok"])
        self.assertFalse(body["auth_required"])

    def test_ui_is_served(self):
        with urllib.request.urlopen("http://127.0.0.1:%d/" % self.port, timeout=10) as resp:
            html = resp.read().decode()
        self.assertEqual(resp.status, 200)
        self.assertIn("Hermes Model Routing", html)
        self.assertIn("Apply changes", html)

    def test_state_lists_profiles_and_use_cases(self):
        code, body = self.call("/api/state")
        self.assertEqual(code, 200)
        self.assertEqual([p["name"] for p in body["profiles"]], ["default", "wiki"])
        self.assertEqual(body["use_cases"][0]["key"], "__main__")
        self.assertIn("intent", body["jev_mode"])

    def test_plan_previews_without_writing(self):
        before = open(os.path.join(self.home, "config.yaml"), encoding="utf-8").read()
        code, body = self.call("/api/plan", {"profile": "default",
                                             "changes": {"compression": {"model": "google/gemini-2.5-flash"}}})
        self.assertEqual(code, 200)
        self.assertEqual(body["rows"][0]["after"], "google/gemini-2.5-flash")
        self.assertEqual(open(os.path.join(self.home, "config.yaml"), encoding="utf-8").read(), before)

    def test_apply_requires_confirm(self):
        code, body = self.call("/api/apply", {"profile": "default",
                                              "changes": {"compression": {"model": "x/y"}}})
        self.assertEqual(code, 400)
        self.assertIn("confirm", body["error"])

    def test_apply_writes_and_verifies(self):
        code, body = self.call("/api/apply", {"profile": "wiki", "confirm": True,
                                              "changes": {"__main__": {"model": "z-ai/glm-5.3"},
                                                          "compression": {"model": "google/gemini-2.5-flash"}}})
        self.assertEqual(code, 200)
        self.assertTrue(body["ok"], body)
        self.assertTrue(body["verified"])
        self.assertTrue(body["reload_required"])
        self.assertTrue(os.path.isfile(body["backup"]))
        cfg = rs.read_config(os.path.join(self.home, "profiles", "wiki", "config.yaml"))
        self.assertEqual(cfg["main"]["model"], "z-ai/glm-5.3")
        self.assertEqual(cfg["slots"]["compression"]["model"], "google/gemini-2.5-flash")

    def test_unknown_profile_and_slot_are_rejected(self):
        code, body = self.call("/api/apply", {"profile": "nope", "confirm": True, "changes": {}})
        self.assertEqual(code, 404)
        code, body = self.call("/api/plan", {"profile": "default", "changes": {"bogus": {"model": "m"}}})
        self.assertEqual(code, 400)
        self.assertIn("unknown use case", body["error"])

    def test_injection_is_rejected(self):
        code, body = self.call("/api/plan", {"profile": "default",
                                             "changes": {"compression": {"model": "a\ninjected: true"}}})
        self.assertEqual(code, 400)


class PoolsEndpointTestCase(unittest.TestCase):
    """The grid the page draws comes from the server, so an empty specialty pool has to
    arrive as a cell, not be missing from the payload."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.home = cls.tmp.name
        with open(os.path.join(cls.home, "config.yaml"), "w", encoding="utf-8") as fh:
            fh.write(CFG)
        os.makedirs(os.path.join(cls.home, "jev"))
        with open(os.path.join(cls.home, "jev", "routing.json"), "w", encoding="utf-8") as fh:
            json.dump({"tiers": {t: {"general": ["openrouter:a/b"], "vision": ["openrouter:c/d"]}
                                 for t in ("simple", "medium", "hard")}}, fh)
        # A routing.json in the tester's own ~/.config would otherwise layer into this.
        cls.env = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": os.path.join(cls.home, "xdg")})
        cls.env.start()
        os.environ.pop("JEV_ROUTING_CONFIG", None)
        cls.httpd = srv.make_server("127.0.0.1", 0, srv.Config(cls.home, None))
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.env.stop()
        cls.tmp.cleanup()

    def get(self, path):
        with urllib.request.urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=10) as resp:
            return json.loads(resp.read().decode())

    def test_pools_endpoint_returns_a_full_grid_per_profile(self):
        body = self.get("/api/jev/pools")
        self.assertEqual(body["tiers"], ["simple", "medium", "hard"])
        grid = body["profiles"][0]["tiers"]
        self.assertEqual(grid["medium"]["coding"]["listed"], 0)
        self.assertEqual(grid["medium"]["general"]["models"][0]["ref"], "openrouter:a/b")

    def test_pools_endpoint_names_the_dead_axis(self):
        profile = self.get("/api/jev/pools")["profiles"][0]
        self.assertEqual(profile["dead_tiers"], ["simple", "medium", "hard"])
        self.assertIn("discarded", " ".join(w["text"] for w in profile["warnings"]))

    def test_page_offers_the_grid_and_the_pool_column(self):
        with urllib.request.urlopen("http://127.0.0.1:%d/" % self.port, timeout=10) as resp:
            html = resp.read().decode()
        self.assertIn("Routing pools", html)
        self.assertIn("From pool", html)


class NonLoopbackTestCase(unittest.TestCase):
    def test_refuses_exposed_bind_without_token(self):
        cfg = srv.Config(tempfile.gettempdir(), token=None)
        with self.assertRaises(SystemExit):
            srv.make_server("0.0.0.0", 0, cfg)

    def test_token_required_when_set(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            with open(os.path.join(tmp.name, "config.yaml"), "w", encoding="utf-8") as fh:
                fh.write(CFG)
            httpd = srv.make_server("127.0.0.1", 0, srv.Config(tmp.name, "s3cret"))
            port = httpd.server_address[1]
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            try:
                req = urllib.request.Request("http://127.0.0.1:%d/api/state" % port)
                with self.assertRaises(urllib.error.HTTPError) as ctx:
                    urllib.request.urlopen(req, timeout=10)
                self.assertEqual(ctx.exception.code, 401)
                req = urllib.request.Request("http://127.0.0.1:%d/api/state" % port)
                req.add_header("X-Dashboard-Token", "s3cret")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    self.assertEqual(resp.status, 200)
            finally:
                httpd.shutdown()
                httpd.server_close()
        finally:
            tmp.cleanup()


class AuthFlowTestCase(unittest.TestCase):
    """The ?token= link must work in a browser: exchange once, then use a cookie."""

    TOKEN = "s3cret"

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        with open(os.path.join(cls.tmp.name, "config.yaml"), "w", encoding="utf-8") as fh:
            fh.write(CFG)
        cls.httpd = srv.make_server("127.0.0.1", 0, srv.Config(cls.tmp.name, cls.TOKEN))
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    def get(self, path, cookie=None, follow=True):
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.port, path))
        if cookie:
            req.add_header("Cookie", cookie)
        opener = None if follow else urllib.request.build_opener(_NoRedirect)
        if follow:
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return resp.status, dict(resp.headers), resp.read().decode()
            except urllib.error.HTTPError as exc:
                return exc.code, dict(exc.headers), exc.read().decode()
        try:
            with opener.open(req, timeout=10) as resp:
                return resp.status, dict(resp.headers), resp.read().decode()
        except urllib.error.HTTPError as exc:
            return exc.code, dict(exc.headers), exc.read().decode()

    def test_token_link_redirects_and_sets_cookie(self):
        code, headers, _ = self.get("/?token=%s" % self.TOKEN, follow=False)
        self.assertEqual(code, 302)
        self.assertEqual(headers.get("Location"), "/")
        cookie = headers.get("Set-Cookie") or ""
        self.assertIn("hermes_dash_token=%s" % self.TOKEN, cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Strict", cookie)

    def test_wrong_token_link_sets_no_cookie(self):
        code, headers, body = self.get("/?token=nope", follow=False)
        self.assertEqual(code, 200)
        self.assertNotIn("Set-Cookie", headers)
        self.assertIn("Hermes Model Routing", body)  # page still loads; API stays locked

    def test_cookie_authorizes_api(self):
        code, _, body = self.get("/api/state", cookie="hermes_dash_token=%s" % self.TOKEN)
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)["profiles"][0]["name"], "default")

    def test_query_token_authorizes_api(self):
        code, _, body = self.get("/api/state?token=%s" % self.TOKEN)
        self.assertEqual(code, 200)
        self.assertIn("profiles", json.loads(body))

    def test_unauthenticated_api_is_locked(self):
        code, _, body = self.get("/api/state")
        self.assertEqual(code, 401)
        self.assertIn("unauthorized", json.loads(body)["error"])


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


if __name__ == "__main__":
    unittest.main(verbosity=2)
