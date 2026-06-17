# Document skeletons

Seed these from gsd's `.planning/PROJECT.md` and the codebase, then write into the
target repo. Starting shapes, not blank forms. No answer yet → write `OPEN:` and
the question, not a guess. Requirements + roadmap are gsd's job (`.planning/`) —
not here.

---

## docs/architecture/overview.md

```markdown
# Architecture overview

One-page map of the system. Grows as the project does.

## What it is
<one paragraph from PROJECT.md / the code>

## Stack
- Backend: <e.g. FastAPI + SQLModel>
- Data: <e.g. Postgres>
- Frontend: <e.g. React + TypeScript>
See decision_log.md for why.

## Main pieces
<list the obvious top-level parts once known; start with "TBD as we build">

## Source of truth
<where the real data lives for each kind of thing — fill in as it emerges>
```

---

## docs/architecture/decision_log.md

```markdown
# Decision log

Locked decisions. Cite by id (L01, L02, ...). Agents must not re-litigate a
logged decision; to change one, add a new entry that supersedes it.

## L01 — Stack
<chosen stack>. Reason: <one line>.

## L02 — <next decision>
...
```

---

## Capture system: ideas + tech_debt

Two parallel dirs, same shape. One file per item, `YYYY-MM-DD-short-slug.md`.
Start flat (`active/` + `resolved/`); when a dir grows past ~15 items, split
`active/` into theme subdirs (this is the monorepo's mature layout — point there
for an example). Resolved items stay for the audit trail, never deleted.

```
docs/
├── ideas/        INDEX.md, TEMPLATE.md, <item>.md         (no lifecycle, just open/done)
└── tech_debt/
    ├── INDEX.md
    ├── TEMPLATE.md
    ├── active/   <item>.md
    └── resolved/ <item>.md   (status flipped, resolution commit recorded)
```

### docs/tech_debt/INDEX.md

```markdown
# Tech debt index

Known-bad code, missing tests, brittle paths, risky shortcuts. One file per item
in `active/`; move to `resolved/` (don't delete) when fixed, in the same commit
as the fix.

Severity (grep-able `Severity:` field):
- blocker = data corruption, silent partial success, source-of-truth violation,
            paid-API drain risk. Fix before shipping.
- must    = correctness/maintainability hygiene, or deferred work with a named
            trigger.
- nice    = cosmetic, speculative, honor-system.

## Active
- (none yet)

## Resolved
- (none yet)
```

### docs/tech_debt/TEMPLATE.md

```markdown
# <short title>

Severity: <blocker | must | nice>
Status: active
Date: YYYY-MM-DD
Source: <task / review / conversation that surfaced it>
Related files:
- <path:line>

## Context
What the debt / workaround / brittle path / missing test is.

## Why it matters
Impact if left unresolved.

## Next step
Smallest useful follow-up action, or "revisit when <trigger>".

<!-- On resolve: set Status: resolved, add `Resolved in: <commit sha>`,
     git mv into resolved/, move the INDEX row to Resolved — same commit as the fix. -->
```

### docs/ideas/INDEX.md + docs/ideas/TEMPLATE.md

Same shape, lighter — ideas have no severity and no resolved/ lifecycle:

```markdown
# Ideas

Good ideas not for now, so they survive past the session. One file per item.

## Open
- (none yet)
```

```markdown
# <short title>

Date: YYYY-MM-DD
Source: <what surfaced it>
Related files:
- <path>

## Context
What was noticed or proposed.

## Why it matters
User / product / operational / engineering value.

## Next step
Smallest useful follow-up, or "revisit when <trigger>".
```
