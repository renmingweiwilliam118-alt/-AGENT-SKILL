# OPENFILENAMEW (x64) — verified ctypes layout

`comdlg32.GetSaveFileNameW` / `GetOpenFileNameW` (NOT user32). Verified via `ctypes.sizeof` probe on Windows x64:

- `sizeof(OFN) == 160` — assert this before trusting any struct change.
- Spot-check offsets: `Flags` @ 80, `lpDefExt` @ 96, `wReserved` @ 158.

| # | field | type |
|---|-------|------|
| 0 | lStructSize | DWORD |
| 1 | hwndOwner | HWND |
| 2 | hInstance | HANDLE |
| 3 | lpstrFilter | LPCWSTR |
| 4 | lpstrFile | LPCWSTR (writer fills it) |
| 5 | nFile | DWORD (capacity of lpstrFile in characters) |
| 6 | lpstrFileTitle | LPCWSTR |
| 7 | nFileTitle | DWORD (buffer capacity) |
| 8 | lpstrInitialDir | LPCWSTR |
| 9 | lpstrTitle | LPCWSTR |
| 10 | Flags | DWORD |
| 11 | nFilterIndex | WORD |
| 12 | nFileOffset | WORD |
| 13 | nFileLength | WORD |
| 14 | nFileTitleLength | WORD |
| 15 | lpDefExt | LPCWSTR |
| 16 | lpstrCustomFilter | LPCWSTR |
| 17 | lCustData | DWORD |
| 18 | lpfnHook | c_void_p |
| 19 | lpTemplateName | LPCWSTR |
| 20 | pvReserved | c_void_p |
| 21 | dwReserved | DWORD |
| 22 | fOwnerData | BOOL |
| 23 | wReserved | WORD |

## Filter strings

Null-separated pairs, terminated with a double null:

```python
"WAV (*.wav)\0*.wav\0All files (*.*)\0*.*\0\0"
```

## Flag values used

- `OFN_EXPLORER` 0x0002 — modern IFileDialog (needs STA COM on the calling thread)
- `OFN_HIDEREADONLY` 0x0004
- `OFN_NOCHANGEDIR` 0x0010
- `OFN_OVERWRITEPROMPT` 0x8000

## Failure triage (verified observations)

- Returns 0 + `GetLastError` 87 (0x57, low word of E_INVALIDARG): dialog never appeared — parameter/COM-class failure, not user-cancel.
- Returns 0 + `GetLastError` 1813 (FNCANCEL): dialog opened and was cancelled.
- `GetLastError` can be stale/meaningless after failures (threads interleave); only trust it when it matches a known code AND the window-watcher saw no dialog.
