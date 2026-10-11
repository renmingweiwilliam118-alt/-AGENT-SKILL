# Audio result-card player — reusable code

Proven patterns for a per-card audio player with pause/resume, seekable progress, and a playback-synced waveform. Adapt variable names; the math and class-gating are the load-bearing parts.

## Single global player state

```js
// mode: "web" (Web Audio BufferSource) or "audio" (fallback <audio> for flac blob)
const P = { on:false, id:null, mode:null, src:null, audio:null, buf:null, offset:0, startedAt:0, url:null };

function hardStop(){
  if (P.src){ P.src.onended=null; try{P.src.stop();}catch(e){} P.src=null; }
  if (P.audio){ try{P.audio.pause();}catch(e){} P.audio=null; }
  if (P.url){ URL.revokeObjectURL(P.url); P.url=null; }
  P.on=false; P.offset=0;
}

// click same card while playing → pause (capture offset first)
function pauseCapture(){
  if (P.mode==="web" && P.on)
    P.offset = Math.min(P.offset + (performance.now()-P.startedAt)/1000, P.buf?.duration||0);
  else if (P.mode==="audio" && P.audio) P.offset = P.audio.currentTime;
  P.on=false;
  if (P.src){ P.src.onended=null; try{P.src.stop();}catch(e){} P.src=null; }
  if (P.audio){ try{P.audio.pause();}catch(e){} }
}
```

## Web Audio play / resume (offset in seconds into buffer)

```js
async function play(buf){
  const AC = window.AudioContext||window.webkitAudioContext;
  if (!S.audioCtx) S.audioCtx = new AC();
  const ctx = S.audioCtx;
  if (ctx.state==="suspended") { const p=ctx.resume(); if(p?.then) await p; }
  P.buf = await ctx.decodeAudioData(buf.slice(0));
  P.mode = "web";
  P.startedAt = performance.now();
  const src = ctx.createBufferSource();
  src.buffer = P.buf; src.connect(ctx.destination);
  src.onended = () => { P.on=false; P.offset=0; /* reset this card's play button to ▶ */ };
  src.start(0, P.offset);        // offset>0 → resume from pause
  P.src = src; P.on = true;
}
```

## `<audio>` fallback (FLAC blob; Web Audio can't decode flac containers in Chromium)

```js
P.url = URL.createObjectURL(new Blob([buf], {type:"audio/flac"}));
P.audio = new Audio(P.url); P.mode = "audio";
P.audio.onended = () => { P.on=false; P.offset=0; };
P.audio.currentTime = P.offset;      // resume position
await P.audio.play(); P.on = true;
```

## Progress bar + time label + seek

`dur` falls back to WAV byte-length when `duration` is unavailable/`Infinity`:

```js
const dur = (el) => el._player?.duration && isFinite(el._player.duration)
  ? el._player.duration
  : (el._wav.length - 44) / 48000 / 2;   // 16-bit WAV: (bytes - 44 hdr) / sampleRate / channels

el._player.addEventListener("timeupdate", () => {
  const d = dur(el), p = d ? el._player.currentTime / d : 0;
  fill.style.width = (p*100).toFixed(2)+"%";
  timer.textContent = fmt(el._player.currentTime) + " / " + fmt(d);
  syncWave(el, p);
});

function fmt(s){ s=Math.max(0,Math.floor(s)); return String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0"); }

// click / drag to seek
let dragging=false;
const seek=(e)=>{ if(!el._player) return; const r=prog.getBoundingClientRect();
  const f=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width));
  el._player.currentTime = f*dur(el); fill.style.width=(f*100).toFixed(2)+"%"; syncWave(el,f); };
prog.addEventListener("mousedown", e=>{ dragging=true; seek(e); });
addEventListener("mousemove", e=>{ if(dragging) seek(e); });
addEventListener("mouseup", ()=>{ dragging=false; });
```

## Waveform: frozen idle → animate on play → colorize by progress

Markup (random per-bar heights so the idle card looks like a real waveform):

```js
const wave = Array.from({length:48}, ()=>
  `<span style="height:${(18+Math.random()*82).toFixed(0)}%;animation-delay:${(-Math.random()*1.1).toFixed(2)}s"></span>`).join("");
// card DOM: <div class="wv">${wave}</div><div class="rprog"><i></i></div>
```

CSS — animation only runs while `.playing`; `transform-origin` keeps the pulse rooted at each bar's base:

```css
.wv{display:flex;justify-content:space-between;align-items:flex-end;height:38px;width:100%}
.wv span{width:3px;height:30%;border-radius:3px;background:linear-gradient(var(--c),var(--b));transform-origin:50% 100%}
.card.playing .wv span{animation:wv 1.1s ease-in-out infinite}
@keyframes wv{0%,100%{transform:scaleY(.55)}50%{transform:scaleY(1)}}
.card .wv span.passed{background:linear-gradient(180deg,var(--ok),var(--c))}
.card .wv span.now{box-shadow:0 0 10px var(--c),0 0 22px rgba(34,211,238,.5)}
.rprog{position:relative;height:4px;cursor:pointer;overflow:hidden;background:rgba(255,255,255,.08);border-radius:2px}
.rprog i{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,var(--a),var(--b))}
```

Colorize in sync with the timeupdate/seek fraction:

```js
function syncWave(el, frac){
  const bars = el._bars;                    // cached from el.querySelectorAll(".wv span")
  const now = Math.min(bars.length-1, Math.round(frac*bars.length));
  bars.forEach((b,i)=>{
    b.classList.toggle("passed", i < now);
    b.classList.toggle("now", i === now && el.classList.contains("playing"));
  });
}
```

On `onended` and on unpausing/reset: `syncWave(el,0)` then strip `passed`/`now` so the frozen idle state returns.

## Pitfalls

- Forgetting `transform-origin:50% 100%` makes the scaleY pulse look like bars jumping out of the row instead of pulsing from the baseline.
- Not clearing `src.onended` before reusing the buffer means the previous card's ended-handler fires and resets the wrong button icon.
- `audio.duration` is `Infinity` until `loadedmetadata` on some blobs; the byte-length fallback (above) is what keeps the bar moving on generated WAVs.
- Two cards each spawning their own `Audio`/`BufferSource` = overlapping audio; enforce the single global `P`.

## Verify in the live app

```python
# playwright headless probe against the running host
errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
rep = pg.evaluate("""() => ({
  cardW: Math.round(document.querySelector('#list .item')?.getBoundingClientRect().width ?? 0),
  player: typeof P !== 'undefined' ? Object.keys(P) : 'undef',
  pause:  typeof pauseCapture,
})""")
# assert expected size + that P/pauseCapture exist; errs must be empty
```

A generated result card (with `.rprog`) only exists after the user synthesizes once, so to probe the progress/wave code either trigger a generation first or unit-test the markup path.
