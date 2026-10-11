#!/usr/bin/env node
// Usage: node headless-dump-dom.mjs <url> [out.html] [virtualTimeMs]
// Drives Edge headless with a FRESH throwaway profile and a virtual-time budget so all
// inline scripts (including deferred probes) settle before the DOM is dumped.
// Works while the user's browser runs — no profile-lock conflict.
// Example (Windows git-bash): node headless-dump-dom.mjs http://127.0.0.1:18097/ C:/Users/.../dump.html 12000
import { spawnSync } from "node:child_process";
import { writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const url = process.argv[2];
const out = process.argv[3];
const vtb = process.argv[4] || "12000";
if (!url || !/^https?:/.test(url)) {
  console.error("usage: node headless-dump-dom.mjs <url> [out.html] [virtualTimeMs]");
  process.exit(1);
}
const outFile = out || join(tmpdir(), "dump-dom.html");

let edge;
for (const c of [
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  "msedge",
  "msedge.exe",
]) {
  if (c.includes("C:") && !existsSync(c)) continue;
  edge = c;
  break;
}
if (!edge) {
  console.error("msedge not found on PATH or in standard install locations");
  process.exit(1);
}

const profile = join(tmpdir(), "rv-dump-profile-" + Date.now());
const args = [
  "--headless=new", "--disable-gpu", "--no-sandbox",
  `--user-data-dir=${profile}`,
  `--virtual-time-budget=${vtb}`,
  "--dump-dom",
  url,
];
const r = spawnSync(edge, args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
if (r.error) {
  console.error("spawn failed:", r.error.message);
  process.exit(1);
}
writeFileSync(outFile, r.stdout, "utf8");
console.log(`dumped ${r.stdout.length} bytes -> ${outFile}`);
console.log("Extract #errdump / symptom counters from the file with Python multiline regex, NOT line-based grep.");
