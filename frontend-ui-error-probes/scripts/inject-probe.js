#!/usr/bin/env node
// Usage: node inject-probe.js <file.html> [delayMs]
// Prepend a zero-side-effect runtime error probe to the first <script> of an HTML page.
// Captures window 'error' + 'unhandledrejection', and after delayMs appends a visible
// <pre id="errdump"> listing captured errors + counters. Read the banner in the page or
// in a headless dump-dom output. Remove by re-running the script (it strips the old probe).
// NOTE: adjust the two counter selectors to your page's symptom markers before trusting the dump.
import { readFileSync, writeFileSync } from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("usage: node inject-probe.js <file.html> [delayMs]");
  process.exit(1);
}
const delay = Number(process.argv[3] || 6000);
let html = readFileSync(file, "utf8");

// strip a previous probe block so re-injection is idempotent
const start = html.indexOf("<script>\n/* ==== runtime error probe");
if (start >= 0) {
  const end = html.indexOf("</script>", start) + "</script>".length;
  html = html.slice(0, start) + html.slice(end);
}

const probe = `<script>\n/* ==== runtime error probe (remove after verification) ==== */\nwindow.__errs = window.__errs || [];
window.addEventListener('error', (e) => { window.__errs.push('ERR: ' + (e.message || '?') + ' @ line ' + e.lineno + ' col ' + e.colno); });
window.addEventListener('unhandledrejection', (e) => { window.__errs.push('REJECT: ' + ((e.reason && e.reason.message) || e.reason)); });
setTimeout(() => {
  const old = document.getElementById('errdump');
  if (old) old.remove();
  const d = document.createElement('pre');
  d.id = 'errdump';
  d.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;background:#000;color:#5f5;font-size:12px;font-family:monospace;max-height:42vh;overflow:auto;padding:10px;white-space:pre-wrap;';
  d.textContent = 'JS PROBE: ' + ((window.__errs || []).length ? window.__errs.join('\n---\n') : '(no runtime errors)') +
    '\nvitems=' + document.querySelectorAll('.vitem').length +
    ' engineText=' + (document.getElementById('engineText') || {}).textContent;
  document.body.appendChild(d);
}, ${delay});
</script>\n`;

const m = html.match(/<script(\s[^>]*)?>/);
if (!m) {
  console.error("no <script> tag found; add one to the page first");
  process.exit(1);
}
html = html.slice(0, m.index) + probe + html.slice(m.index);
writeFileSync(file, html, "utf8");
console.log(`probe injected into ${file} (delay=${delay}ms). Remember to remove after verifying (re-run this script).`);
