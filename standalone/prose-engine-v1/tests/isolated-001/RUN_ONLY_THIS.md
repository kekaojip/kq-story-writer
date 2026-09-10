# RUN ONLY THIS — ISOLATED PROSE ENGINE TEST

## Hard Isolation

This test MUST run only from:

- branch: `design/prose-engine-v1`
- path: `standalone/prose-engine-v1/`

Do NOT read or use:

- repository root `START_HERE.md`
- `skills/story-writer-runtime/**`
- `skills/human-writing-l2/**`
- `input/current/**`
- `output/current/**`
- `archive/**`
- any Main workflow repository
- any existing novel project files

This is NOT a production Writer task.

## Task

Run Prose Engine V1 in `WRITE` mode on:

`tests/isolated-001/PROSE_PACKET.md`

Follow only the standalone module's own routing and runtime rules.

There is no approved Voice Corpus for this test, so use the module's natural modern Chinese baseline. Do not invent a benchmark author or style source.

## Output

Write the final prose to:

`standalone/prose-engine-v1/tests/isolated-001/OUTPUT.md`

For this first isolated test:

- generate the draft;
- run the standalone Blind Reader only;
- if there are genuine findings, allow at most one local repair under the standalone Repair rules;
- output only final fiction prose in `OUTPUT.md`;
- do not include analysis, scores, rule explanations, or test commentary in `OUTPUT.md`.

Stop after writing `OUTPUT.md`.
