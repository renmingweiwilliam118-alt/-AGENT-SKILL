import { afterEach, describe, expect, test } from "bun:test";
import fs from "fs";
import path from "path";

import {
  DEFAULT_DESIGN_MODELS,
  DESIGN_MODEL_ENV,
  IMAGE_TOOL_MODEL,
  imagePairingProblem,
  imageRequestBody,
} from "../src/models";

// Tripwire for the image_generation orchestrator/tool pairing.
//
// History: v1.43.2.0 (66f3a180) pinned the tool to `gpt-image-2` under a
// `gpt-4o` orchestrator, a 400 on the Responses API that took every image
// command offline (#1771); v1.64.0.0 (#2571) dropped the pin, which made the
// tool fall back to `gpt-image-1`. OpenAI shuts gpt-image-1 down on
// 2026-10-23 (replacement: gpt-image-2), so an unpinned tool is a dead
// pairing too (#2807).
//
// The contract now: every image call goes through models.ts's
// imageRequestBody(), which pins the tool to IMAGE_TOOL_MODEL (gpt-image-2)
// under a gpt-5-class orchestrator and refuses, before sending, an
// orchestrator that cannot drive it (gpt-4o and older).
// design/test/models.test.ts drives each of the five call sites and checks
// the body each one actually sends.

const DESIGN_SRC = path.join(import.meta.dir, "..", "src");
const sources = fs
  .readdirSync(DESIGN_SRC)
  .filter((f) => f.endsWith(".ts"))
  .map((f) => ({ rel: `src/${f}`, body: fs.readFileSync(path.join(DESIGN_SRC, f), "utf-8") }));

const savedOverride = process.env[DESIGN_MODEL_ENV];
afterEach(() => {
  if (savedOverride === undefined) delete process.env[DESIGN_MODEL_ENV];
  else process.env[DESIGN_MODEL_ENV] = savedOverride;
});

describe("design image-generation tool/orchestrator pairing (#1771, #2807)", () => {
  test("the default pairing is a gpt-5-class orchestrator with the tool pinned to gpt-image-2", () => {
    delete process.env[DESIGN_MODEL_ENV];
    expect(DEFAULT_DESIGN_MODELS.image).toMatch(/^gpt-(?:5|6)/);
    expect(IMAGE_TOOL_MODEL).toBe("gpt-image-2");
    expect(imagePairingProblem(DEFAULT_DESIGN_MODELS.image)).toBeNull();
    const body = JSON.parse(imageRequestBody("a login page", { size: "1536x1024", quality: "high" }));
    expect(body.model).toBe(DEFAULT_DESIGN_MODELS.image);
    expect(body.tools).toEqual([{ type: "image_generation", model: "gpt-image-2", size: "1536x1024", quality: "high" }]);
  });

  test("gpt-4o (and older) + gpt-image-2 is refused before any request, naming GSTACK_DESIGN_MODEL", () => {
    for (const old of ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "chatgpt-4o-latest"]) {
      expect(imagePairingProblem(old)).toContain(DESIGN_MODEL_ENV);
      process.env[DESIGN_MODEL_ENV] = old;
      expect(() => imageRequestBody("x", { size: "1024x1024", quality: "low" })).toThrow(DESIGN_MODEL_ENV);
    }
    process.env[DESIGN_MODEL_ENV] = "gpt-5.6-sol";
    expect(() => imageRequestBody("x", { size: "1024x1024", quality: "low" })).not.toThrow();
  });

  for (const { rel, body } of sources.filter((s) => s.rel !== "src/models.ts")) {
    test(`${rel}: image calls pin the tool model through imageRequestBody`, () => {
      // An image_generation tool spec written outside models.ts could omit the
      // tool model (→ gpt-image-1) or pair it with an old orchestrator.
      expect(/type:\s*["'`]image_generation["'`]/.test(body), `${rel} builds its own image_generation tool spec`).toBe(false);
      expect(body.includes(`model: "gpt-image-`), `${rel} pins an image model outside models.ts`).toBe(false);
      if (body.includes("/v1/responses")) {
        expect(body.includes("imageRequestBody("), `${rel} calls the Responses API without imageRequestBody()`).toBe(true);
      }
    });
  }
});
