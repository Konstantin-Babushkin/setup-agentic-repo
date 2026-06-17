# setup-agentic-repo

A Claude Code / Codex skill that takes a non-technical founder from a fuzzy idea
(or an existing codebase) to a repository set up for **agentic engineering**:
the AI implements, but inside clear intent, durable context, and automatic
verification — not vibe coding.

## What it sets up

```
[ CLI + system prompt ]  strict-engineering override (optional preflight)
[ Skills              ]  gsd-redux (plan/build), caveman (text), ponytail (code)
[ Repo context        ]  AGENTS.md + docs/  = what every agent reads first
[ Harness             ]  lint + types + tests + import boundaries = slop can't pass
[ gsd: discuss + plan ]  idea -> spec -> roadmap, on top of the infra above
```

Greenfield and brownfield both supported. Infra is laid first; the spec and
roadmap are handed to the gsd skills (gsd owns the discussion).

## Install

Drop the folder into your skills directory:

- Claude Code: `~/.claude/skills/setup-agentic-repo/`
- Codex: per its skill-install path (manifest at `agents/openai.yaml`).

Then trigger it: "set up this repo for AI agents" / "make my project
agent-ready", or just describe the idea.

## Layout

- `SKILL.md` — the skill spec + flow.
- `references/` — context-engineering primer, CLI setup, doc templates, worktree workflow.
- `templates/` — `AGENTS.md`, `OPERATING.md`, system-prompt override, and the harness.
- `scripts/bootstrap_agentic_repo.py` — scaffolds infra (`--dry-run`, `--self-check`, never overwrites).
- `scripts/test_bootstrap.sh` — regression test (self-check + greenfield `make verify`).

## Test

```
scripts/test_bootstrap.sh
```
