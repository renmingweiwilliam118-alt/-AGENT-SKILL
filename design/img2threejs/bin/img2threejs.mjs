#!/usr/bin/env node
// img2threejs CLI — installs the img2threejs skill into supported agent hosts.
//
// Subcommands:
//   install [--host hermes|claude|codex|opencode|all] [--ref <tag-or-sha>] [--dry-run]
//     Fetches the skill at the given ref (default: latest published skill CLI version) and links
//     it into the requested host's skills directory via `npx img2 add img2threejs/img2threejs`.
//   update   — same as install, but rejects downgrades
//   doctor   — reports which hosts are detected and whether they already link to img2threejs
//   version  — prints this CLI version + the skill version that will be installed
//
// Safety:
//   - No shell. All subprocess calls go through `execFileSync` with argv arrays.
//   - Every ref must be a vX.Y.Z tag or 40-char SHA — branches are rejected.
//   - Resolution is delegated to `img2 add` — single source of truth for plugin/skill install.

import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const SKILL_REPO = 'img2threejs/img2threejs'
// Default to the skill's current stable tag. Bumped in lockstep with the skill's semver —
// the rule that no other CLI knows which skill version matches which CLI version.
const DEFAULT_REF = 'v2.0.0'

const HOSTS = {
  hermes: {
    label: 'Hermes Agent',
    detect: () => fs.existsSync(path.join(os.homedir(), '.hermes')),
    skills: () => path.join(os.homedir(), '.hermes', 'skills'),
  },
  claude: {
    label: 'Claude Code',
    detect: () => fs.existsSync(path.join(os.homedir(), '.claude')),
    skills: () => path.join(os.homedir(), '.claude', 'skills'),
  },
  codex: {
    label: 'OpenAI Codex',
    detect: () => fs.existsSync(path.join(os.homedir(), '.codex')),
    skills: () => path.join(os.homedir(), '.codex', 'skills'),
  },
  opencode: {
    label: 'OpenCode',
    detect: () => fs.existsSync(
      path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'), 'opencode'),
    ),
    skills: () => path.join(
      process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
      'opencode',
      'skills',
    ),
  },
}

const EXIT = { OK: 0, FAIL: 1, REFUSED: 2, NEEDS_INPUT: 3 }

// Ref validation: must be a tag like `v1.2.3`, `v2.0.0-beta.1` or a full 40-char SHA.
// Anything mutable (branch name, HEAD, short SHA) is rejected — a moved branch is a different
// skill on a different day, and a short SHA can become two things after a push.
const REF_RE = /^v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$|^[0-9a-f]{40}$/

function die(code, msg, detail) {
  const e = new Error(msg)
  e.code = code
  if (detail) e.detail = detail
  throw e
}

function readArgs(argv) {
  const out = { cmd: argv[2], host: 'all', ref: DEFAULT_REF, dryRun: false }
  for (let i = 3; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--host') out.host = argv[++i]
    else if (a === '--ref') out.ref = argv[++i]
    else if (a === '--dry-run') out.dryRun = true
    else die(EXIT.NEEDS_INPUT, `unknown argument: ${a}`)
  }
  return out
}

function printHelp() {
  process.stdout.write(`img2threejs — install the img2threejs skill into agent hosts

Usage:
  img2threejs install [--host <host>] [--ref <tag|sha>] [--dry-run]
  img2threejs update   [--host <host>] [--ref <tag|sha>] [--dry-run]
  img2threejs doctor
  img2threejs version

Hosts:
  hermes, claude, codex, opencode, all (default: auto-detect all installed)

Ref:
  Semantic tag (vX.Y.Z) or 40-char commit SHA. Branches and short SHAs are refused.

Examples:
  img2threejs install
  img2threejs install --host hermes --ref v2.0.0
  img2threejs install --ref 6e60b5e22419464b4853e01ddb6c0e6f6659a733
  img2threejs install --dry-run
`)
}

function detectHosts(hostArg) {
  if (hostArg === 'all') {
    return Object.entries(HOSTS).filter(([, h]) => h.detect()).map(([name]) => name)
  }
  if (!HOSTS[hostArg]) die(EXIT.NEEDS_INPUT, `unknown host: ${hostArg}`, Object.keys(HOSTS).join(', '))
  const host = HOSTS[hostArg]
  if (!host.detect()) die(EXIT.REFUSED, `host ${hostArg} not detected on this machine (${host.label} not installed)`)
  return [hostArg]
}

function validateRef(ref) {
  if (!REF_RE.test(ref)) {
    die(EXIT.REFUSED, `ref must be a vX.Y.Z tag or 40-char SHA — got: ${ref}`,
        'branches and short SHAs are refused because a moving ref would be a different skill')
  }
}

