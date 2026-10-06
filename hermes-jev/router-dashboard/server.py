#!/usr/bin/env python3
"""Hermes model-routing dashboard.

Reads every Hermes profile's model routing and lets you change it from a browser:
per-use-case model dropdowns, Jev's tier x specialty pool grid, a live split view,
a change preview, and an Apply button that writes with a backup and verifies the
read-back.

Safety defaults:
  * binds 127.0.0.1 unless --host is given explicitly;
  * a non-loopback bind REQUIRES a token (`--token` or DASHBOARD_TOKEN);
  * POST /api/apply requires an explicit confirm flag;
  * the server never restarts a gateway and never pushes anywhere — it reports
    that a reload is required.

Usage:
    python3 server.py [--host 127.0.0.1] [--port 8791] [--token TOKEN]
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import routing_store as rs  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "static", "index.html")
MAX_BODY = 256 * 1024

LOOPBACK = {"127.0.0.1", "localhost", "::1"}
COOKIE = "hermes_dash_token"


class Config:
    def __init__(self, hermes_home: str, token: Optional[str] = None) -> None:
        self.hermes_home = hermes_home
        self.token = token or os.environ.get("DASHBOARD_TOKEN") or None


def _is_loopback(host: str) -> bool:
    return host in LOOPBACK


class Handler(BaseHTTPRequestHandler):
    server_version = "HermesRoutingDashboard/1.0"
    cfg: Config  # set by make_server

    # ------------------------------------------------------------- helpers
    def _json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            raise ValueError("missing or oversized body")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _supplied_token(self, path: str) -> str:
        """Header first (programmatic), then cookie, then a one-time ?token=."""
        supplied = self.headers.get("X-Dashboard-Token") or ""
        if supplied:
            return supplied
        cookie = self.headers.get("Cookie") or ""
        for part in cookie.split(";"):
            name, _, value = part.strip().partition("=")
            if name == COOKIE:
                return value
        if "?" in path:
            from urllib.parse import parse_qs
            return (parse_qs(path.split("?", 1)[1]).get("token") or [""])[0]
        return ""

    def _authed(self, path: str = "") -> bool:
        if not self.cfg.token:
            return True
        return hmac.compare_digest(self._supplied_token(path), self.cfg.token)

    def _redirect(self, location: str, cookie: Optional[str] = None) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        if cookie:
            self.send_header(
                "Set-Cookie",
                "%s=%s; HttpOnly; SameSite=Strict; Path=/" % (COOKIE, cookie),
            )
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, fmt: str, *args: Any) -> None:  # keep stdout clean
        sys.stderr.write("dashboard %s\n" % (fmt % args))

    # --------------------------------------------------------------- routes
    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            # A ?token= link is exchanged once for a cookie and stripped from the URL.
            if self.cfg.token and "token=" in self.path and self._authed(self.path):
                self._redirect("/", cookie=self.cfg.token)
                return
            try:
                with open(INDEX, "r", encoding="utf-8") as fh:
                    self._html(fh.read())
            except OSError as exc:
                self._json({"error": f"UI missing: {exc}"}, 500)
            return
        if path == "/api/health":
            self._json({"ok": True, "hermes_home": self.cfg.hermes_home,
                        "auth_required": bool(self.cfg.token)})
            return
        if not self._authed(self.path):
            self._json({"error": "unauthorized"}, 401)
            return
        if path == "/api/state":
            self._json(rs.snapshot(self.cfg.hermes_home))
            return
        if path == "/api/jev/switches":
            self._json(rs.jev_switch_state(self.cfg.hermes_home))
            return
        if path == "/api/jev/pools":
            self._json(rs.jev_pools(self.cfg.hermes_home))
            return
        if path == "/api/jev/live":
            from urllib.parse import parse_qs
            query = parse_qs(self.path.split("?", 1)[1]) if "?" in self.path else {}
            try:
                since = float((query.get("since") or ["0"])[0])
            except ValueError:
                since = 0.0
            self._json(rs.jev_live(self.cfg.hermes_home, since=since))
            return
        if path == "/api/models":
            self._json({"models": rs.model_catalog(self.cfg.hermes_home)})
            return
        self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if not self._authed(self.path):
            self._json({"error": "unauthorized"}, 401)
            return
        try:
            payload = self._read_json()
        except Exception as exc:
            self._json({"error": f"bad request: {exc}"}, 400)
            return

        if path == "/api/jev/switch":
            if payload.get("scope") == "__all__" and payload.get("confirm") is not True:
                self._json({"error": "changing every profile requires confirm:true"}, 400)
                return
            try:
                self._json(rs.set_jev_switch(self.cfg.hermes_home, str(payload.get("scope") or ""),
                                             str(payload.get("switch") or ""), str(payload.get("value") or "")))
            except ValueError as exc:
                self._json({"error": str(exc)}, 400)
            return

        profile = str(payload.get("profile") or "")
        changes = payload.get("changes") or {}
        if not isinstance(changes, dict):
            self._json({"error": "changes must be an object"}, 400)
            return
        targets = {t.name: t for t in rs.discover_targets(self.cfg.hermes_home)}
        if profile not in targets:
            self._json({"error": f"unknown profile: {profile!r}"}, 404)
            return

        try:
            if path == "/api/plan":
                self._json({"profile": profile, "rows": rs.plan(targets[profile].path, changes)})
                return
            if path == "/api/apply":
                if payload.get("confirm") is not True:
                    self._json({"error": "apply requires confirm:true"}, 400)
                    return
                receipt = rs.apply_changes(self.cfg.hermes_home, targets[profile].path, changes)
                receipt["profile"] = profile
                self._json(receipt)
                return
        except ValueError as exc:
            self._json({"error": str(exc)}, 400)
            return
        except Exception as exc:
            self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
            return
        self._json({"error": "not found"}, 404)


def make_server(host: str, port: int, cfg: Config) -> ThreadingHTTPServer:
    if not _is_loopback(host) and not cfg.token:
        raise SystemExit(
            "refusing to bind %s without a token: exposing model routing off-loopback "
            "requires --token or DASHBOARD_TOKEN" % host
        )
    handler = type("BoundHandler", (Handler,), {"cfg": cfg})
    return ThreadingHTTPServer((host, port), handler)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Hermes model-routing dashboard")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8791)
    ap.add_argument("--token", default=None)
    ap.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes"))
    args = ap.parse_args(argv)

    cfg = Config(hermes_home=args.hermes_home, token=args.token)
    httpd = make_server(args.host, args.port, cfg)
    where = "http://%s:%d/" % (args.host, httpd.server_address[1])
    print("model-routing dashboard: %s" % where)
    print("hermes home: %s" % cfg.hermes_home)
    print("auth: %s" % ("token required" if cfg.token else "none (loopback only)"))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
