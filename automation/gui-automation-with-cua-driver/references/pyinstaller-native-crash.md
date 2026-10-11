# PyInstaller Native Crash Prevention

## The Problem

PyInstaller onefile apps that use ctypes (Win32 API calls) or mss
(screen capture) across multiple threads crash with:

```
Exception code: 0xc0000005 (ACCESS_VIOLATION)
Faulting module: python314.dll
```

This does NOT happen when running the same code as a plain .py script.
The crash is specific to the PyInstaller frozen environment.

## Root Cause

Multiple threads concurrently calling into C extensions (ctypes, mss)
corrupt shared C-level state. The Python GIL does not protect C extension
internal state. In PyInstaller's frozen environment, the C extensions are
loaded differently, making the race condition more likely to manifest.

## Solution: Global RLock

```python
import threading

# MUST be RLock (reentrant), not Lock.
# Reason: a function holding the lock may call another function
# that also needs the lock (e.g., _execute holds lock, then calls
# verify_sent which calls grab_png which needs the same lock).
_native_lock = threading.RLock()

def grab_png(region=None):
    with _native_lock:
        import mss
        with mss.mss() as sct:
            # ... screenshot code

def win32_click(xy):
    with _native_lock:
        # ... SetCursorPos + SendInput

def win32_send_text(text):
    with _native_lock:
        # ... clipboard + Ctrl+V

def virtual_screen():
    with _native_lock:
        import mss
        with mss.mss() as sct:
            # ...
```

## Additional: Pause or Stop Background Threads

Even with a global lock, background monitoring threads that periodically
call `grab_png` can deadlock or race with foreground operations.

**Light pause (skip cycles):**

```python
def _monitor_loop(self):
    while self.monitoring:
        time.sleep(self.cycle)
        if self.picking:
            continue  # skip this cycle
        png = grab_png(self.region)
```

**Hard stop (for heavy Win32 window operations like rubber-band selection):**

```python
def begin_region_pick(self):
    was_monitoring = self.monitoring
    if was_monitoring:
        self.stop_monitor()
        time.sleep(0.2)  # let the thread finish its current cycle

    try:
        # ... creates/destroys Win32 windows (rubber band overlay)
    finally:
        if was_monitoring:
            self.start_monitor()
```

## Debugging Crashes

When the app crashes, check Windows Event Viewer:

```powershell
Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000; StartTime=(Get-Date).AddMinutes(-10)} |\
  Select-Object TimeCreated, Message | Format-List
```

Look for:
- `Exception code: 0xc0000005` → access violation (race condition)
- `Faulting module: python314.dll` → C extension state corruption
- Fault offset (e.g. `0xa4487`) → consistent offset = same code path crashing

## What Does NOT Work

- `threading.Lock()` instead of `RLock()` → deadlocks on reentrant calls
- Only skipping cycles with a flag → thread may be mid-call when flag is set
- faulthandler → changes crash behavior, gives false positives on thread teardown
- Separate locks per subsystem → still allows cross-subsystem races

## Build Output Verification

A build script ending in `ls -l dist/app.exe` reports that pipeline's exit
code, which can mask a partial failure. After `PyInstaller` finishes:

1. Re-check the exe timestamp/length directly (`ls -l dist/*.exe`); a build
   that "succeeded" but did not touch the file is not a real rebuild.
2. Confirm new code actually shipped — e.g. `grep -c '<unique-new-symbol>'
   source.py` returns ≥1, and for bundled binaries inspect the generated
   `.spec` for the expected `binaries=[...]` entries.
3. For onefile bundles with extra `--add-binary` payloads, expect a large
   size jump (tens of MB) — no size change means the payload was not embedded.
