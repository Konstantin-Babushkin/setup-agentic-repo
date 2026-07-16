# setup-agentic-repo

Claude Code / Codex skill. Takes non-technical founder from fuzzy idea
(or existing codebase) to repo set up for **agentic engineering**:
AI implements, but inside clear intent, durable context, automatic
verification — not vibe coding.

## What it sets up

```
[ CLI + system prompt ]  strict-engineering override (optional preflight)
[ Skills              ]  gsd-core (plan/build), caveman (text), ponytail (code)
[ Repo context        ]  AGENTS.md + docs/  = what every agent reads first
[ Harness             ]  lint + types + tests + import boundaries = slop can't pass
[ Push + AI QA        ]  push to GitHub, connect Enji Guard for continuous audit
[ gsd: discuss + plan ]  idea -> spec -> roadmap, on top of the infra above
```

Greenfield + brownfield both supported. Infra laid first; spec + roadmap
handed to gsd skills (gsd owns discussion).

## Install

Drop folder into skills directory:

- Claude Code: `~/.claude/skills/setup-agentic-repo/`
- Codex: per its skill-install path (manifest at `agents/openai.yaml`).

Trigger: "set up this repo for AI agents" / "make my project
agent-ready", or just describe idea.

## Layout

- `SKILL.md` — skill spec + flow.
- `references/` — context-engineering primer, CLI setup, doc templates, worktree workflow.
- `templates/` — `AGENTS.md`, `CODING_VALUES.md`, `HOW_TO_DEVELOP.md`, project-skills
  README, system-prompt override, harness.

Infra wired by hand from templates, adapted to chosen stack — no
bootstrap script. Greenfield picks stack via short product interview
(SKILL.md "Choosing the stack"); brownfield detects it.