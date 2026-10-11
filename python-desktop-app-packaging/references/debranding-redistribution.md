# De-branding for redistribution
Strip author identity while keeping protective text.

## Remove (the user's explicit ask)
- Author **names, emails, GitHub handles/links, paid-ads, FUNDING, CODEOWNERS**, sponsor/discount links (README included).
- UI: author footer components, sidebar Star/GitHub buttons, license-modal author links, i18n `author`/`github` keys. Delete the components and their render calls.
- **Runtime console strings** the app prints to its own terminal/log panel: ASCII-art project-name banners (figlet blocks), logger names (`getLogger("<Project>")`), prompt strings like `root@crawler:~$`, and startup banner prints. The user sees these live, not just in source — replace with the new name or drop the banner.
- **App-name metadata**: `pyproject.toml` `author = …`, npm `package.json`/`package-lock.json` top-level `"name"`, FastAPI `title=`/health-check message strings (surface in `/docs` and API probes), i18n JSON bundles, and any `README`/`CODEOWNERS` identity.
- File headers: batch line-filter `# Copyright (c)` / `This file is part of <Project> project` author lines across all source (hundreds of files) — a script, not by hand.
- **Header-GENERATOR constants** (the surface a UI-only audit misses): tooling that *writes* a copyright/author header into **user data files** — e.g. a file-header manager with `REPO_URL` / `EMAIL` / `GITHUB_PROFILE` / banner constants — leaks the old identity into every artifact the app produces, even though it never renders in the UI or console. Grep for the constant names (not just the project string) and re-point them to the new name.
- Metadata: `pyproject.toml` `author = …`, `LICENSE` copyright holder, third-party JS signature lines you added.

## Keep (do NOT strip)
- The **NON-COMMERCIAL / learning-only license disclaimer** and protective Chinese/English usage notices — they protect the novice user and the author's terms.
- **Third-party upstream credits** you did not write (e.g. a vendored library's own copyright) — removing those is legally wrong.

## Verify
A whole-repo grep for the author tokens returns **zero** matches (excluding the intentionally-kept third-party credit) — grep source AND console-visible runtime strings (i18n bundles, log lines, banner art), not just docs. `compileall` + importing the entrypoint both pass. Byte-scan the **built** frontend and bundle for any leftover signature (e.g. an emoji tab title) — not just source.

## Rebuild after de-brand
Any UI/author change requires rebuilding the web frontend **and** regenerating the served copy (e.g. `api/webui`) **and** re-bundling into the frozen backend's `_internal/webui`. A stale served copy is the usual reason "I removed it but it still shows".
