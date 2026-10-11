---
name: windows-process-inspection
description: Use when managing Windows processes from git-bash/MSYS.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, processes, powershell, msys, pywebview]
    related_skills: [frontend-ui-error-probes]
---

# Windows Process Inspection & Cleanup

Reliable process listing / identity / killing when the shell is git-bash (MSYS) on Windows. MSYS silently mangles many native-tool arguments; wmic is gone on Win11; and pywebview apps leave orphan WebView2 trees behind.

## When to Use

- Any time you list, identify, or kill a live Windows process from a git-bash / MSYS terminal.
- Before killing any PID: confirm ownership via CIM command line, not pid/memory size alone.
- Cleaning up a pywebview desktop app: kill the host tree AND purge its `msedgewebview2.exe` children, then verify port-free + single fresh host (full recipe in `references/pywebview-cleanup.md`).

## Pitfalls (mechanism first)

- **MSYS path-translates bare single-slash args to native tools.** `tasklist //FI "IMAGENAME eq python.exe"` and `cmd //C "taskkill /F /PID 123"` frequently do NOTHING while still printing success-ish banners — the filter/switches arrive mangled. Prefix with `MSYS2_ARG_CONV_EXCL="*"` when a command passes single-slash args to a native program. Verify with the follow-up read; never trust the exit code or the banner.
- **wmic does not exist on modern Win11.** Use `Get-CimInstance Win32_Process`. Inline `powershell -Command "...$_..."` gets mangled by bash quoting — WRITE the CIM query to a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File <path>`. Single-file probes are the pattern that works.
- **Read-before-kill, always via CIM command line.** Persistent PIDs can belong to UNRELATED long-running infrastructure that reuses PIDs (agent gateways, app servers). Before killing ANY pid, print its `ExecutablePath` + `CommandLine` and confirm ownership. PID + memory size alone is NOT identification.
- **pywebview apps on Windows = host process + a whole `msedgewebview2.exe` tree.** Killing only the host leaves orphaned WebView2 windows still polling the dead backend: the UI shows stuck-connecting status, dead native bridge, empty content — the classic stale-backend symptom. Cleanup = kill host tree AND purge `msedgewebview2.exe` children, then verify port-free + single fresh host. NEVER kill `msedge.exe` for this — that is the user's browser.
- **Background launcher wrappers report late exit 127/2 after their host was killed externally.** Treat such delayed notifications as noise: re-check port ownership + host identity before acting.
- **Cascade-killing hazard in parent/child trees.** A launched host often runs as a *pair* (a launcher/parent + the real port-owning child). Killing "the extra one" by pid, when the real one is its sibling or child in the same tree, drags the live host down with it — the next probe shows port FREE / health 000 and you have killed your own working app. Before any selective kill, confirm via CIM that the target pid does NOT own the port AND that its close/kill cannot take the port-holder's tree. When in doubt, don't do surgical zombie kills: prefer the full teardown + single relaunch in `references/pywebview-cleanup.md` (kills everything of the app, then launches exactly one fresh host). After ANY kill, re-verify port ownership + health before concluding.
- **`$pid` is a RESERVED PowerShell variable — never feed it to `Stop-Process`/`taskkill`.** PowerShell sets `$pid` to the *current* powershell process's pid automatically. Writing `Stop-Process -Id $pid` (or building a `taskkill` arg from `$pid`) kills the powershell shell itself / an unintended pid, not the app you targeted. Use a non-reserved variable name (`$t`, `$id`, `$pp`) for the target pid, and confirm the variable actually holds the app's pid before the kill.

## Standard probe (write to a .ps1, run with -File)

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Select-Object ProcessId, ExecutablePath, CommandLine | Format-Table -Wrap 200
```

Port ownership: `netstat -ano | grep <port>` (last column = pid) is reliable even when tasklist is not.

For the pywebview-specific kill-and-verify sequence, see `references/pywebview-cleanup.md`.
