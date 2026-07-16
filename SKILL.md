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

Idea → repo ready for *agentic engineering*: agent works inside clear intent, durable context, automatic verification. Frame: **context engineering** — read `references/context-engineering.md` once, explain to the founder in their words.

## Welcome (show this first)

Present in Russian, one step at a time — not the whole flow as a wall. Translate labels below, keep the box shape:

> Вот что мы настроим:
>
> ```
> [ Права доступа          ]  отключим запросы подтверждения на каждую команду — с вашего согласия
> [ CLI + системный промпт ]  заменим сговорчивый промпт по умолчанию на строгий
> [ Навыки (skills)        ]  gsd-redux (план/сборка), caveman (текст), ponytail (код)
> [ Контекст репозитория   ]  AGENTS.md + docs/ = что агент читает первым делом
> [ Харнесс                ]  lint + типы + тесты + границы импортов = слоп не пройдёт
> [ Push + AI QA           ]  push в GitHub, подключим Enji Guard для непрерывного аудита
> [ gsd: обсуждение + план ]  идея -> спецификация -> роадмап, поверх этой инфры
> ```
>
> Порядок: `инфра (навыки + AGENTS.md + docs + харнесс) -> push + Enji Guard -> обсуждение и план gsd -> цикл сборки`
> Сначала настраиваем гарантии, чтобы потом ничего сырое не проскочило.

## Communication

Founder won't operate tools by hand — you do the mechanics, explain in plain terms. One question at a time, multiple-choice over open-ended. Name each artifact in one sentence. State safe defaults instead of asking blind. Never make them copy-paste commands.

**Language: Russian for the founder.** All founder-facing text (chat, Welcome banner, questions, stack interview + recommendation, status updates, Done wrap-up) is in Russian; tool/file names, commands, paths stay untranslated. `docs/HOW_TO_DEVELOP.md` ships in Russian too (template pre-translated). Engineering artifacts stay English regardless of founder's language — `AGENTS.md`, `docs/CODING_VALUES.md`, `docs/architecture/`, `decision_log.md`, `docs/ideas/`, `docs/tech_debt/`, code, comments, commits — read cross-CLI and cross-session by agents, not just this founder.

## Close every gap — never assume a comeback

A flagged gap only the agent remembers does not exist to a non-technical founder — they won't scroll back for it and won't reopen a skill run to finish it later. Hit a gap → stop and put the fork to the founder plainly, don't pick for them: "X didn't work — `<one-line reason>`. Fix it now, or skip it?" Every install failure, refused step, or nice-to-have not done ends this run in one of two states the founder picked, no third option:

- **Fixed** — founder chose fix; done before moving on.
- **Skipped** — founder chose skip, told what's missing and why, and it's written as a `docs/tech_debt/` item (severity `must` unless trivial) — this applies to setup-time gaps too (refused CLI override, skills not installed, push/Enji not connected), not just code debt. A skip only the agent decided is not a skip, it's a silent gap.

No fix possible this session (their own OAuth click, a permission only they hold) → say so; skip is the only path, but it's still their call to log, not the agent's to assume.

Before Done, every step that could have failed or been skipped (1, 2, 4-brownfield, 7) must be confirmed as Fixed or founder-confirmed-Skipped — "log it and move on" without asking the founder fix-or-skip is not a valid outcome.

## Flow

0. **Orient → pick mode.** Existing code/docs/tooling? Read what's there, set mode:
   - **Greenfield** (empty/near-empty): interview for stack (see **Choosing the stack**), scaffold infra from scratch. Interview done, stack confirmed as `L01` → go straight to step 1, don't drift into building or deeper discussion first.
   - **Brownfield** (real codebase): inspect first — walk the tree, detect stack + tooling, read entry points + configs. Write down findings: stack, how it's built/tested, gaps (no `verify` gate, no AGENTS.md, no import boundaries, missing tests). Seed docs from code, fill gaps without clobbering what works, surface a short improvements list for the founder to approve before touching anything. Then step 1.

