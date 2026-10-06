/**
 * /context-save + /context-restore project identity (#3003), end to end.
 *
 * Runs the REAL bash blocks extracted from the generated context-save and
 * context-restore SKILL.md files (with ~/.claude/skills/gstack pointed at this
 * checkout) inside fixture repos, so the checkpoint stamp, the restore
 * classification and the helper modes are exercised together. The bug these
 * pin: GitLab repos in different groups (a/product/repo, b/product/repo) shared
 * one projects/product-repo/ bucket, and /context-restore in project B
 * presented project A's checkpoint as the latest one, with nothing failing.
 */
import { describe, test, expect, beforeEach, afterEach } from 'bun:test';
import { spawnSync } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

const ROOT = path.resolve(import.meta.dir, '..');
const SLUG_BIN = path.join(ROOT, 'bin', 'gstack-slug');

function bashBlockAfter(skillFile: string, heading: string, contains?: string): string {
  const md = fs.readFileSync(path.join(ROOT, skillFile), 'utf-8');
  const start = md.indexOf(heading);
  if (start < 0) throw new Error(`${skillFile}: heading not found: ${heading}`);
  const re = /```bash\n([\s\S]*?)```/g;
  re.lastIndex = start;
  for (let m = re.exec(md); m; m = re.exec(md)) {
    if (!contains || m[1].includes(contains)) return m[1].replaceAll('~/.claude/skills/gstack', ROOT);
  }
  throw new Error(`${skillFile}: no bash block after ${heading}`);
}

const SAVE_PATH_BLOCK = bashBlockAfter('context-save/SKILL.md', '### Step 4: Write saved-context file').replace(
  'TIMESTAMP=$(date +%Y%m%d-%H%M%S)',
  'TIMESTAMP="$TEST_TIMESTAMP"',
);
const STAMP_BLOCK = bashBlockAfter('context-save/SKILL.md', '### Step 4: Write saved-context file', '--stamp-checkpoint');
const RESTORE_BLOCK = bashBlockAfter('context-restore/SKILL.md', '### Step 1: Find saved contexts');

let tmp: string;
let home: string;

function env(extra: Record<string, string> = {}): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [k, v] of Object.entries(process.env)) if (v !== undefined) out[k] = v;
  delete out.GSTACK_PROJECT_SLUG;
  delete out.GSTACK_STATE_ROOT;
  delete out.GSTACK_STATE_DIR;
  delete out.CURRENT_BRANCH;
  return { ...out, HOME: tmp, GSTACK_HOME: home, ...extra };
}

function sh(script: string, cwd: string, extra: Record<string, string> = {}) {
  const r = spawnSync('bash', ['-c', script], { cwd, env: env(extra), encoding: 'utf-8', timeout: 30_000 });
  return { stdout: r.stdout ?? '', stderr: r.stderr ?? '', status: r.status ?? -1 };
}

function repo(name: string, origin?: string): string {
  const dir = path.join(tmp, name);
  fs.mkdirSync(dir, { recursive: true });
  for (const args of [['init', '-q', '-b', 'main'], ...(origin ? [['remote', 'add', 'origin', origin]] : [])]) {
    const r = spawnSync('git', args, { cwd: dir, encoding: 'utf-8', timeout: 30_000 });
    if (r.status !== 0) throw new Error(`git ${args.join(' ')}: ${r.stderr}`);
  }
  return dir;
}

/** The context-save flow: path block, the agent's Write, then the stamp block. */
function save(cwd: string, title: string, timestamp: string, branch = 'main'): string {
  const paths = sh(SAVE_PATH_BLOCK, cwd, { TITLE_RAW: title, TEST_TIMESTAMP: timestamp });
  expect(paths.status).toBe(0);
  const file = paths.stdout.match(/^FILE=(.+)$/m)![1];
  fs.writeFileSync(file, `---\nstatus: in-progress\nbranch: ${branch}\ntimestamp: ${timestamp}\n---\n\n## Working on: ${title}\n`);
  const stamp = sh(STAMP_BLOCK.replace('FILE="<the FILE path printed above>"', `FILE=${JSON.stringify(file)}`), cwd);
  expect(stamp.stdout).toContain('STAMPED');
  return file;
}

