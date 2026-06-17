# Worktree workflow (parallel, isolated agent work)

A git worktree is a second checkout of the same repo on its own branch, in its
own directory. Agents build there so the main checkout stays clean and several
loops run in parallel without colliding. Modeled on the miracare monorepo's
proven `worktree.bootstrap` / `worktree.land` targets — bundled in the harness
`Makefile`.

## The guarantees (why land is a make target, not raw git)

`make worktree.land` refuses to land unless it's safe, so a non-technical owner
can't accidentally ship a mess:
- worktree must be committed (clean) — verification matches the landed code.
- main checkout must be on the base branch and clean.
- a portable lock (mkdir-based, works on Linux + macOS) serializes the whole
  critical section, so two parallel lands can't interleave.
- runs `make verify` on the **merged result** (after squash, before commit), so
  integration breakage is caught, not just per-branch greenness.
- lands exactly one squash commit, then removes the worktree and deletes the
  `agent/<slug>` branch.
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

Each independent task gets its own SLUG + worktree, so you can have several in
flight: one executing, one in review, one landing. Only constraint: two worktrees
editing the same files will conflict at land time — split work along module
boundaries (the import-linter contracts help keep those boundaries real). If
unsure two tasks are independent, ask the agent before starting both.

## Notes

- Never push worktree branches to a shared remote; they're ephemeral, land-only.
- One worktree owns a long-lived dev stack at a time (fixed ports) — siblings run
  tests, not the full stack.