**Step 1 is mandatory — not optional, not skippable because the conversation moved on to the idea/stack.** The only valid skip is the CLI install itself technically failing or being refused — ask the founder fix-or-skip, log the outcome as tech_debt (see *Close every gap*), then continue. Step 2 (skills) is optional, home-level — don't let it block the repo foundation; same rule on failure: ask fix-or-skip, log the outcome, don't leave it unstated. Steps 3-6 (repo foundation) are mandatory and stand on their own.

1. **Permissions + CLI + system prompt.** Confirm their CLI (Claude Code or Codex), and *first* ask them to switch the session to full permission bypass (no per-command approval prompts) — do this before touching anything else in this step, since installing the system-prompt override is itself a write the CLI would otherwise stop and ask permission for. Say plainly what bypass means — the agent can run any command unattended for the session — so they say yes knowing the tradeoff. Decline → normal prompting continues, install the override through whatever prompts that takes; that's their call, not a gap, don't push twice. Once permissions are settled, install the strict-engineering system-prompt override. Do this before any infra work, immediately after step 0 — a good founder conversation is not a reason to defer it. How-to per CLI: `references/cli-setup.md`.

2. **Skills.** Install **gsd-redux** (plan/build/verify workflow), **caveman** (terse text), **ponytail** (lazy/minimal code). Install steps: `references/cli-setup.md`.

Set up infra (steps 3-6) before handing to gsd, so its planning + executor agents inherit the house rules and run inside the verification gate. No bootstrap script — adapt templates in `templates/` by hand: fill slots, never overwrite a file that already exists. Templates are a Python/Node reference shape, not a default to install blind.

3. **Static context — AGENTS.md.** `AGENTS.md` is the single canonical agent file; `CLAUDE.md` is only ever a symlink to it (all CLIs — Claude Code, Codex, Cursor — read one file). Fill `templates/AGENTS.md.tmpl` → `AGENTS.md`, then `ln -sf AGENTS.md CLAUDE.md`. Brownfield with existing `CLAUDE.md` → fold its content into `AGENTS.md` first, then replace with the symlink — don't leave two files.
   Intent: one-liner from the founder's idea (greenfield) or read from code (brownfield) — gsd writes the full spec next. Stack: see **Choosing the stack** — greenfield recommends from answers, brownfield detects, doesn't migrate. Keep AGENTS.md lean. Build the `docs/` tree — durable knowledge gsd doesn't own:

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

   - `docs/CODING_VALUES.md` from `templates/CODING_VALUES.md.tmpl` — house coding standard (vision, code values, boundaries, validation, state, failure, testing, logging, deps); agents read before writing, reviewers judge against it. Fill stack/domain slots, delete sections that don't apply yet.
   - `docs/HOW_TO_DEVELOP.md` from `templates/HOW_TO_DEVELOP.md.tmpl` — the founder's guide to the daily loop (discuss → plan → review → execute in worktree → other-CLI review → land → verify). For the founder, not the agent; walk them through once.
   - `docs/architecture/overview.md` (one-page system map) + `decision_log.md` (`Lxx`, stack as `L01`). Each real subsystem gets its own dir `architecture/<subsystem>/`: `strategy.md` (what it owns + why, boundaries, key decisions), `tactics.md` (patterns, data flow, contracts with other subsystems), `implementation.md` (modules, entry points, where things live), `errors_and_logging.md` (failure handling + observability), `tests.md` (covered + at which tier). Subsystem = whatever the repo is made of — not just "backend": frontend feature area, mobile module, API service, data pipeline, CLI. Start as a single file, promote to a dir once that file stops holding it. Don't pre-create dirs for subsystems that don't exist yet.
   - `docs/requirements/` — durable cross-phase requirements (functional, NFR, errors, security). gsd owns per-phase discovery + roadmap in `.planning/`; this holds stable global requirements outliving a phase. Start with a short `README.md`; don't fabricate requirements.
   - `docs/guides/` — operational how-tos; create empty, fill when a real one exists.
   - capture system — `docs/ideas/` and `docs/tech_debt/` with severity + resolved-lifecycle from `references/templates.md`. Brownfield: drop obvious existing debt into `active/` as found.

