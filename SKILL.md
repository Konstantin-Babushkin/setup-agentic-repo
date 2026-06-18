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
   - **Greenfield** (empty/near-empty): interview for the stack (see **Choosing the
     stack**), scaffold infra from scratch.
   - **Brownfield** (real codebase): inspect first. Walk the tree, detect stack +
     existing tooling, read the entry points and configs. Write down what you find
     — stack, how it's built/tested, gaps (no `verify` gate, no AGENTS.md, no
     import boundaries, missing tests). Seed docs from the code, fill gaps without
     clobbering what works, and surface a short list of improvements for the
     founder to approve before you touch anything.

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
There is no bootstrap script. Adapt the templates in `templates/` by hand to the
stack you land on — fill the slots, never overwrite a file that already exists.
The templates are a Python/Node reference shape, not a default to install blind.

3. **Static context — AGENTS.md.** `AGENTS.md` is the single canonical agent file;
   `CLAUDE.md` is only ever a symlink to it, never a separate file (all CLIs —
   Claude Code, Codex, Cursor — read the one file). Fill `templates/AGENTS.md.tmpl`
   → `AGENTS.md`, then `ln -sf AGENTS.md CLAUDE.md`. If a brownfield `CLAUDE.md`
   already exists, fold its content into `AGENTS.md` first, then replace it with
   the symlink — don't leave two files.
   Intent: a one-liner from the founder's idea (greenfield) or read from the code
   (brownfield) — the full spec comes from gsd next, this just needs the gist.
   Stack: see **Choosing the stack** below — greenfield, recommend from their
   answers; brownfield, detect and don't migrate. Keep AGENTS.md lean. Build the
   `docs/` tree — durable knowledge gsd doesn't own. Layout:

   ```
   docs/
   ├── CODING_VALUES.md     what code this project welcomes and rejects (the house style)
   ├── HOW_TO_DEVELOP.md     the founder's guide to the daily loop
   ├── architecture/         overview.md + decision_log.md + one dir per subsystem as they appear
   ├── requirements/         durable global requirements (functional, NFR, errors, security)
   ├── guides/               how-tos (run locally, deploy, onboard) — empty until there's one to write
   ├── ideas/                INDEX.md + TEMPLATE.md + <item>.md
   └── tech_debt/            INDEX.md + TEMPLATE.md + active/ + resolved/
   ```

   - `docs/CODING_VALUES.md` from `templates/CODING_VALUES.md.tmpl` — the house
     coding standard (vision, code values, boundaries, validation, state, failure,
     testing, logging, deps) agents read before writing and reviewers judge
     against. Fill the stack/domain slots; delete sections that don't apply yet.
   - `docs/HOW_TO_DEVELOP.md` from `templates/HOW_TO_DEVELOP.md.tmpl` — the human's
     guide to the daily loop (discuss → plan → review → execute in worktree →
     other-CLI review → land → verify). For the founder, not the agent; walk them
     through it once.
   - `docs/architecture/overview.md` (one-page system map) + `decision_log.md`
     (`Lxx`, stack as `L01`). As each real subsystem appears, give it its own dir
     `architecture/<subsystem>/` with: `strategy.md` (what it owns + why,
     boundaries, key decisions), `tactics.md` (patterns, data flow, contracts with
     other subsystems), `implementation.md` (modules, entry points, where things
     live), `errors_and_logging.md` (failure handling + observability), `tests.md`
     (what's covered + at which tier). A subsystem is whatever the repo is made of —
     not just "backend": a frontend feature area, a mobile module, an API service,
     a data pipeline, a CLI. Start a subsystem as a single file; promote to the dir
     when one file stops holding it. Don't pre-create dirs for subsystems that
     don't exist yet.
   - `docs/requirements/` — durable cross-phase requirements (functional, NFR,
     errors, security). gsd owns per-phase discovery + the roadmap in `.planning/`;
     this holds the stable global requirements that outlive a phase. Start with a
     short `README.md` saying what goes here; don't fabricate requirements.
   - `docs/guides/` — operational how-tos; create empty, fill when there's a real one.
   - capture system — `docs/ideas/` and `docs/tech_debt/` with the severity +
     resolved-lifecycle from `references/templates.md`. Brownfield: drop obvious
     existing debt into `active/` as you find it.

4. **Harness — the guarantees that make slop hard to pass** (foundation only —
   commands + configs). The *shape* is fixed; the *tools* follow the stack you
   chose in step 3. Don't install a stack the founder didn't land on.
   - Greenfield: build the shape for the chosen stack — one `make verify` gate
     (lint + typecheck + import-boundaries + test), one starter boundary contract
     that's valid immediately, one green smoke test, pre-commit. The Python/Node
     reference configs in `templates/harness/` show the shape; adapt them to the
     stack, or build the equivalent for a different one (see
     `templates/harness/README.md`, "A different stack?"). For Python init `uv`
     so configs are real; for Node init the package manager the founder will use.
   - Brownfield: detect existing tooling first. Wrap what's there behind a
     `make verify` gate if missing, add only the missing checks, do NOT replace
     working config. Existing checks may fail — log as tech_debt, don't loosen rules.
   The `Makefile` also ships `worktree.bootstrap` / `worktree.new` / `worktree.land`
   (parallel isolated work + safe landing — runs `make verify` before merging; see
   `references/worktree-workflow.md`). Run `make worktree.bootstrap` once.
   This is what makes "it works" mean "checks passed", and it's the gate gsd's
   agents must clear before any change counts as done. See `templates/harness/README.md`.

5. **Skill policy + room for project skills.** Fill the skill-policy section of
   `AGENTS.md`: gsd for workflow, caveman for text, ponytail for code, plus any
   domain skills. Then scaffold an empty home for skills *this project* will grow:
   `.ai_skills/` (tool-neutral, like `AGENTS.md` — every CLI reads the `SKILL.md`s
   as plain instructions; a CLI with native skill auto-load can symlink its own
   path at it, e.g. `ln -s ../.ai_skills .claude/skills`) with
   `templates/project-skills-README.md.tmpl` → `.ai_skills/README.md`. Leave it
   empty — don't pre-build speculative skills. Point the `AGENTS.md` skill policy
   at it so the building agent knows to add a skill (via `skill-creator`) when a
   project-specific workflow repeats, instead of re-deriving it each session.

6. **Commit the foundation.** Git init if needed, one semantic-checkpoint commit
   (`docs/` = durable knowledge; gsd `.planning/` = live state, they coexist).

7. **Now hand to gsd.** The infra is in place; gsd discusses + plans on top of it.
   - Greenfield: `gsd-new-project` — interviews the founder, writes the spec
     (`PROJECT.md`), requirements, and roadmap into `.planning/`.
   - Brownfield: `gsd-map-codebase` + `gsd-ingest-docs` to reconstruct intent and
     fold in existing docs.
   Then `gsd-plan-phase` for the first/next real change. gsd absent → stop after
   the commit, tell them to install it before planning.

## Anti-slop measures

Slop = plausible-but-unverified output that looks done — confident prose, code
that imports clean but was never run, a "fixed" claim with nothing behind it. The
founder can't read the code, so every measure here exists to make "done" mean
something they can trust without reading it. Slop runs in two directions: doing
**less** than the spec (cut corners, "fine for MVP", "not my job", silent stubs)
and doing **more** than the spec (speculative features, gold-plating, abstractions
nobody asked for). Both break the contract. The measures below fight both.

**This skill installs the measures; it does not perform them.** Each one lands as a
durable artifact in the repo — a gate check, a pre-commit hook, a rule in
`AGENTS.md`, or a skill-policy entry — so the agents that later *build* the product
follow it on every turn, long after this setup is done. Two enforcement kinds:
**machine-enforced** (the gate / hooks fail the change — preferred whenever the
rule is mechanizable) and **rule-enforced** (`AGENTS.md` loaded every turn for the
short version, with the full coding standard in `docs/CODING_VALUES.md` read on
demand — for the judgment calls a check can't make). When a measure isn't yet a
check, write it as a rule, not as a hope. The flow above
installs the must-haves; name them out loud so the founder knows what's protecting
them, and state which nice-to-haves you wired in or skipped and why.

### Must-have (the repo is not agent-ready without these)

- **One verify gate.** A single `make verify` running four required check
  classes with stack-native tools: lint, typecheck/contract-check,
  import-boundary lint, and tests. Without one canonical command, "done" drifts
  to whatever the agent felt like running. This is the spine every other measure
  hangs off.
- **Tests in the gate from day one.** A gate with no tests is theater — it goes
  green on code that does nothing. One green smoke test proves the wiring; new
  behavior ships with its tests in the same change, not a follow-up that never
  comes.
- **Pre-commit enforcement.** The gate must run at the commit boundary, not on
  the honor system. An optional check is a skipped check the moment an agent is in
  a hurry. This is what stops unverified code from entering history at all.
- **Strict system-prompt override.** The stock assistant is agreeable — it says
  "looks good!" and emits confident guesses. The strict prompt makes the agent
  flag unverified claims, mark `ASSUMPTION:`, and refuse to call work done it
  didn't check. Slop starts as a tone; this kills the tone.
- **AGENTS.md house rules.** Evidence-grounded claims, stop-and-ask on unverified
  APIs / conflicting evidence / destructive ops, simplest-thing-that-works,
  semantic-checkpoint commits. The standing brief every agent reads first, so the
  rules apply on turn one of every session, not just when remembered.
- **Decision log (`Lxx`).** Locked decisions in one file. Without it, each new
  session re-litigates the stack and quietly contradicts past choices — slow
  architectural drift that no single diff reveals. New choice → options + pick +
  log; don't re-open logged ones.
- **Import boundaries.** import-linter (Python) / dependency-cruiser or ESLint
  boundaries (JS). One valid contract from day one, grown as modules appear.
  Structural slop is invisible per-edit — it's the tangle that accumulates over
  fifty small "reasonable" imports. A machine-checked boundary is the only thing
  that catches it.
- **Cross-CLI review.** A second agent on a different model (e.g. Codex reviewing
  Claude's diff) before anything lands. An author can't catch the slop it
  rationalized into being — same blind spots wrote it and review it. An
  independent model breaks that loop. Run via `gsd-review` and wire it into the
  land step, not as an optional courtesy. This makes a second reviewer CLI part of
  setup — if one truly can't be installed (preflight refused), that's a logged gap
  the founder is told about, not a silent skip.
- **Capture system (`docs/ideas/`, `docs/tech_debt/`).** One file per deferred
  item + an INDEX. Fights the quiet-drop failure: an agent hits a known problem,
  buries it in its final prose, and it's lost the moment the session ends. For a
  founder who can't audit the code, an un-captured issue is an invisible one. The
  templates ship it; the AGENTS.md rule forces a file, not just a mention.
- **Discipline skills (caveman / ponytail).** Terse user-facing text (caveman),
  lazy/minimal code (ponytail). Slop scales with surface area — the most reliable
  way to ship fewer bugs is to ship less code and less prose. These keep the agent
  from padding both. Set them in the skill policy so they apply every turn, not
  when remembered.
- **Build to the spec — exactly** (`AGENTS.md` rule). Install the rule that the
  spec's acceptance criteria *are* the contract: implement every criterion, add
  nothing it didn't ask for, and treat "done" as each criterion demonstrably met —
  not a vibe. Over-delivery is a bug too: untested surface the founder never
  approved. The rule also names the deviation path — spec can't be built as
  written → stop and surface options, never silently reinterpret into something
  easier. gsd produces the spec + criteria; this rule binds the building agent to
  them.
- **No fake-done, no silent corner-cutting** (gate check + `AGENTS.md` rule).
  Machine half: wire a scan of changed files for unfinished-work markers into the
  gate, so a `TODO`, placeholder return, empty handler, stub exception,
  hardcoded-happy-path, or stack-equivalent marker can't ride in as "done". Rule
  half: install the `AGENTS.md` rule that "good enough for MVP" and "not my
  responsibility" don't excuse dropping error handling, edge cases, or input
  validation the spec implies — in scope by default; a corner-cut is allowed only
  as a logged `docs/tech_debt/` item with a trigger and the founder's sign-off,
  never a silent gap.
- **Typed/contracted boundaries — no untyped escape hatches.** Boundary data
  (request/response, external calls, stored shapes, event payloads) must have a
  machine-checked contract using the stack's native type/schema system. Python/TS:
  mypy-strict / tsc-strict and no `Any` / `dict[str, Any]` smuggling. Other stacks:
  use the strongest credible equivalent; if none exists, log the gap as tech debt
  and enforce the closest available contract check in `verify`.
- **Consistency with what's already there** (`AGENTS.md` rule + decision log).
  Install the rule that new code follows the repo's existing conventions — naming,
  structure, error model, file layout — so the codebase reads as one hand, not a
  fresh dialect each session. Brownfield: record the detected patterns so the
  building agent can match them; greenfield: set them in the decision log as they
  emerge. Predictable code is reviewable code; inconsistency is where bugs hide.
- **Reproducible build (committed lockfile).** Commit the lockfile; install
  latest-compatible once, then freeze. No floating `latest` that turns today's
  green build into tomorrow's mystery failure. Same inputs, same result is the
  precondition that makes every other check mean anything.

### Nice-to-have (raise the ceiling; add when the project earns it)

- **Worktree isolation + verify-before-land.** Parallel work in throwaway
  worktrees; `make worktree.land` runs `verify` before merging. Keeps a failing
  experiment from ever touching the mainline. Bundled in the harness already —
  cheap to keep.
- **CI mirror of the gate.** Run `make verify` in CI so the gate holds even if a
  local hook is bypassed. The local hooks are the real boundary at founder scale;
  CI is the backstop when there's more than one contributor.
- **Coverage gate.** Fail `verify` under a coverage floor. Stops tests that exist
  but assert nothing. Add once there's enough code that the floor is meaningful —
  too early and it just nags.

## Choosing the stack

The stack is a real, hard-to-reverse decision — log it as `L01`. Don't reach for
a default. Python and React/TS are the most common landing spots and safe when
nothing pulls against them, but pick from what the founder actually needs.

**Brownfield: don't choose, detect.** Read what's there (`templates/harness/README.md`
has the detection table) and record the real stack. Migrating an existing stack is
out of scope — note any mismatch as tech_debt, don't rewrite.

**Greenfield: interview, then recommend.** The founder is non-technical — ask
about the product and its users, not frameworks. One question at a time,
multiple-choice, plain language. Cover:

- **What is it?** Web app, mobile app, just-an-API/backend, desktop, CLI,
  automation/script. (Shapes whether there's a frontend at all.)
- **Who uses it and on what?** Public website visitors, signed-in users, internal
  team, other software calling an API. Phone-first or desktop-first?
- **How many, realistically?** A handful / hundreds / "I hope it goes viral."
  Don't over-build for scale that isn't coming — most ideas start small.
- **Anything non-negotiable?** Payments, login/accounts, file or photo uploads,
  real-time updates (chat/live), offline use, AI features, a deadline.
- **Constraints from their world?** A platform they're tied to, a language their
  future hires will know, a host they already pay for.

Then recommend ONE stack in plain terms, with the why and the tradeoff, framed so
they can say yes or push back:

> Sounds like a web app a few hundred people sign into, with payments. I'd suggest
> **Python (FastAPI) for the backend, React for the screens, Postgres to store
> data, Stripe for payments**. It's boring on purpose — huge community, easy to
> hire for, and AI agents write it well. Sound right, or do you have a preference?

Let scale and needs move the recommendation — a static marketing site doesn't need
React; an internal script needs no frontend; "must run on their phone offline"
changes everything. Once they confirm, that's `L01`, and the harness in step 4
follows it.

## Done

Infra committed first: `AGENTS.md` (+ `CLAUDE.md` symlink), `docs/`
(`CODING_VALUES.md`, `HOW_TO_DEVELOP.md`, `architecture/`, `requirements/`,
`guides/`, `ideas/`, `tech_debt/`), an empty `.ai_skills/` (+ README) for
project skills, a wired `make verify`.
The founder has seen `docs/HOW_TO_DEVELOP.md` and knows the loop. Then gsd runs on top and produces
the spec + roadmap in `.planning/`; next step is `gsd-plan-phase`. Greenfield:
`make verify` green on the smoke test. Brownfield: the gate runs; existing
failures logged as tech_debt, not silenced.

## Acceptance checks

The setup is correct when these hold — use them to self-check a run:

- Every must-have anti-slop measure is present and named to the founder; each
  skipped nice-to-have was a stated choice, not an omission.
- The gate enforces four required check classes, using the stack's native tools:
  lint, typecheck/contract-check, tests, and import-boundary lint. Python might
  use ruff + mypy + pytest + import-linter; TypeScript might use ESLint/Biome +
  tsc + a test runner + dependency-cruiser/ESLint boundaries. Other stacks must
  provide equivalent checks, not skip the category. If a stack has no credible
  native typecheck or import-boundary tool, log that as `docs/tech_debt/active/`
  and make the closest available contract check part of `verify`. Commit the
  lockfile or dependency pin file when the stack has one.
- Greenfield fuzzy idea → a short stack interview (product/users/scale, not
  frameworks) ending in ONE recommended stack logged as `L01`, then infra
  scaffolded for it. No broad product questionnaire wall — gsd does the deep
  spec discussion later.
- Greenfield → no stack installed before the founder confirmed it; Python/React
  used only when their answers point there, not as a default.
- Brownfield → you inspected and wrote down the real stack, tooling, and gaps, and
  surfaced an improvements list before changing anything.
- Brownfield with existing `CLAUDE.md`/`AGENTS.md`/`Makefile` → you never clobber
  them: merge by hand using the detection table in `templates/harness/README.md`
  (the merge is judgment). End state has ONE `AGENTS.md` with `CLAUDE.md` a symlink
  to it — an existing standalone `CLAUDE.md` is folded into `AGENTS.md`, not kept.
- Brownfield with failing tests → you log the failures to `docs/tech_debt/active/`;
  the gate is NOT weakened to go green.
- gsd not installed → infra committed, stop before planning, tell them to install.
- Existing `Makefile` → you point `make verify` at the existing checks; don't
  replace them.

## References

- `references/context-engineering.md` — six context types, static vs dynamic.
- `references/cli-setup.md` — system-prompt override + skills install, per CLI.
- `references/templates.md` — docs, decision log, capture skeletons.
- `references/worktree-workflow.md` — parallel isolated work + safe landing.
- `templates/AGENTS.md.tmpl` — static-context file to fill.
- `templates/CODING_VALUES.md.tmpl` — the house coding standard, → `docs/CODING_VALUES.md`.
- `templates/HOW_TO_DEVELOP.md.tmpl` — human guide to the daily loop, → `docs/HOW_TO_DEVELOP.md`.
- `templates/project-skills-README.md.tmpl` — README for the empty `.ai_skills/`
  home where project-specific skills get added later.
- `templates/strict-engineer-system-prompt.md` — starting system-prompt override.
- `templates/harness/` — reference command surface + configs (Python/Node shape);
  adapt to the chosen stack, including "A different stack?" for everything else.
