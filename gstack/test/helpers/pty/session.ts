/**
 * The one PTY session loop (runPtySession) and its launch seam (PtyDriver).
 * Owns launch, the poll/deadline loop, failure capture and close/cleanup
 * ordering; each runner in pty/runners/ supplies its policy as a PtySessionPlan
 * (start, poll, tick, timeout, capture hooks). New runner: build a plan and
 * `return runPtySession(plan)`; tests pass the fake driver from fake-session.ts.
 * Size ratchet (c) binds this module. Moved from the three runner loops of the
 * former claude-pty-runner.ts. Tests import through claude-pty-runner.ts.
 */
import { launchClaudePty, type ClaudePtyOptions, type ClaudePtySession } from './launch';

/**
 * The runners' launch seam: how a session starts, and the clock the runner
 * loop reads. Omitted in production (real launcher, Date.now,
 * performance.now, Bun.sleep); tests pass the fake driver from
 * test/helpers/pty/fake-session.ts.
 */
export interface PtyDriver {
  launch(opts: ClaudePtyOptions): Promise<ClaudePtySession>;
  /** Wall clock, Date.now() semantics. */
  now(): number;
  /** Monotonic clock, performance.now() semantics. */
  monotonic(): number;
  sleep(ms: number): Promise<void>;
}

export const realPtyDriver: PtyDriver = {
  launch: opts => launchClaudePty(opts),
  now: () => Date.now(),
  monotonic: () => performance.now(),
  sleep: ms => Bun.sleep(ms),
};

/** One poll step: finish with a result, keep polling, or end the loop as a timeout. */
export type PtyStep<R> = { done: R } | 'continue' | 'break';

export interface PtySessionPlan<R> {
  driver: PtyDriver;
  launch: ClaudePtyOptions;
  /** Owned fixture cleanup; runs after close, and when launch itself fails. */
  cleanup?: () => void;
  /** Boot and command submission. A returned result ends the run before polling. */
  start(session: ClaudePtySession): Promise<R | undefined>;
  /** Wait for the next poll. False means the deadline passed: the run times out. */
  poll(session: ClaudePtySession): Promise<boolean>;
  tick(session: ClaudePtySession): Promise<PtyStep<R>>;
  timeout(session: ClaudePtySession): R;
  /** Snapshot a thrown run before close; the original error is rethrown. */
  onError?(session: ClaudePtySession, error: unknown): void;
  /** Always runs before close. A throw here fails an otherwise successful run. */
  beforeClose?(session: ClaudePtySession, failure: { error: unknown } | undefined): void;
  /** Close failed after a successful run; the close error is rethrown. */
  onCloseError?(session: ClaudePtySession, error: unknown): void;
}

/**
 * launch → start → (poll → tick)* → timeout, with one failure contract: a
 * run's own error wins over capture and close errors, close always runs, and
 * owned cleanup runs last.
 */
export async function runPtySession<R>(plan: PtySessionPlan<R>): Promise<R> {
  let session: ClaudePtySession;
  try {
    session = await plan.driver.launch(plan.launch);
  } catch (error) {
    plan.cleanup?.();
    throw error;
  }
  let failure: { error: unknown } | undefined;
  try {
    const early = await plan.start(session);
    if (early !== undefined) return early;
    while (await plan.poll(session)) {
      const step = await plan.tick(session);
      if (step === 'break') break;
      if (step !== 'continue') return step.done;
    }
    return plan.timeout(session);
  } catch (error) {
    failure = { error };
    plan.onError?.(session, error);
    throw error;
  } finally {
    try {
      try { plan.beforeClose?.(session, failure); }
      catch (error) { if (!failure) { failure = { error }; throw error; } }
      finally {
        try { await session.close(); }
        catch (error) { if (!failure) { plan.onCloseError?.(session, error); throw error; } }
      }
    } finally { plan.cleanup?.(); }
  }
}
