# Harness templates

Harness = feedback loop making repo agent-ready: one command surface, automatic checks, green smoke test. Scaffold **foundation only** now — commands and configs. CI, docker stack come later. Import boundaries start now, one trivially-valid contract, grow as modules appear.

## Python reference shape (only if Python is the chosen stack)

Configs = reference, not default. Use when founder landed on Python (see SKILL.md "Choosing the stack"); for Node/TS build parallel shape, else see "A different stack?" below. No bootstrap script — wire by hand so every piece real, matches stack.

1. `uv init` creates `pyproject.toml`, merge `pyproject-tooling.toml.tmpl` in (replace `{{PKG}}` w/ import package name), `uv sync`.
2. Copy `Makefile.tmpl` → `Makefile`. `make verify` = gate: lint + typecheck + lint-imports + test.
3. Write one smoke test (`tests/test_smoke.py`) so `make test` green, wiring proven.
4. Copy `.pre-commit-config.yaml.tmpl` → `.pre-commit-config.yaml`, then (after `git init`) `uv run pre-commit install`.
5. Frontend: when `web/` app exists, add Biome + `tsc` + test script, uncomment `fe.verify` lines in Makefile.

Platform notes: `CLAUDE.md` symlink, `make worktree.*` need Unix-like shell (Linux/macOS/WSL). Native Windows: keep `CLAUDE.md` as copy of `AGENTS.md`, not symlink.

## How strict? (the default stance)

Strict enough to **fail the build** — warning nobody blocks on isn't guardrail.

- **Strictness fails, doesn't warn.** Every check exit-nonzero inside `make verify`. No "warning" tier that accumulates, gets ignored.
- **Greenfield: max strict day one.** Cheapest when almost no code to fix. Python config in `pyproject-tooling.toml.tmpl` = default: strong ruff set (tied to CODING_VALUES rules — naming, simplify, dead code, exception + logging hygiene), `mypy --strict` + `warn_unreachable` + `disallow_any_explicit` (enforces no-`dict[str, Any]` rule), pytest w/ `--strict-markers --strict-config`, `xfail_strict`, `filterwarnings=["error"]`.
- **Brownfield: same strict config, baseline violations.** Don't loosen rule to go green. Freeze current violation count (ratchet: forbid *new* violations, burn backlog down as `docs/tech_debt/` items). Mypy on legacy tree: comment out `disallow_any_explicit`, re-enable once `Any`s typed — ratchet, not permanent exemption.
- **No blanket suppressions.** Bare `# noqa` / `# type: ignore` fails (ruff RUF100 + mypy `ignore-without-code`) — suppress one rule by code, ideally w/ reason. Silent blanket ignore = how strict configs rot into decoration.
- **Format is not lint.** Formatter (`ruff format` / Biome) auto-fixes style silently, never blocks; linter blocks on correctness. Keeps style out of review so gate flags real problems, not whitespace.

Frontend equivalent: `tsconfig.json` `"strict": true` plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes`; Biome recommended ruleset on, errors fail. Same five principles.

What NOT to enable: pydocstyle (`D`) — docstrings banned by house style; `ANN` — `mypy --strict` already requires annotations; ruff `ALL` — churns across versions, turns review into bikeshedding.

### Import boundaries (import-linter)

Starter contract ("app does not import tests") valid moment package exists, real guardrail. As structure emerges, add contracts so module boundaries enforced, not just hoped for:
- `independence` — sibling feature packages must not import each other.
- `layers` — e.g. `api` may import `domain`, `domain` may not import `api`.
Stops agent from quietly tangling codebase over many edits.

## Existing (brownfield) repo?

Detect first, don't clobber. Scan what's already there, fill only gaps.

Detection checklist:

| Signal | Files / markers | If present |
|---|---|---|
| Python project | `pyproject.toml`, `setup.cfg`, `uv.lock`, `requirements*.txt` | use it; don't re-init |
| Python tools | `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest]`, `[tool.importlinter]` | keep config, wrap in `verify` |
| Node project | `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` | use existing PM |
| Node tools | `.eslintrc*`, `biome.json`, `tsconfig.json` | keep config, wrap in `verify` |
| Existing gate | `Makefile`, `Justfile`, npm `scripts` | wrap, see below |
| Pre-commit | `.pre-commit-config.yaml` | add missing hooks, don't replace |
| CI | `.github/workflows/*`, `.gitlab-ci.yml` | note it, don't duplicate locally |

Merge rules:
- **Wrap, don't replace.** If check already exists, point `make verify` at it. Only add tool (ruff/mypy/import-linter/...) when genuinely absent.
- **Never overwrite config file.** Augment in place or surface conflict.
- Expect existing checks to fail first run — signal, not failure. Log failures as `docs/tech_debt/active/` items; never make gate pass by loosening rules or deleting tests.

## A different stack?

Don't look for matching template. Build same shape from these principles:

- **One command surface.** Single `verify` command running everything, plus `test` / `lint` / `typecheck` / `fmt`. Agents, humans use same commands.
- **Lint + type + test + import-boundaries + pre-commit.** Whatever stack's standard tools are (import-linter for Python; ESLint boundaries / dependency-cruiser for JS/TS).
- **One green smoke test day one**, harness provably wired.
- **One starter boundary contract**, valid immediately, grows as modules appear.
- **Foundation only.** No feature code.

Goal always same: "it works" should mean "checks passed", not "agent said so".