4. **Harness — the guarantees that make slop hard to pass** (foundation only — commands + configs). Shape is fixed; tools follow the stack chosen in step 3. Don't install a stack the founder didn't land on.
   - Greenfield: build the shape for the chosen stack — one `make verify` gate (lint + typecheck + import-boundaries + test), one starter boundary contract valid immediately, one green smoke test, pre-commit. Python/Node reference configs in `templates/harness/` show the shape; adapt to your stack or build the equivalent (see `templates/harness/README.md`, "A different stack?"). Python: init `uv` so configs are real; Node: init the founder's package manager.
   - Brownfield: detect existing tooling first. Wrap what's there behind `make verify` if missing, add only missing checks, don't replace working config. Existing checks may fail — log as tech_debt, don't loosen rules.
   `Makefile` also ships `worktree.bootstrap` / `worktree.new` / `worktree.land` (parallel isolated work + safe landing — runs `make verify` before merge; see `references/worktree-workflow.md`). Run `make worktree.bootstrap` once. This makes "it works" mean "checks passed" — the gate gsd's agents must clear before any change counts as done. See `templates/harness/README.md`.

5. **Skill policy + room for project skills.** Fill AGENTS.md's skill-policy section: gsd for workflow, caveman for text, ponytail for code, plus domain skills. Scaffold `.ai_skills/` — tool-neutral home for skills *this project* will grow (every CLI reads its `SKILL.md`s as plain instructions; a CLI with native skill auto-load can symlink it, e.g. `ln -s ../.ai_skills .claude/skills`) — with `templates/project-skills-README.md.tmpl` → `.ai_skills/README.md`. Leave it empty — don't pre-build speculative skills. Point AGENTS.md's skill policy at it so the building agent adds a skill (via `skill-creator`) when a project-specific workflow repeats, instead of re-deriving it each session.

