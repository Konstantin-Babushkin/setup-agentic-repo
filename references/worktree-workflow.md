# Worktree workflow (parallel, isolated agent work)

Git worktree = second checkout, same repo, own branch, own dir. Agents build there, main checkout stays clean, several loops run parallel without colliding. Modeled on miracare monorepo's proven `worktree.bootstrap` / `worktree.land` targets — bundled in harness `Makefile`.

## The guarantees (why land is a make target, not raw git)

`make worktree.land` refuses to land unless safe, so non-technical owner can't accidentally ship mess:
- worktree must be committed (clean) — verification matches landed code.
- main checkout must be on base branch, clean.
- portable lock (mkdir-based, Linux + macOS) serializes whole critical section, so two parallel lands can't interleave.
- runs `make verify` on **merged result** (after squash, before commit) — catches integration breakage, not just per-branch greenness.
- lands exactly one squash commit, removes worktree, deletes `agent/<slug>` branch.
No rebase, no force-push, no merging unverified work.

## Daily commands

```
make worktree.bootstrap                       # once per clone
make worktree.new SLUG=add-login              # branch agent/add-login into .claude/worktrees/add-login
# ... gsd-execute-phase builds + commits in that worktree, keeping `make verify` green ...
# ... other-CLI code review on the worktree diff ...
make worktree.land SLUG=add-login MSG="feat(auth): email login"
```

## Parallel loops

Each independent task gets own SLUG + worktree — several in flight: one executing, one in review, one landing. Only constraint: two worktrees editing same files conflict at land time — split work along module boundaries (import-linter contracts keep boundaries real). Unsure two tasks independent? Ask agent before starting both.

## Notes

- Never push worktree branches to shared remote — ephemeral, land-only.
- One worktree owns long-lived dev stack at a time (fixed ports) — siblings run tests, not full stack.