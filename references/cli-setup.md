# Runtime layer: CLI, system-prompt override, skills

Agent behavior before it reads repo. Backs SKILL flow step 1 (CLI + system prompt), step 2 (skills). Plain language; founder picks CLI, you wire it.

## Pick the CLI

- **Claude Code**
- **Codex**

Both read `AGENTS.md` — repo work identical. Only override mechanism differs.

## Permissions (SKILL step 1 — do this first)

Why: default per-command approval prompts stall a long unattended setup + build run — including the very next action, installing the system-prompt override, which is itself a write the CLI would otherwise stop and ask permission for. Full bypass removes that for this session, on the founder's explicit yes (see SKILL.md step 1 — say plainly what it means, don't push if they decline).

- **Claude Code**: relaunch with `--dangerously-skip-permissions`, or set permission mode to `bypassPermissions` for the session. Tell founder: no more command-approval prompts until they end or relaunch the session normally.
- **Codex**: switch approval policy to full-auto / sandbox-bypass equivalent for the session.

Confirm active before doing anything else in step 1. Founder declines → proceed with normal prompting for the override install below (and everything after), not a blocker, don't re-ask later in the run.

## System-prompt override (SKILL step 1)

Why: out of box agent agreeable, flatters / cuts corners. Strict-engineering override makes it tell founder when idea bad — exactly what non-technical owner needs. Explain it that way.

Use bundled `templates/strict-engineer-system-prompt.md` as starting override (strict, evidence-over-confidence, challenges weak requirements, no flattery). Copy it, tweak only if founder wants different tone.

- **Claude Code**: save to `~/.config/agent-prompts/strict-engineer.md`, add wrapper alias with `--append-system-prompt "$(cat ~/.config/agent-prompts/strict-engineer.md)"`. Tell user launch via this alias.
- **Codex**: point its system-prompt / instructions setting at same file.

Confirm file exists, launch path applies it before moving on.

## Install skills (SKILL step 2)

Install via CLI's plugin/marketplace mechanism, re-check each present.

- **gsd-core** (github.com/open-gsd/gsd-core) — disciplined plan -> build -> verify cycles instead of one giant prompt. Owns project init, phase planning, execution. Install: `npx @opengsd/gsd-core@latest` (or via the CLI's plugin/marketplace mechanism if it wraps that). Individual commands keep the `gsd-` prefix unchanged (e.g. `gsd-new-project`, `gsd-plan-phase`) — check those are present after install.
- **caveman** — terse, high-signal user-facing text. Used for explanations, reviews — strips filler, keeps substance. NOT for commit messages (those stay Conventional Commits, normal prose).
- **ponytail** — lazy/minimal coding discipline. Used when writing code: simplest thing that works, stdlib over deps, no speculative abstractions.

Record usage split in `AGENTS.md` (skill policy): gsd for workflow, caveman for text, ponytail for code.

Skills can't install → escalate to user, ask them install.