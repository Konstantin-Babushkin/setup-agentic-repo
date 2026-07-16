# Anti-Slop Measures — Rationale

Full "why" behind each row in SKILL.md's Anti-slop measures tables. Read on demand — not needed to run the flow, only for judgment calls or explaining a measure to the founder.

## What is slop

Plausible-but-unverified output that looks done — confident prose, code that imports clean but never ran, a "fixed" claim with nothing behind it. Founder can't read the code, so every measure here makes "done" mean something trustable without reading it. Slop runs two directions: doing **less** than spec (cut corners, "fine for MVP", "not my job", silent stubs) and doing **more** than spec (speculative features, gold-plating, abstractions nobody asked for). Both break the contract.

## Enforcement model

This skill installs the measures; it doesn't perform them. Each lands as a durable artifact in the repo — gate check, pre-commit hook, rule in `AGENTS.md`, or skill-policy entry — so agents later *building* the product follow it every turn, long after setup is done.

Two enforcement kinds:
- **Machine-enforced** — gate/hooks fail the change. Preferred whenever the rule is mechanizable.
- **Rule-enforced** — `AGENTS.md` (loaded every turn, short version) + `docs/CODING_VALUES.md` (full standard, read on demand) — for judgment calls a check can't make.

A measure that isn't yet a check gets written as a rule, not left as a hope.

## Must-have

- **One verify gate.** Without one canonical command, "done" drifts to whatever the agent felt like running. This is the spine every other measure hangs off.
- **Tests in gate from day one.** A gate with no tests is theater — it goes green on code that does nothing.
- **Pre-commit enforcement.** An optional check is a skipped check the moment an agent is in a hurry.
- **Strict system-prompt override.** The stock assistant is agreeable — "looks good!", confident guesses. Slop starts as a tone; this kills the tone.
- **AGENTS.md house rules.** The standing brief every agent reads first, so rules apply turn one of every session, not just when remembered.
- **Decision log (`Lxx`).** Without it, each new session re-litigates the stack and quietly contradicts past choices — slow architectural drift no single diff reveals.
- **Import boundaries.** Structural slop is invisible per-edit — it's the tangle that accumulates over fifty small "reasonable" imports. A machine-checked boundary is the only thing that catches it.
- **Cross-CLI review.** An author can't catch the slop it rationalized into being — same blind spots wrote it and review it. An independent model breaks that loop.
- **Capture system.** Fights the quiet-drop failure: an agent hits a known problem, buries it in final prose, and it's lost the moment the session ends. An un-captured issue is invisible to a founder who can't audit code.
- **Discipline skills (caveman/ponytail).** Slop scales with surface area — the most reliable way to ship fewer bugs is to ship less code and less prose.
- **Build to spec — exactly.** Over-delivery is a bug too: untested surface the founder never approved. Deviation path: spec can't be built as written → stop, surface options, never silently reinterpret into something easier.
- **No fake-done, no silent corner-cutting.** "Good enough for MVP" and "not my job" don't excuse dropping error handling, edge cases, or input validation the spec implies — in scope by default. A corner-cut is allowed only as a logged tech-debt item with the founder's sign-off, never a silent gap.
- **Typed/contracted boundaries.** No untyped escape hatches at request/response, external-call, stored-shape, or event-payload boundaries.
- **Consistency with what's already there.** Predictable code is reviewable code; inconsistency is where bugs hide.
- **Reproducible build.** No floating `latest` turning today's green build into tomorrow's mystery failure. Same inputs, same result is the precondition that makes every other check mean anything.

## Nice-to-have

- **Worktree isolation + verify-before-land.** Keeps a failing experiment from ever touching mainline. Bundled in the harness already — cheap to keep.
- **CI mirror of the gate.** Local hooks are the real boundary at founder scale; CI is the backstop once there's more than one contributor.
- **Coverage gate.** Add once there's enough code that the floor is meaningful — too early and it just nags.
- **Continuous AI audit (Enji Guard).** Catches what a local-only gate can't (deployed-app checks, drift across sessions) — an always-on second QA pass with no local upkeep.
