# Model routing dashboard

One page for every Hermes profile's models, with Jev on top.

```bash
jev dashboard
```

Then open http://127.0.0.1:8791/.

- **Jev routing switch**: Off, Shadow (decide and log, do not switch) or On. It follows the profile picker: one profile, or **All profiles** with a confirmation. Takes effect on the next message; no restart.
- **Routing pools**: the pools in `jev/routing.json` as a grid — tiers down the side, kinds of work across the top — because that is the shape routing actually has. A missing pool is drawn as a hatched gap rather than left out, and a tier that has nothing but `general` and `vision` gets said out loud: Jev is asked what kind of work the turn is, that tier has no specialist pool, so the answer is bought and discarded. Models struck through are removed by an `exclude` pattern; a pool with nothing left is called empty in practice. Read-only — `jev models suggest --write` and your editor own that file.
- **Live**: every Jev decision as it happens, across all profiles: tier, kind of work, the model it went to, **which pool it came from**, confidence, Jev's latency. `medium / coding` means the specialty answer chose the model; `medium / general (fallback)` means it did not, which is the same money for no effect. Decisions only; the text of a turn is never logged or shown.
- **Models**: the main model and each auxiliary slot (compression, vision, title generation and the rest) per profile, with a searchable list of every model you hold a key or login for. **All profiles** sets a slot for everyone at once, after a confirmation that names how many agents it touches.
- Every write is previewed, backed up beside the config, and read back to verify. It never restarts a gateway.

The grid is layered the way `jevkit/route.py` layers it: `~/.config/jev/routing.json`, then the shared Hermes one, then the profile's own. A later file replaces a whole tier it mentions and inherits the tiers it does not, so a profile that pins only `hard` keeps everyone else's `simple` and `medium`. The page names every file it read.

Needs PyYAML, which Hermes' own Python already has; `jev dashboard` uses that interpreter when it finds it.

**Off your own machine** (Tailscale, VPN): `jev dashboard --host <private-ip>`. It refuses to start without a token off loopback, prints a one-time link carrying it, and swaps it for an HttpOnly cookie. The traffic is plain HTTP, so only do this on a network you trust end to end, and never on a public address.

Tests: `python -m unittest discover -s router-dashboard/tests` (with PyYAML installed).
