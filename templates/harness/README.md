# Harness templates

The harness is the feedback loop that makes the repo agent-ready: one command
surface, automatic checks, a green smoke test. Scaffold the **foundation only**
now — commands and configs. CI and a docker stack come later. Import boundaries
start now with one trivially-valid contract and grow as modules appear.

## Python reference shape (only if Python is the chosen stack)

These configs are a reference, not a default. Use them when the founder landed on
Python (see SKILL.md "Choosing the stack"); for Node/TS build the parallel shape,
and for anything else see "A different stack?" below. There is no bootstrap script
— wire it by hand so every piece is real and matches the stack.

1. `uv init` to create `pyproject.toml`, then merge `pyproject-tooling.toml.tmpl`
   into it (replace `{{PKG}}` with the import package name) and `uv sync`.
2. Copy `Makefile.tmpl` → `Makefile`. `make verify` is the gate: lint + typecheck
   + lint-imports + test.
3. Write one smoke test (`tests/test_smoke.py`) so `make test` is green and the
   wiring is proven.
4. Copy `.pre-commit-config.yaml.tmpl` → `.pre-commit-config.yaml`, then (after
   `git init`) `uv run pre-commit install`.
5. Frontend: when a `web/` app exists, add Biome + `tsc` + a test script and
   uncomment the `fe.verify` lines in the Makefile.

Platform notes: the `CLAUDE.md` symlink and `make worktree.*` need a Unix-like
shell (Linux/macOS/WSL). On native Windows, keep `CLAUDE.md` as a copy of
`AGENTS.md` instead of a symlink.

## How strict? (the default stance)

Strict enough to **fail the build** — a warning nobody blocks on isn't a guardrail.

- **Strictness fails, it doesn't warn.** Every check is exit-nonzero inside
  `make verify`. No "warning" tier that accumulates and gets ignored.
- **Greenfield: max strict from day one.** It's cheapest when there's almost no
  code to fix. The Python config in `pyproject-tooling.toml.tmpl` is the default:
  a strong ruff set (tied to the CODING_VALUES rules — naming, simplify, dead
  code, exception + logging hygiene), `mypy --strict` + `warn_unreachable` +
  `disallow_any_explicit` (enforces the no-`dict[str, Any]` rule), and pytest with
  `--strict-markers --strict-config`, `xfail_strict`, `filterwarnings=["error"]`.
- **Brownfield: same strict config, baseline the violations.** Don't loosen the
  rule to go green. Freeze the current violation count (ratchet: forbid *new*
  violations, burn the backlog down as `docs/tech_debt/` items). For mypy on a
  legacy tree, comment out `disallow_any_explicit` and re-enable once the `Any`s
  are typed — that's a ratchet, not a permanent exemption.
- **No blanket suppressions.** A bare `# noqa` / `# type: ignore` fails (ruff
  RUF100 + mypy `ignore-without-code`) — suppress one rule by code, ideally with a
  reason. A silent blanket ignore is how strict configs rot into decoration.
- **Format is not lint.** The formatter (`ruff format` / Biome) auto-fixes style
  silently and never blocks; the linter blocks on correctness. Keeps style out of
  review so the gate flags real problems, not whitespace.

Frontend equivalent: `tsconfig.json` `"strict": true` plus
`noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes`;
Biome's recommended ruleset on, errors fail. Same five principles.

What NOT to enable: pydocstyle (`D`) — docstrings are banned by house style;
`ANN` — `mypy --strict` already requires annotations; ruff `ALL` — it churns
across versions and turns review into bikeshedding.

### Import boundaries (import-linter)

The starter contract ("app does not import tests") is valid the moment a package
exists and is a real guardrail. As structure emerges, add contracts so module
boundaries are enforced, not just hoped for:
- `independence` — sibling feature packages must not import each other.
- `layers` — e.g. `api` may import `domain`, `domain` may not import `api`.
This is what stops an agent from quietly tangling the codebase over many edits.

## Existing (brownfield) repo?

Detect first, don't clobber. Scan for what's already there, then fill only the gaps.

Detection checklist:

| Signal | Files / markers | If present |
|---|---|---|
| Python project | `pyproject.toml`, `setup.cfg`, `uv.lock`, `requirements*.txt` | use it; don't re-init |
| Python tools | `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest]`, `[tool.importlinter]` | keep config, wrap in `verify` |
| Node project | `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` | use the existing PM |
| Node tools | `.eslintrc*`, `biome.json`, `tsconfig.json` | keep config, wrap in `verify` |
| Existing gate | `Makefile`, `Justfile`, npm `scripts` | wrap, see below |
| Pre-commit | `.pre-commit-config.yaml` | add missing hooks, don't replace |
| CI | `.github/workflows/*`, `.gitlab-ci.yml` | note it; don't duplicate locally |

Merge rules:
- **Wrap, don't replace.** If a check already exists, point `make verify` at it.
  Only add a tool (ruff/mypy/import-linter/...) when it's genuinely absent.
- **Never overwrite a config file.** Augment in place or surface a conflict.
- Expect existing checks to fail on first run — that's signal, not failure. Log
  failures as `docs/tech_debt/active/` items; never make the gate pass by loosening
  rules or deleting tests.

## A different stack?

Don't look for a matching template. Build the same shape from these principles:

- **One command surface.** A single `verify` command that runs everything, plus
  `test` / `lint` / `typecheck` / `fmt`. Agents and humans use the same commands.
- **Lint + type + test + import-boundaries + pre-commit.** Whatever the stack's
  standard tools are (import-linter for Python; ESLint boundaries / dependency-cruiser
  for JS/TS).
- **One green smoke test from day one**, so the harness is provably wired.
- **One starter boundary contract**, valid immediately, grown as modules appear.
- **Foundation only.** No feature code.

The goal is always the same: "it works" should mean "the checks passed", not
"the agent said so".
