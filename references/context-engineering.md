# Context engineering, in plain language

Explain *why* each step matters, to non-technical founder. Don't dump it all. Pull relevant sentence when artifact comes up.

## The core idea

AI coding agent good work, same reason good new hire good: knows what building, why, house rules, has way check own work. Most people skip that, just ask chat. Work shaky, agent guessing.

"Context engineering" = unglamorous skill: write knowledge down where agent reads automatically. Keep asking: **"What would new teammate need know to do this well?"** Put answer where agent sees it.

## The six kinds of context an agent needs

1. **Instructions** — role, goals, lines must not cross. (Goes in `AGENTS.md`.)
2. **Knowledge** — how system built, decisions made, what it has to do. (Goes in `docs/`.)
3. **Memory** — what happened this session, durable facts about project that outlive session.
4. **Examples** — patterns to copy. Early on, few; codebase becomes examples as grows.
5. **Tools** — commands, scripts, other skills agent allowed use. (`Makefile` and skill policy.)
6. **Guardrails** — hard constraints, safety checks: "never do X", "always verify before claiming done". (Also in `AGENTS.md`, enforced by harness.)

## Static vs dynamic context (why we split things up)

Everything agent reads costs money, attention *every* interaction if always loaded. So split:

- **Static context** always on: `AGENTS.md`. Stay short, hold only what's true across whole project. Too much here, important rules drowned out.
- **Dynamic context** loaded only when needed: `docs/` files agent pulls for specific task, skills activate when job comes up. Why `docs/` exists separate from `AGENTS.md` — detail there when wanted, without weighing down every request.

Getting split right = real decision, not formality. Founder doesn't need theory; needs trust "rules short, details filed where agent can find them."

## Why the harness matters most

Difference between "vibe coding" and "agentic engineering": not whether use AI. Whether structure and verification around AI's output. Harness — tests, linter, type checker, one command checks everything — is that structure. Without it, "it works" just agent's opinion. With it, agent can prove work, fix own mistakes, next agent pick up safely. For non-technical founder: single most valuable thing in repo — lets them trust work they can't read.