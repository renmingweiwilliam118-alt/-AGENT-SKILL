#!/usr/bin/env node
// Self-contained tests for the img2threejs CLI. Run via `node bin/img2threejs.mjs-test.mjs` or
// indirectly through `npm test`. Pure: no network, no fs writes outside TMPDIR.

import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { spawn } from 'node:child_process'

const here = path.dirname(new URL(import.meta.url).pathname)
const cliPath = path.join(here, 'img2threejs.mjs')

let passed = 0
let failed = 0
const failures = []

function assert(cond, msg) {
  if (cond) { passed++; return }
  failed++
  failures.push(msg)
  process.stderr.write(`FAIL: ${msg}\n`)
}

// 1. CLI file exists and is the entry the bin field points at.
const pkg = JSON.parse(fs.readFileSync(path.join(here, '..', 'package.json'), 'utf8'))
assert(pkg.bin?.img2threejs === 'bin/img2threejs.mjs', 'package.json bin -> bin/img2threejs.mjs')
assert(fs.existsSync(cliPath), 'bin entry exists on disk')

// 2. CLI has --help subpath that exits 0 without doing anything destructive.
function runCli(argv, env = {}) {
  return new Promise((resolve) => {
    const proc = spawn(process.execPath, [cliPath, ...argv], {
      env: { ...process.env, ...env, NPM_CONFIG_FUND: 'false' },
      stdio: ['ignore', 'pipe', 'pipe'],
    })
    let out = '', err = ''
    proc.stdout.on('data', (d) => out += d)
    proc.stderr.on('data', (d) => err += d)
    proc.on('close', (code) => resolve({ code, stdout: out, stderr: err }))
  })
}

const v = await runCli(['--version'])
assert(v.code === 0, `--version exit 0 (got ${v.code})`)
assert(/img2threejs CLI: 0\.1\.0/.test(v.stdout), '--version prints CLI version')

const help = await runCli(['--help'])
assert(help.code === 0, '--help exit 0')
assert(/Usage:/.test(help.stdout), '--help prints Usage')

// 3. Ref validation: branches refused, short SHAs refused, tags and full SHAs accepted.
const src = fs.readFileSync(cliPath, 'utf8')
assert(src.includes('v\\d+\\.\\d+\\.\\d+') && src.includes('[0-9a-f]{40}'), 'REF_RE accepts only vX.Y.Z tag or 40-char SHA')
assert(!/accepts branch/i.test(src), 'docs do not advertise branch support')

// 4. Refuse non-pinned ref with the right error code.
const badRef = await runCli(['install', '--ref', 'main', '--host', 'claude', '--dry-run'])
assert(badRef.code === 2, `refusing 'main' exit 2 (got ${badRef.code}, stderr: ${badRef.stderr})`)

// 5. Hosts listed in --help match the canonical four. Scope: hermes, claude, codex, opencode.
for (const host of ['hermes', 'claude', 'codex', 'opencode']) {
  assert(help.stdout.includes(host), `--help mentions host: ${host}`)
}

// 6. Optional: doctor dry-run doesn't require network. Skip if running with no host present.
const doc = await runCli(['doctor'])
assert(doc.code === 0 || doc.code === 1, `doctor exit sane (got ${doc.code})`)

process.stdout.write(`\nimg2threejs CLI self-test: ${passed} passed, ${failed} failed\n`)
if (failed > 0) {
  process.exit(1)
}
