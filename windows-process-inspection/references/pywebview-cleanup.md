# PyWebView (Windows) cleanup recipe

## Process topology

```
shell/background wrapper (may die, exits 127/2 late)
└── host: python rvox_desktop.py          (owns the API port, e.g. 18097)
    └── webview2 runtime: msedgewebview2.exe x N   (the actual app window + helper procs)
```

A pywebview app's UI is msedgewebview2.exe, NOT msedge.exe. Never kill msedge.exe to "clean up" an app — that is the user's browser. Only kill the host tree + its msedgewebview2 children.

## Recipe (from git-bash)

**Default to a full teardown + single relaunch over surgical zombie kills.** In a parent/child host tree, "selectively" killing one pid risks cascade-killing the live port-holder — the next probe then shows port FREE / health 000 and you have terminated your own working app. Unless CIM confirms the target pid does NOT own the port AND cannot take down the port-holder's tree, kill every app host pid + its msedgewebview2 children and launch exactly one fresh host. Surgical kills are only safe after verifying ownership of every pid involved. After ANY kill, re-verify port ownership + health before concluding.

1. Identify owners via CIM (ps1 file, run with -File): every `python.exe` with `*<app>*` in CommandLine.
2. Confirm which pid holds the port (`netstat -ano | grep <port>`); that one is the live host. Other matching pids are zombies — but ONLY after CIM confirmed their command line belongs to the app (never kill by pid alone).
3. Kill host pids: `MSYS2_ARG_CONV_EXCL="*" cmd //C "taskkill /F /PID <pid>"` — or a ps1 `Stop-Process -Id <pid> -Force`. Verify each with a CIM re-read; taskkill's silent banner means nothing.
4. Purge WebView2 children (ps1): `Get-CimInstance Win32_Process -Filter "Name='msedgewebview2.exe'" | Stop-Process -Force`. Some respawn on a 1–2s race — re-run once, then re-count.
5. Verify: port FREE, zero app python pids, only the new host's msedgewebview2 pids present.
6. Launch exactly ONE fresh host (persistent background job, absolute native paths), wait for its `/health`, then confirm feature markers in the served page.

## Stale-backend symptom signature (the "why")

After a restart sequence, if the user's window shows stuck "connecting" status + empty content region + dead native controls, it is almost always an ORPHAN WebView2 window still pointing at a dead backend pid. The fix is this recipe, not another UI patch.

## Verifying a deployed UI change actually reached the running app

When a user reports the UI 'looks unchanged' after a deploy, a stale instance is usually the cause — verify ops before touching design:

1. Kill every running instance (dev name AND deployed name) first. A running EXE is file-locked on Windows: the rebuild or the copy of the deployed copy fails with a permission error, not a visible 'in use' message.
2. `md5sum` the build output against the deployed copy — they must match.
3. Purge stale unpacked payloads before relaunch: `_MEI*` dirs sit NEXT TO WHERE THE APP LAST RAN (often the user's Desktop when the exe was deployed there, not only in temp — check both locations), plus the app's WebView2 cache (EBWebView under the app's window-title-named folder, in the exe dir and under `%LOCALAPPDATA%`).
4. Relaunch exactly one instance, wait for paint, then MARKER-CHECK the newest unpacked UI copy: read it, assert the NEW design marker string is present AND the OLD marker absent (grep for both). Grep the live asset, not the source tree — the source being correct proves nothing about what the window shows.
5. Only after 1–4 all pass and the user still perceives 'no difference' is it a design-conservatism problem: escalate to a structurally different layout, not another skin pass. When doing the structural pass, leave distinct marker strings for old and new designs so step 4 stays mechanically checkable next time.
