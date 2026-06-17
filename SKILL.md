---
name: setup-agentic-repo
description: >-
  Guided setup that turns a fuzzy product idea into an AI-agent-ready repository
  for a non-technical founder — and equally sets up agentic infrastructure on an
  existing (brownfield) codebase. Use this whenever someone wants to start a new
  project they will build mostly with AI coding agents, OR wants to make an
  existing repo agent-ready; asks to "set up a repo for AI agents", "make my
  project agent-ready", "add AGENTS.md / context docs / a verification harness",
  "vibe coding setup", how to write a spec an AI can follow, or about context
  engineering foundations. Trigger it even when they only describe an idea ("I
  want to build an app that does X") or point at a codebase and clearly need the
  agentic scaffolding. It sets up the repo infrastructure — a context-engineered
  AGENTS.md, a docs skeleton, and a test/lint/type/import harness — then hands the
  spec and roadmap off to the gsd planning skills (gsd does the discussion).
---

# Setup Agentic Repo

Take a non-technical founder from idea to a repo set up for *agentic
engineering*: the agent implements, inside clear intent + durable context +
automatic verification. Frame = **context engineering**: write what a new
teammate would need, where an agent reads it automatically. Read
`references/context-engineering.md` once to explain it in their words.

## Welcome (show this first)

Present this, then go one step at a time. Don't dump the whole flow as a wall.

> Here's what we'll set up:
>
> ```
> [ CLI + system prompt ]  replace the agreeable default prompt with a strict one
> [ Skills              ]  gsd-redux (plan/build), caveman (text), ponytail (code)
> [ Repo context        ]  AGENTS.md + docs/  = what the agent reads first
> [ Harness             ]  lint + types + tests + import boundaries = slop can't pass
> [ gsd: discuss + plan ]  idea -> spec -> roadmap, on top of the infra above
> ```
>
> Flow: `infra (skills + AGENTS.md + docs + harness) -> gsd discuss + plan -> build loop`
> We set up the guarantees first, so nothing sloppy slips through later.

## Communication

The founder may know what git, markdown, and linters are, but won't operate them
by hand — you do the mechanics and explain in plain terms. One question at a time;
multiple-choice over open-ended. Name each artifact in one plain sentence. State
safe defaults instead of asking them to choose blind. Never make them copy-paste
commands.

## Flow

0. **Orient → pick mode.** existing code/docs/tooling? Read what's there, then set the mode — it changes a few steps below:
   - **Greenfield** (empty/near-empty): recommend stack, scaffold infra from scratch.
   - **Brownfield** (real codebase): detect stack + existing tooling, seed docs from the code, fill gaps without clobbering what works.

**Runtime preflight (steps 1-2) is OPTIONAL and home-level — it must not block the
repo foundation.** If a CLI install fails or is refused, note it and continue;
steps 3-6 (the repo foundation) are mandatory and stand on their own.

1. **CLI + system prompt.** Confirm their CLI (Claude Code or Codex) and install a
   strict-engineering system-prompt override so the agent's baseline behavior is
   right everywhere. How-to per CLI: `references/cli-setup.md`.

2. **Skills.** Install the three the project relies on: **gsd-redux**
   (plan/build/verify workflow), **caveman** (terse user-facing text),
   **ponytail** (lazy/minimal code). Install steps + how they're used:
   `references/cli-setup.md`.

Set up the infra (steps 3-6) BEFORE handing to gsd, so gsd's planning and its
executor agents inherit the house rules and run inside the verification gate.
Prefer the bootstrap script (`scripts/bootstrap_agentic_repo.py`) over hand-copying
templates — it fills slots and never overwrites. Run with `--dry-run` first.

3. **Static context — AGENTS.md.** Fill `templates/AGENTS.md.tmpl` → `AGENTS.md`,
   then `ln -s AGENTS.md CLAUDE.md` (if `CLAUDE.md` exists, merge — don't clobber).
   Intent: a one-liner from the founder's idea (greenfield) or read from the code
   (brownfield) — the full spec comes from gsd next, this just needs the gist.
   Stack: recommend the default (greenfield, Python/FastAPI + Postgres + React/TS)
   or detect it (brownfield, don't migrate). Keep AGENTS.md lean. Add the durable
   knowledge gsd doesn't own:
   - `docs/architecture/overview.md` — one-page system map.
   - `docs/architecture/decision_log.md` — `Lxx`, stack as `L01`.
   - capture system — `docs/ideas/` (`INDEX.md` + `TEMPLATE.md`) and
     `docs/tech_debt/` (`INDEX.md` + `TEMPLATE.md` + `active/` + `resolved/`),
     with the severity + resolved-lifecycle from `references/templates.md`.
     Brownfield: drop obvious existing debt into `active/` as you find it.
   Also write `OPERATING.md` to the repo root from `templates/OPERATING.md.tmpl` —
   the human's guide to the daily loop (discuss → plan → review → execute in
   worktree → other-CLI review → land → verify). This is for the founder, not the
   agent; walk them through it once.

4. **Harness — the guarantees that make slop hard to pass** (foundation only —
   commands + configs).
   - Greenfield: copy/adapt `templates/harness/` — `Makefile`
     (`make verify` = lint+typecheck+lint-imports+test, the gate), Ruff+mypy /
     Biome+tsc, import-linter with one starter boundary contract, one green smoke
     test, `.pre-commit-config.yaml`. Init `uv` so configs are real.
   - Brownfield: detect existing tooling first. Wrap what's there behind a
     `make verify` gate if missing, add only the missing checks, do NOT replace
     working config. Existing checks may fail — log as tech_debt, don't loosen rules.
   The `Makefile` also ships `worktree.bootstrap` / `worktree.new` / `worktree.land`
   (parallel isolated work + safe landing — runs `make verify` before merging; see
   `references/worktree-workflow.md`). Run `make worktree.bootstrap` once.
   This is what makes "it works" mean "checks passed", and it's the gate gsd's
   agents must clear before any change counts as done. See `templates/harness/README.md`.

5. **Skill policy.** Fill the skill-policy section of `AGENTS.md`: gsd for
   workflow, caveman for text, ponytail for code, plus any domain skills.

6. **Commit the foundation.** Git init if needed, one semantic-checkpoint commit
   (`docs/` = durable knowledge; gsd `.planning/` = live state, they coexist).

7. **Now hand to gsd.** The infra is in place; gsd discusses + plans on top of it.
   - Greenfield: `gsd-new-project` — interviews the founder, writes the spec
     (`PROJECT.md`), requirements, and roadmap into `.planning/`.
   - Brownfield: `gsd-map-codebase` + `gsd-ingest-docs` to reconstruct intent and
     fold in existing docs.
   Then `gsd-plan-phase` for the first/next real change. gsd absent → stop after
   the commit, tell them to install it before planning.

## Done

Infra committed first: `AGENTS.md` (+ `CLAUDE.md` symlink), `OPERATING.md` (human
loop guide), `docs/` (overview, decision log, capture), a wired `make verify`.
The founder has seen `OPERATING.md` and knows the loop. Then gsd runs on top and produces
the spec + roadmap in `.planning/`; next step is `gsd-plan-phase`. Greenfield:
`make verify` green on the smoke test. Brownfield: the gate runs; existing
failures logged as tech_debt, not silenced.

## Acceptance checks

The setup is correct when these hold — use them to self-check a run:

- Greenfield fuzzy idea → infra scaffolded, no broad questionnaire wall (gsd does
  the deep discussion later).
- Brownfield with existing `CLAUDE.md`/`AGENTS.md`/`Makefile` → the script never
  clobbers them: it skips and reports each. YOU then merge by hand using the
  detection table in `templates/harness/README.md` (the merge is judgment, not
  automated).
- Brownfield with failing tests → YOU log the failures to `docs/tech_debt/active/`
  (the script doesn't run them); the gate is NOT weakened to go green.
- gsd not installed → infra committed, stop before planning, tell them to install.
- Existing `Makefile` → you point `make verify` at the existing checks; don't
  replace them.

## References

- `references/context-engineering.md` — six context types, static vs dynamic.
- `references/cli-setup.md` — system-prompt override + skills install, per CLI.
- `references/templates.md` — docs, decision log, capture skeletons.
- `references/worktree-workflow.md` — parallel isolated work + safe landing.
- `templates/AGENTS.md.tmpl` — static-context file to fill.
- `templates/OPERATING.md.tmpl` — human guide to the daily loop.
- `templates/strict-engineer-system-prompt.md` — starting system-prompt override.
- `templates/harness/` — default-stack command surface, configs, notes.
- `scripts/bootstrap_agentic_repo.py` — scaffolds infra (slot-fill, never
  overwrites, `--dry-run`, `--self-check`). Prefer over hand-copying templates.
