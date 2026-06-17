# Context engineering, in plain language

Use this to explain *why* you're doing each step to a non-technical founder.
Don't dump it on them. Pull the one relevant sentence when an artifact comes up.

## The core idea

An AI coding agent does good work for the same reason a good new hire does: it
knows what you're building, why, the rules of the house, and it has a way to
check its own work. Most people working with AI agents skip all of that and just
ask for things in a chat. The work comes out shaky because the agent is guessing.

"Context engineering" is the unglamorous skill of writing that knowledge down in
the forms an agent reads automatically. The question to keep asking is: **"What
would a new teammate need to know to do this well?"** Then we put the answer
where the agent will see it.

## The six kinds of context an agent needs

1. **Instructions** — its role, goals, and the lines it must not cross. (Goes in
   `AGENTS.md`.)
2. **Knowledge** — how the system is built, the decisions already made, what it
   has to do. (Goes in `docs/`.)
3. **Memory** — what just happened in this session, and the durable facts about
   the project that should outlive any one session.
4. **Examples** — patterns to copy. Early on there are few; the codebase becomes
   the examples as it grows.
5. **Tools** — the commands, scripts, and other skills the agent is allowed to
   use. (The `Makefile` and the skill policy.)
6. **Guardrails** — hard constraints and safety checks: "never do X", "always
   verify before claiming done". (Also in `AGENTS.md`, enforced by the harness.)

## Static vs dynamic context (why we split things up)

Everything the agent reads costs money and attention on *every* interaction if
it's always loaded. So we split it:

- **Static context** is always on: `AGENTS.md`. It must stay short and hold only
  what's true across the whole project. Too much here and the important rules get
  drowned out.
- **Dynamic context** is loaded only when needed: the `docs/` files the agent
  pulls for a specific task, and skills that activate when their job comes up.
  This is why `docs/` exists separately from `AGENTS.md` — so detail is there
  when wanted without weighing down every request.

Getting this split right is a real decision, not a formality. The founder doesn't
need the theory; they need to trust that "the rules are short and the details are
filed where the agent can find them."

## Why the harness matters most

The difference between "vibe coding" and "agentic engineering" is not whether you
use AI. It's whether there's structure and verification around the AI's output.
The harness — tests, a linter, a type checker, one command that checks
everything — is that structure. Without it, "it works" is just the agent's
opinion. With it, the agent can prove the work, fix its own mistakes, and the
next agent can pick up safely. For a non-technical founder this is the single
most valuable thing in the repo: it's what lets them trust work they can't read.
