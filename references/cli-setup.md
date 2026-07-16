# Runtime layer: CLI, system-prompt override, skills

Agent behavior before it reads repo. Backs SKILL flow step 1 (CLI + system prompt), step 2 (skills). Plain language; founder picks CLI, you wire it.

## Pick the CLI

- **Claude Code**
- **Codex**

Both read `AGENTS.md` — repo work identical. Only override mechanism differs.

## System-prompt override (SKILL step 1)

Why: out of box agent agreeable, flatters / cuts corners. Strict-engineering override makes it tell founder when idea bad — exactly what non-technical owner needs. Explain it that way.

Use bundled `templates/strict-engineer-system-prompt.md` as starting override (strict, evidence-over-confidence, challenges weak requirements, no flattery). Copy it, tweak only if founder wants different tone.

- **Claude Code**: save to `~/.config/agent-prompts/strict-engineer.md`, add wrapper alias with `--append-system-prompt "$(cat ~/.config/agent-prompts/strict-engineer.md)"`. Tell user launch via this alias.
- **Codex**: point its system-prompt / instructions setting at same file.

Confirm file exists, launch path applies it before moving on.

## Install skills (SKILL step 2)

Install via CLI's plugin/marketplace mechanism, re-check each present.

- **gsd-redux** — disciplined plan -> build -> verify cycles instead of one giant prompt. Owns project init, phase planning, execution. Check for `gsd-*` skills (e.g. `gsd-new-project`, `gsd-plan-phase`).
- **caveman** — terse, high-signal user-facing text. Used for explanations, reviews — strips filler, keeps substance. NOT for commit messages (those stay Conventional Commits, normal prose).
- **ponytail** — lazy/minimal coding discipline. Used when writing code: simplest thing that works, stdlib over deps, no speculative abstractions.

Record usage split in `AGENTS.md` (skill policy): gsd for workflow, caveman for text, ponytail for code.

Skills can't install → escalate to user, ask them install.