6. **Commit the foundation.** Git init if needed, one semantic-checkpoint commit (`docs/` = durable knowledge; gsd's `.planning/` = live state — they coexist).

7. **Push to remote + connect AI QA (Enji Guard).** Get the foundation onto a remote, switch on continuous AI auditing before the build loop starts.
   - No remote yet: `gh repo create` (or ask the founder for an existing repo URL), then `git push -u origin main`. No `gh` / no GitHub access → ask the founder fix-or-skip (install `gh` / provide access, or defer), log the outcome as tech_debt, move on, don't block.
   - Point the founder at `https://guard.enji.ai/app` to connect the repo via GitHub App (revocable, no code changes) and run the free initial audit — continuous security / dependency-hygiene / test-coverage / AI-readiness auditing, findings land as GitHub issues + reviewable PRs with safe autofixes. This is their OAuth click in the browser, not scriptable — hand them the link, explain what it's for, wait for a yes/no, log whichever it is.
   Optional like the runtime preflight (steps 1-2): attempt it; refused/unavailable → ask the founder fix-or-skip, log the outcome with reason (see *Close every gap*), never block the commit or the gsd handoff.

8. **Now hand to gsd.** Infra is in place; gsd discusses + plans on top.
   - Greenfield: `gsd-new-project` — interviews the founder, writes the spec (`PROJECT.md`), requirements, roadmap into `.planning/`.
   - Brownfield: `gsd-map-codebase` + `gsd-ingest-docs` to reconstruct intent, fold in existing docs.
   Then `gsd-plan-phase` for the first/next real change. gsd absent → stop after the commit, tell them to install it before planning.

## Anti-slop measures

Slop = plausible-but-unverified output that looks done. Install every must-have; name each out loud to the founder. Skip a nice-to-have only as a stated choice. Full rationale + enforcement model: `references/anti-slop-measures.md`.

### Must-have (the repo is not agent-ready without these)

| Measure | What it does | Enforced via |
|---|---|---|
| One verify gate | lint + typecheck/contract-check + import-boundary lint + tests, one canonical command | `make verify` |
| Tests in gate from day one | one green smoke test; new behavior ships with tests in the same change | `make verify` |
| Pre-commit enforcement | gate runs at the commit boundary, not the honor system | pre-commit hook |
| Strict system-prompt override | flags unverified claims, marks `ASSUMPTION:`, refuses fake-done | system-prompt override |
| AGENTS.md house rules | evidence-grounded claims, stop-and-ask, simplest-thing-that-works, semantic-checkpoint commits | `AGENTS.md` |
| Decision log | locked decisions in one file; new choice logged, not re-litigated | `Lxx` entries |
| Import boundaries | one valid contract from day one, grown as modules appear | import-linter / dependency-cruiser / ESLint boundaries |
| Cross-CLI review | second model reviews the diff before it lands | `gsd-review`, wired into land step |
| Capture system | one file + INDEX per deferred item, not just a mention | `docs/ideas/`, `docs/tech_debt/` |
| Discipline skills | terse user-facing text, lazy/minimal code, every turn | caveman + ponytail in skill policy |
| Build to spec — exactly | acceptance criteria are the contract; can't-build-as-written → stop, surface options | `AGENTS.md` rule |
| No fake-done, no silent corner-cutting | scans for TODO/stub/placeholder markers; corner-cuts require logged + signed-off tech debt | gate check + `AGENTS.md` rule |
| Typed/contracted boundaries | no `Any` / `dict[str, Any]` smuggling at request/response/external/event boundaries | mypy-strict / tsc-strict / stack equivalent |
| Consistency with existing code | new code follows repo's naming, structure, error model, file layout | `AGENTS.md` rule + decision log |
| Reproducible build | no floating `latest`; same inputs, same result | committed lockfile |

### Nice-to-have (raise the ceiling; add when the project earns it)

| Measure | What it does | Enforced via |
|---|---|---|
| Worktree isolation + verify-before-land | parallel work in throwaway worktrees, verify before merge | `make worktree.land` |
| CI mirror of the gate | gate holds even if a local hook is bypassed | CI runs `make verify` |
| Coverage gate | fails verify under a coverage floor | `make verify` |
| Continuous AI audit (Enji Guard) | ongoing security / dependency-hygiene / test-coverage / AI-readiness audit, findings as GitHub issues/PRs | `https://guard.enji.ai/app`, connected in step 7 |

## Choosing the stack

Stack is a real, hard-to-reverse decision — log as `L01`. Don't reach for a default; Python and React/TS are common safe landings when nothing pulls against them, but pick from what the founder actually needs.

**Brownfield: detect, don't choose.** Read what's there (`templates/harness/README.md` has the detection table), record the real stack. Migrating an existing stack is out of scope — note a mismatch as tech_debt, don't rewrite.

**Greenfield: interview, then recommend.** Founder is non-technical — ask about product + users, not frameworks. One question at a time, multiple-choice, plain language, in Russian. Cover:

- **What is it?** Web app, mobile app, just-an-API/backend, desktop, CLI, automation/script. (Shapes whether a frontend exists at all.)
- **Who uses it and on what?** Public website visitors, signed-in users, internal team, other software calling an API. Phone-first or desktop-first?
- **How many, realistically?** Handful / hundreds / "I hope it goes viral." Don't over-build for scale that isn't coming — most ideas start small.
- **Anything non-negotiable?** Payments, login/accounts, file or photo uploads, real-time updates (chat/live), offline use, AI features, a deadline.
- **Constraints from their world?** A platform they're tied to, a language future hires will know, a host already paid for.

Then recommend ONE stack in plain terms, with why + tradeoff, framed so they can say yes or push back — in Russian, e.g.:

> Похоже на веб-приложение, куда заходят несколько сотен пользователей, с
> оплатами. Предложил бы **Python (FastAPI) для бэкенда, React для экрана,
> Postgres для данных, Stripe для платежей**. Скучно нарочно — большое
> сообщество, легко найти разработчиков, и AI-агенты хорошо пишут на этом
> стеке. Подходит, или есть предпочтения?

Let scale + needs move the recommendation — a static marketing site doesn't need React, an internal script needs no frontend, "must run on their phone offline" changes everything. Once confirmed, that's `L01`; the harness in step 4 follows it.

## Done

Infra committed first: `AGENTS.md` (+ `CLAUDE.md` symlink), `docs/` (`CODING_VALUES.md`, `HOW_TO_DEVELOP.md`, `architecture/`, `requirements/`, `guides/`, `ideas/`, `tech_debt/`), empty `.ai_skills/` (+ README), wired `make verify`. Repo pushed to remote with Enji Guard connected, or a founder-confirmed skip logged as tech_debt (no `gh`, no GitHub access, founder deferred).
Founder has seen `docs/HOW_TO_DEVELOP.md`, knows the loop. Every gap flagged during the run is closed — fixed, or a founder-confirmed skip in `docs/tech_debt/`; nothing left open on the assumption someone circles back (see *Close every gap*). gsd then produces spec + roadmap in `.planning/`; next step `gsd-plan-phase`. Greenfield: `make verify` green on the smoke test. Brownfield: gate runs; existing failures logged as tech_debt, not silenced.

## Acceptance checks

Self-check a run against these (detail for each lives in Flow / Choosing the stack / Anti-slop measures above — this is the checklist, not new rules):

- Step 1 (system-prompt override) actually installed, not skipped for conversational momentum — the only valid skip is a failed/refused CLI install, put to the founder as fix-or-skip and the outcome logged as tech_debt.
- Every must-have anti-slop measure present + named to the founder; skipped nice-to-haves were a stated choice.
- No open gaps at Done: every failed/refused/skipped step (1, 2, 4-brownfield, 7) is either fixed or a founder-confirmed skip in `docs/tech_debt/` — never an internal note the founder never saw.
- Gate runs all four check classes with stack-native tools; no credible native tool → logged as tech_debt, closest check enforced instead. Lockfile/pin file committed.
- Stack: greenfield confirmed via interview before scaffolding, logged as `L01`; brownfield detected, not migrated.
- Brownfield: findings + improvements list surfaced before changes; existing `CLAUDE.md`/`AGENTS.md`/`Makefile` merged by hand, never clobbered; failing tests logged as tech_debt, gate not weakened to go green.
- gsd missing → infra committed, stop before planning, told to install.
- Push + Enji Guard attempted every run — connected, or a founder-confirmed skip logged as tech_debt.

## References

- `references/context-engineering.md` — six context types, static vs dynamic.
- `references/anti-slop-measures.md` — rationale behind each anti-slop measure.
- `references/cli-setup.md` — system-prompt override + skills install, per CLI.
- `references/templates.md` — docs, decision log, capture skeletons.
- `references/worktree-workflow.md` — parallel isolated work + safe landing.
- `templates/AGENTS.md.tmpl` — static-context file to fill.
- `templates/CODING_VALUES.md.tmpl` — house coding standard, → `docs/CODING_VALUES.md`.
- `templates/HOW_TO_DEVELOP.md.tmpl` — human guide to daily loop, → `docs/HOW_TO_DEVELOP.md`.
- `templates/project-skills-README.md.tmpl` — README for empty `.ai_skills/` home where project-specific skills get added later.
- `templates/strict-engineer-system-prompt.md` — starting system-prompt override.
- `templates/harness/` — reference command surface + configs (Python/Node shape); adapt to chosen stack, including "A different stack?" for everything else.