function restore(cwd: string, branch = 'main') {
  const r = sh(RESTORE_BLOCK, cwd, { CURRENT_BRANCH: branch });
  expect(r.status).toBe(0);
  const lines = r.stdout.split('\n').filter(Boolean);
  const candidates = lines.filter((l) => l.startsWith('/'));
  return { out: r.stdout, lines, candidates, latest: candidates[0] };
}

function legacyCheckpoint(bucket: string, name: string, branch = 'main'): string {
  const dir = path.join(home, 'projects', bucket, 'checkpoints');
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, name);
  fs.writeFileSync(file, `---\nstatus: in-progress\nbranch: ${branch}\n---\n\n## Working on: ${name}\n`);
  return file;
}

beforeEach(() => {
  tmp = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'ctx-identity-')));
  home = path.join(tmp, '.gstack');
});

afterEach(() => {
  fs.rmSync(tmp, { recursive: true, force: true });
});

describe('context-save stamps the project identity', () => {
  test('checkpoint frontmatter gets the canonical remote and physical root; credentials never reach disk', () => {
    const secret = ['sentinel', 'pw', '55120'].join('-');
    const a = repo('a', `https://deploy-bot:${secret}@GitLab.com:8443/customer-a/product/repo.git`);
    const file = save(a, 'auth refactor', '20261001-100000');
    expect(file.startsWith(path.join(home, 'projects', 'product-repo-5eca1fe041984543', 'checkpoints'))).toBe(true);
    const text = fs.readFileSync(file, 'utf-8');
    const frontmatter = text.split('---')[1];
    expect(frontmatter).toContain('\nremote: gitlab.com/customer-a/product/repo\n');
    expect(frontmatter).toContain(`\nproject_root: ${a}\n`);
    expect(text).toContain('## Working on: auth refactor');
    const leaks = spawnSync('grep', ['-rl', secret, home], { encoding: 'utf-8', timeout: 10_000 });
    expect(leaks.stdout).toBe('');
  });

  test('re-stamping replaces stale identity lines instead of duplicating them', () => {
    const a = repo('a', 'git@gitlab.com:customer-a/product/repo.git');
    const file = save(a, 'x', '20261001-100000');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf-8').replace('remote: gitlab.com/customer-a/product/repo', 'remote: bogus'));
    const r = spawnSync('bash', [SLUG_BIN, '--stamp-checkpoint', file], { cwd: a, env: env(), encoding: 'utf-8', timeout: 30_000 });
    expect(r.status).toBe(0);
    const fm = fs.readFileSync(file, 'utf-8').split('---')[1];
    expect(fm.match(/^remote:/gm)?.length).toBe(1);
    expect(fm.match(/^project_root:/gm)?.length).toBe(1);
    expect(fm).toContain('remote: gitlab.com/customer-a/product/repo');
  });
});