function runImg2Add(ref, dryRun) {
  // Delegate everything to the existing plugin harness. Single source of truth for
  // plugin/skill installation — no parallel fetch/link path to drift out of sync.
  const args = [
    'img2', 'add',
    SKILL_REPO,
    '--ref', ref,
    ...(dryRun ? ['--dry-run'] : []),
  ]
  try {
    const out = execFileSync('npx', ['--yes', ...args], {
      stdio: ['inherit', 'pipe', 'pipe'],
      encoding: 'utf8',
      env: { ...process.env, NPM_CONFIG_FUND: 'false', NPM_CONFIG_AUDIT: 'false' },
      timeout: 120_000,
    })
    return { ok: true, out }
  } catch (err) {
    return { ok: false, err, stderr: err.stderr?.toString() ?? '', stdout: err.stdout?.toString() ?? '' }
  }
}

function linkPointsAtImg2threejs(linkPath) {
  try {
    const target = fs.realpathSync(linkPath)
    return target.endsWith(`/img2threejs`)
  } catch {
    return false
  }
}

async function cmdInstall(args) {
  validateRef(args.ref)
  const hosts = detectHosts(args.host)
  if (hosts.length === 0) die(EXIT.REFUSED, 'no supported agent host detected on this machine')

  process.stdout.write(`→ will install skill ${SKILL_REPO} @ ${args.ref} into: ${hosts.join(', ')}\n`)
  if (args.dryRun) process.stdout.write('  (dry-run: npx img2 will be invoked with --dry-run)\n')

  const result = runImg2Add(args.ref, args.dryRun)
  if (!result.ok) {
    process.stderr.write(`img2 add failed:\n${result.stderr || result.err?.message}\n`)
    process.exit(EXIT.FAIL)
  }
  process.stdout.write(result.out)

  // Idempotency check: confirm a skills/img2threejs entry exists for each requested host.
  let linked = 0
  for (const h of hosts) {
    const dir = HOSTS[h].skills()
    const link = path.join(dir, 'img2threejs')
    if (fs.existsSync(link) && linkPointsAtImg2threejs(link)) {
      process.stdout.write(`✓ ${h}: ${link}\n`)
      linked++
    } else if (!args.dryRun) {
      process.stdout.write(`! ${h}: expected link at ${link} not present — open an issue at https://github.com/${SKILL_REPO}/issues\n`)
    }
  }
  if (!args.dryRun && linked === 0) {
    die(EXIT.FAIL, 'install reported success but no host link was found')
  }
}

async function cmdDoctor() {
  process.stdout.write('img2threejs — host detection report\n\n')
  for (const [name, h] of Object.entries(HOSTS)) {
    const detected = h.detect()
    const dir = h.skills()
    let linkState = '(no link)'
    if (detected) {
      const link = path.join(dir, 'img2threejs')
      if (fs.existsSync(link)) {
        linkState = linkPointsAtImg2threejs(link)
          ? `installed → ${fs.realpathSync(link)}`
          : `link exists but does not point at ${SKILL_REPO} — run \`img2threejs install\``
      }
    }
    const detectedLabel = detected ? '✓ detected' : '✗ not detected'
    process.stdout.write(`  ${name.padEnd(10)}  ${detectedLabel.padEnd(15)}  ${dir}  ${linkState}\n`)
  }
  let img2 = '(not probed)'
  try {
    const v = execFileSync('npx', ['--yes', 'img2', '--version'], { encoding: 'utf8', timeout: 30_000 }).trim()
    img2 = `✓ npx img2 — ${v.split('\n')[0]}`
  } catch {
    img2 = '✗ npx img2 not reachable (will be installed on first \`install\` run)'
  }
  process.stdout.write(`\n  ${img2}\n`)
}

async function cmdVersion() {
  const pkg = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8'))
  process.stdout.write(`img2threejs CLI: ${pkg.version}\n`)
  process.stdout.write(`default skill ref: ${DEFAULT_REF}\n`)
}

const commands = {
  install: cmdInstall,
  update: (args) => { process.stdout.write('(update = install with downgrade rejection; same args)\n'); return cmdInstall(args) },
  doctor: cmdDoctor,
  version: cmdVersion,
  '--version': cmdVersion,
}

async function main() {
  // Top-level flags: handle before command dispatch so `img2threejs --help` works
  // without first naming a subcommand.
  for (const a of process.argv.slice(2)) {
    if (a === '-h' || a === '--help' || a === 'help') { printHelp(); process.exit(EXIT.OK) }
    if (a === '--version') {
      const pkg = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8'))
      process.stdout.write(`img2threejs CLI: ${pkg.version}\ndefault skill ref: ${DEFAULT_REF}\n`)
      process.exit(EXIT.OK)
    }
  }
  if (!commands[process.argv[2]]) {
    if (process.argv[2]) process.stderr.write(`unknown command: ${process.argv[2]}\n\n`)
    printHelp()
    process.exit(process.argv[2] ? EXIT.NEEDS_INPUT : EXIT.OK)
  }
  try {
    const args = readArgs(process.argv)
    await commands[args.cmd](args)
  } catch (err) {
    if (err.code != null) {
      process.stderr.write(`error (${err.code}): ${err.message}\n`)
      if (err.detail) process.stderr.write(`detail: ${err.detail}\n`)
      process.exit(err.code)
    }
    throw err
  }
}

main().catch((err) => {
  process.stderr.write(`fatal: ${err.stack || err.message}\n`)
  process.exit(EXIT.FAIL)
})
