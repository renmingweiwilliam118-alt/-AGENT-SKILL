# Adding an audio input format to RENVOX end-to-end

The model wants specific wav input, but users upload arbitrary formats. Three layers, all must be touched:

1. **Frontend `ui/renvox.html`**: `accept` attribute on the file input + the `setFile` extension whitelist. Widen both (add `audio/*` plus explicit extensions: wav/mp3/flac/m4a/aac/ogg/oga/opus/wma/aiff/amr/3gp/caf/webm/m4b/dss/ac3/eac3/ape/wv...). Keep the "no extension" rejection only; replace the hard-block on unknown extensions with a "will be transcoded on generation" hint.
2. **Upload/persistence layer (`audio_compat.py` + `app.py`)**: the layer that both the torch and ONNX runtimes consume. On upload: probe readability with `soundfile.info` (wav/flac/ogg ok); on failure, transcode via ffmpeg to 16-bit 44.1kHz mono wav, save next to the original, and hand the runtime the wav path. ffmpeg lookup order: bundled `<project>/ffmpeg-1/bin/ffmpeg(.exe)` → system PATH. If ffmpeg is missing or the transcode fails, keep the original file and let the runtime try its own decoder (graceful degradation, never block the upload).
   - `ffmpeg_convert_to_wav` args that work: `-hide_banner -loglevel error -y -i <in> -ac 1 -ar 44100 -f wav <out>`.
3. **Packing (`build.spec`)**: ship the ffmpeg binary via `datas` (path `<proj>/ffmpeg-1/bin/ffmpeg.exe` → `ffmpeg-1/bin`) and add `audio_compat` to `hiddenimports` — otherwise the portable PyInstaller build has no transcode capability and every non-wav upload regresses on target machines.

Verify per layer, in order:
- Direct: generate a fixture m4a (ffmpeg-encode a synthetic wav), assert `soundfile.info(m4a)` fails on this build → `ffmpeg_convert_to_wav(m4a)` → `soundfile.read` returns the right duration/sample rate.
- Live host: POST the m4a as `prompt_audio` to `/api/generate-stream/start` (multipart; note required fields — empty optional fields like a blank demo_id can 422), stream_id in the response, close the stream immediately; grep the host log for the transcode line.
- Windows note: hand-rolled wav bytes for fixtures trip ffmpeg; use the `wave` stdlib module to write the source wav instead.