describe('context-restore never presents another project checkpoint as latest', () => {
  test('nested groups: B restores after A saved — A is not presented, the old shared bucket is reported', () => {
    const a = repo('a', 'git@gitlab.com:customer-a/product/repo.git');
    const b = repo('b', 'https://gitlab.com/customer-b/product/repo.git');
    // Before the fix both projects filed into projects/product-repo/.
    legacyCheckpoint('product-repo', '20260901-090000-old-a-work.md');
    const aFile = save(a, 'customer a migration', '20261001-120000');

    const r = restore(b);
    expect(r.out).not.toContain(aFile);
    expect(r.out).not.toContain('old-a-work');
    expect(r.out).toContain('NO_CHECKPOINTS');
    expect(r.out).toContain('PROJECT_IDENTITY: gitlab.com/customer-b/product/repo');
    expect(r.out).toContain('LEGACY_BUCKET: projects/product-repo holds 1 earlier checkpoint(s)');

    const own = restore(a);
    expect(own.latest).toBe(aFile);
  });

  test('two projects still sharing one bucket: the foreign newer checkpoint is never "latest"', () => {
    // github.com/product/repo and gitlab.com/product/repo are 2-segment remotes
    // and so keep the same slug (product-repo); identity tells them apart.
    const gh = repo('gh', 'https://github.com/product/repo.git');
    const gl = repo('gl', 'git@gitlab.com:product/repo.git');
    const own = save(gl, 'gitlab work', '20261001-090000');
    const foreign = save(gh, 'github work', '20261001-110000');
    expect(path.dirname(own)).toBe(path.dirname(foreign));

    const r = restore(gl);
    expect(r.latest).toBe(own);
    expect(r.candidates).not.toContain(foreign);
    expect(r.lines).toContain(`FOREIGN ${foreign}`);
    expect(r.out).toContain('SHARED_BUCKET: 1 checkpoint(s) here were saved by another project');

    // With no checkpoint of its own, gh's view of gl's bucket shows nothing as latest.
    fs.rmSync(foreign);
    const other = restore(gh);
    expect(other.latest).toBeUndefined();
    expect(other.out).toContain('NO_VERIFIED_CHECKPOINTS');
    expect(other.lines).toContain(`FOREIGN ${own}`);
  });

  test('unstamped checkpoints: trusted in an unshared bucket, UNVERIFIED once another project wrote there', () => {
    const gh = repo('gh', 'https://github.com/product/repo.git');
    const gl = repo('gl', 'git@gitlab.com:product/repo.git');
    const old = legacyCheckpoint('product-repo', '20260901-090000-pre-stamp.md');

    expect(restore(gh).latest).toBe(old);

    const foreign = save(gl, 'gitlab work', '20261001-110000');
    const r = restore(gh);
    expect(r.latest).toBeUndefined();
    expect(r.lines).toContain(`UNVERIFIED ${old}`);
    expect(r.lines).toContain(`FOREIGN ${foreign}`);
  });

  test('same remote, different checkout (workspace handoff): restorable, with ROOT_DIFFERS as info', () => {
    const first = repo('workspace-1', 'git@github.com:acme/app.git');
    const second = repo('workspace-2', 'https://github.com/acme/app');
    const file = save(first, 'handoff', '20261001-100000', 'feat-x');
    const r = restore(second, 'main');
    expect(r.latest).toBe(file);
    expect(r.lines).toContain(`ROOT_DIFFERS ${file}`);
    expect(r.out).not.toContain('FOREIGN');
  });

  test('no remote: identity is the project root', () => {
    const one = repo('solo');
    const file = save(one, 'local only', '20261001-100000');
    expect(fs.readFileSync(file, 'utf-8')).not.toMatch(/^remote:/m);
    expect(restore(one).latest).toBe(file);

    const elsewhere = repo('elsewhere');
    const r = sh(RESTORE_BLOCK, elsewhere, { CURRENT_BRANCH: 'main', GSTACK_PROJECT_SLUG: 'solo' });
    expect(r.stdout).toContain('NO_VERIFIED_CHECKPOINTS');
    expect(r.stdout).toContain(`FOREIGN ${file}`);
  });
});

