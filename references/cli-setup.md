# Runtime layer: CLI, system-prompt override, skills

How the agent behaves before it ever reads the repo. Backs SKILL flow steps 1
(CLI + system prompt) and 2 (skills). Plain language; the founder picks the CLI,
you do the wiring.

## Pick the CLI

- **Claude Code**
- **Codex**

Both read `AGENTS.md`, so the repo work is identical. Only the override mechanism
differs.

## System-prompt override (SKILL step 1)

Why: out of the box the agent is agreeable and will flatter / cut corners. A
strict-engineering override makes it tell the founder when something is a bad
idea — exactly what a non-technical owner needs. Explain it that way.

Use the bundled `templates/strict-engineer-system-prompt.md` as the starting
override (strict, evidence-over-confidence, challenges weak requirements, no
flattery). Copy it, tweak only if the founder wants a different tone.

- **Claude Code**: save to `~/.config/agent-prompts/strict-engineer.md` and add a
  wrapper alias with `--append-system-prompt "$(cat ~/.config/agent-prompts/strict-engineer.md)"`.
  Tell the user to launch via this alias.
- **Codex**: point its system-prompt / instructions setting at the same file.

Confirm the file exists and the launch path applies it before moving on.

## Install skills (SKILL step 2)

Install via the CLI's plugin/marketplace mechanism, then re-check each is present.

- **gsd-redux** — disciplined plan -> build -> verify cycles instead of one giant
  prompt. Owns project init, phase planning, execution. Check for `gsd-*` skills
  (e.g. `gsd-new-project`, `gsd-plan-phase`).
- **caveman** — terse, high-signal user-facing text. Used for explanations and
  reviews — strips filler, keeps substance. NOT for commit messages (those stay
  Conventional Commits, normal prose).
- **ponytail** — lazy/minimal coding discipline. Used when writing code: simplest
  thing that works, stdlib over deps, no speculative abstractions.

Record the usage split in `AGENTS.md` (skill policy): gsd for workflow, caveman
for text, ponytail for code.

If skills can't be installed, escalate to the user and ask them to install.
