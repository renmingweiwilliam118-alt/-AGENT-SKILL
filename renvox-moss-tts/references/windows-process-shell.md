# RENVOX host restart + Windows shell pitfalls

The host is a process tree behind port 18097 (launcher `rvox_desktop.py` forks a venv shim + real cpython parent/child). Restart procedure:

1. Find the listener: `netstat -ano | grep 18097 | grep LISTEN` → OwningProcess pid.
2. Inspect before killing: `Get-CimInstance Win32_Process -Filter "ProcessId=<pid>"` for Name + CommandLine + ParentProcessId; kill the whole tree (launcher + real host), not one guessed pid — extra pids are NOT stale zombies.
3. Relaunch: `cd /g/MOSS-TTS-Nano && (G:/MOSS-TTS-Nano/.venv-onnx/Scripts/python.exe G:/MOSS-TTS-Nano/rvox_desktop.py > "$LOCALAPPDATA/Temp/rvox_host.log" 2>&1 &)` then wait ~25s, tail the log, health-check `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18097/` → 200.

Shell pitfalls (this machine, hit repeatedly — write to a `.ps1` file and `powershell -NoProfile -File` instead of fighting inline):

- git-bash terminal runs POSIX bash; tasklist/taskkill args get mangled by escaping — use PowerShell CIM: `Get-CimInstance Win32_Process` / `Stop-Process -Id`.
- `$pid` is a reserved PowerShell variable: `Stop-Process -Id $pid` kills the wrong process — use `$t`/`$id`.
- Inline `powershell -Command` next to other bash commands gets polluted by `$()`/`==` in adjacent echo text — write the PS to a `.ps1` file first.
- Execution policy blocks unsigned `.ps1` scripts — `powershell -File` may refuse; `-NoProfile -Command` inline (carefully quoted, `\$var`) is the fallback that works.
- The launcher wrapper's own `exit=127` exit in logs is a known path-resolution quirk, not a host crash — verify by health-check before re-launching.