describe('gstack-slug --adopt-legacy', () => {
  function adopt(cwd: string, ...args: string[]) {
    const r = spawnSync('bash', [SLUG_BIN, '--adopt-legacy', ...args], {
      cwd,
      env: env(),
      encoding: 'utf-8',
      timeout: 30_000,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    return { stdout: r.stdout ?? '', status: r.status ?? -1 };
  }

  test('lists the old bucket with labels and copies only what is named; foreign and traversal refused', () => {
    const a = repo('a', 'git@gitlab.com:customer-a/product/repo.git');
    const b = repo('b', 'git@gitlab.com:customer-b/product/repo.git');
    const oldBucket = path.join(home, 'projects', 'product-repo');
    const unstamped = legacyCheckpoint('product-repo', '20260901-090000-unknown.md');
    // Stamped checkpoints in the old bucket (written by A and B), via the real stamp.
    const mine = legacyCheckpoint('product-repo', '20260902-090000-mine.md');
    const theirs = legacyCheckpoint('product-repo', '20260903-090000-theirs.md');
    spawnSync('bash', [SLUG_BIN, '--stamp-checkpoint', mine], { cwd: a, env: env(), timeout: 30_000 });
    spawnSync('bash', [SLUG_BIN, '--stamp-checkpoint', theirs], { cwd: b, env: env(), timeout: 30_000 });
    fs.writeFileSync(path.join(oldBucket, 'question-preferences.json'), '{"review-finding-fix":"never-ask"}');
    fs.writeFileSync(path.join(oldBucket, 'learnings.jsonl'), '{"x":1}\n');
    const before = spawnSync('bash', ['-c', 'find . -type f | sort | xargs cat | cksum'], { cwd: oldBucket, encoding: 'utf-8', timeout: 10_000 }).stdout;

    const list = adopt(a);
    expect(list.status).toBe(0);
    expect(list.stdout).toContain('checkpoints/20260902-090000-mine.md  [checkpoint: matching this project]');
    expect(list.stdout).toContain('checkpoints/20260903-090000-theirs.md  [checkpoint: another project (not copyable)]');
    expect(list.stdout).toContain('checkpoints/20260901-090000-unknown.md  [checkpoint: unknown project');
    expect(list.stdout).toContain('question-preferences.json  [no project identity');
    expect(list.stdout).toContain('Nothing copied.');
    const newBucket = path.join(home, 'projects', 'product-repo-5eca1fe041984543');
    expect(fs.existsSync(path.join(newBucket, 'question-preferences.json'))).toBe(false);

    const copy = adopt(
      a,
      '--copy',
      'checkpoints/20260902-090000-mine.md',
      'question-preferences.json',
      'checkpoints/20260903-090000-theirs.md',
      '../product-repo/learnings.jsonl',
    );
    expect(copy.stdout).toContain('COPIED checkpoints/20260902-090000-mine.md');
    expect(copy.stdout).toContain('COPIED question-preferences.json');
    expect(copy.stdout).toContain('SKIPPED checkpoints/20260903-090000-theirs.md');
    expect(copy.stdout).toContain('REFUSED ../product-repo/learnings.jsonl');
    expect(copy.status).toBe(1);
    expect(fs.readFileSync(path.join(newBucket, 'question-preferences.json'), 'utf-8')).toContain('never-ask');
    expect(fs.existsSync(path.join(newBucket, 'checkpoints', '20260903-090000-theirs.md'))).toBe(false);
    expect(fs.existsSync(path.join(newBucket, 'learnings.jsonl'))).toBe(false);
    expect(fs.existsSync(path.join(newBucket, 'checkpoints', path.basename(unstamped)))).toBe(false);

    // Never overwrites, never touches the old bucket.
    const again = adopt(a, '--copy', 'question-preferences.json');
    expect(again.stdout).toContain('SKIPPED question-preferences.json');
    const after = spawnSync('bash', ['-c', 'find . -type f | sort | xargs cat | cksum'], { cwd: oldBucket, encoding: 'utf-8', timeout: 10_000 }).stdout;
    expect(after).toBe(before);

    // The adopted checkpoint is now A's latest on restore.
    expect(restore(a).latest).toBe(path.join(newBucket, 'checkpoints', '20260902-090000-mine.md'));
  });

  test('a project whose slug did not change has nothing to adopt', () => {
    const gh = repo('gh', 'https://github.com/acme/app.git');
    const r = adopt(gh);
    expect(r.status).toBe(0);
    expect(r.stdout).toContain("Nothing to adopt: this project's slug (acme-app) did not change.");
  });
});
