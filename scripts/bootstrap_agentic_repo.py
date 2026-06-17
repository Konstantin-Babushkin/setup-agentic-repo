from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

PYPROJECT = """[project]
name = "{dist}"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{pkg}"]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.12"
strict = true
# Opt in once ready (noisy early): disallow_any_explicit = true

[tool.importlinter]
root_package = "{pkg}"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "App does not import tests"
type = "forbidden"
source_modules = ["{pkg}"]
forbidden_modules = ["tests"]

[dependency-groups]
dev = ["pytest", "ruff", "mypy", "import-linter"]
"""

OVERVIEW = """# Architecture overview

One-page map of the system. Grows as the project does.

## What it is
TODO: one paragraph from PROJECT.md / the code.

## Stack
{stack}
See decision_log.md for why.

## Main pieces
TBD as we build.

## Source of truth
TODO: where the real data lives for each kind of thing.
"""

DECISION_LOG = """# Decision log

Locked decisions. Cite by id (L01, ...). Don't re-litigate a logged decision;
supersede it with a new entry.

## L01 — Stack
{stack}. Reason: TODO one line.
"""

TECH_DEBT_INDEX = """# Tech debt index

Known-bad code, missing tests, brittle paths, risky shortcuts. One file per item
in `active/`; move to `resolved/` (don't delete) in the same commit as the fix.

Severity: blocker (corruption / silent partial success / source-of-truth /
paid-API drain) | must (correctness/maintainability, or deferred with a trigger) |
nice (cosmetic, speculative).

## Active
- (none yet)

## Resolved
- (none yet)
"""

TECH_DEBT_TEMPLATE = """# <short title>

Severity: <blocker | must | nice>
Status: active
Date: YYYY-MM-DD
Source: <task / review that surfaced it>
Related files:
- <path:line>

## Context
What the debt / workaround / brittle path / missing test is.

## Why it matters
Impact if left unresolved.

## Next step
Smallest useful follow-up, or "revisit when <trigger>".
"""

IDEAS_INDEX = """# Ideas

Good ideas not for now, so they survive past the session. One file per item.

## Open
- (none yet)
"""

IDEAS_TEMPLATE = """# <short title>

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
"""

SMOKE_TEST = "def test_smoke() -> None:\n    assert True\n"


@dataclass
class Plan:
    created: list[str]
    skipped: list[str]

    def report(self) -> str:
        lines = [f"created: {p}" for p in self.created]
        lines += [f"exists (skipped, merge manually): {p}" for p in self.skipped]
        return "\n".join(lines) or "nothing to do"


def norm_dist(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "app"


def norm_pkg(name: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_") or "app"


def post_install(root: Path) -> None:
    if not shutil.which("uv"):
        print("uv not found — run `uv sync` then `make verify` to finish wiring the harness.")
        return
    result = subprocess.run(["uv", "sync"], cwd=root, check=False)
    if result.returncode != 0:
        print(f"`uv sync` failed (exit {result.returncode}) — fix it, then `uv sync` and `make verify`.")
        return
    print("ran `uv sync`. Verify with `make verify`. After `git init`: `uv run pre-commit install`.")


def render(text: str, slots: dict[str, str]) -> str:
    for key, value in slots.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_file(root: Path, target: Path, content: str, plan: Plan, dry_run: bool) -> None:
    rel = str(target.relative_to(root))
    if target.exists():
        plan.skipped.append(rel)
        return
    plan.created.append(rel)
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def detect_brownfield(root: Path) -> list[str]:
    markers = [
        "pyproject.toml",
        "uv.lock",
        "requirements.txt",
        "package.json",
        "Makefile",
        ".pre-commit-config.yaml",
        "tsconfig.json",
        "biome.json",
    ]
    return [m for m in markers if (root / m).exists()]


def slots_for(project_name: str, one_liner: str, stack: str, verify_cmd: str, pkg: str) -> dict[str, str]:
    return {
        "PROJECT_NAME": project_name,
        "ONE_LINE_VISION": one_liner or "TODO: one-line vision.",
        "STACK_SUMMARY": stack,
        "VERIFY_COMMAND": verify_cmd,
        "PKG": pkg,
        "CODE_STYLE": "- Self-documenting code; comments only where the WHY is non-obvious.\n- Explicit types; avoid `Any`.",
        "EXTRA_SKILLS": "",
    }


def run(root: Path, mode: str, slots: dict[str, str], dry_run: bool) -> Plan:
    plan = Plan(created=[], skipped=[])
    stack = slots["STACK_SUMMARY"]

    agents = render((TEMPLATES / "AGENTS.md.tmpl").read_text(), slots)
    write_file(root, root / "AGENTS.md", agents, plan, dry_run)

    operating = render((TEMPLATES / "OPERATING.md.tmpl").read_text(), slots)
    write_file(root, root / "OPERATING.md", operating, plan, dry_run)

    write_file(root, root / "docs/architecture/overview.md", OVERVIEW.format(stack=stack), plan, dry_run)
    write_file(root, root / "docs/architecture/decision_log.md", DECISION_LOG.format(stack=stack), plan, dry_run)
    write_file(root, root / "docs/tech_debt/INDEX.md", TECH_DEBT_INDEX, plan, dry_run)
    write_file(root, root / "docs/tech_debt/TEMPLATE.md", TECH_DEBT_TEMPLATE, plan, dry_run)
    write_file(root, root / "docs/tech_debt/active/.gitkeep", "", plan, dry_run)
    write_file(root, root / "docs/tech_debt/resolved/.gitkeep", "", plan, dry_run)
    write_file(root, root / "docs/ideas/INDEX.md", IDEAS_INDEX, plan, dry_run)
    write_file(root, root / "docs/ideas/TEMPLATE.md", IDEAS_TEMPLATE, plan, dry_run)

    if mode == "greenfield":
        pkg = norm_pkg(slots["PKG"])
        dist = norm_dist(slots["PROJECT_NAME"])
        write_file(root, root / "Makefile", render((TEMPLATES / "harness/Makefile.tmpl").read_text(), slots), plan, dry_run)
        write_file(root, root / "pyproject.toml", PYPROJECT.format(dist=dist, pkg=pkg), plan, dry_run)
        write_file(root, root / ".pre-commit-config.yaml", (TEMPLATES / "harness/.pre-commit-config.yaml.tmpl").read_text(), plan, dry_run)
        write_file(root, root / f"{pkg}/__init__.py", "", plan, dry_run)
        write_file(root, root / "tests/test_smoke.py", SMOKE_TEST, plan, dry_run)

    claude = root / "CLAUDE.md"
    if claude.exists():
        plan.skipped.append("CLAUDE.md")
    elif dry_run:
        plan.created.append("CLAUDE.md -> AGENTS.md")
    else:
        try:
            os.symlink("AGENTS.md", claude)
            plan.created.append("CLAUDE.md -> AGENTS.md")
        except OSError:
            claude.write_text((root / "AGENTS.md").read_text())
            plan.created.append("CLAUDE.md (copy; symlink unavailable — keep AGENTS.md canonical)")

    return plan


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        slots = slots_for("Demo", "", "Python + TS", "make verify", "demo")
        first = run(root, "greenfield", slots, dry_run=False)
        assert "AGENTS.md" in first.created
        assert (root / "AGENTS.md").exists()
        assert (root / "CLAUDE.md").is_symlink()
        before = (root / "AGENTS.md").read_text()
        second = run(root, "greenfield", slots, dry_run=False)
        assert "AGENTS.md" in second.skipped
        assert (root / "AGENTS.md").read_text() == before
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        slots = slots_for("Demo", "", "Python + TS", "make verify", "demo")
        plan = run(root, "greenfield", slots, dry_run=True)
        assert plan.created
        assert not (root / "AGENTS.md").exists()
    print("self-check OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold agentic-repo infra (never overwrites).")
    parser.add_argument("--mode", choices=["greenfield", "brownfield"], default="greenfield")
    parser.add_argument("--project-name", default="Project")
    parser.add_argument("--one-liner", default="")
    parser.add_argument("--stack", default="Python (FastAPI + SQLModel) + Postgres + React/TS")
    parser.add_argument("--verify-command", default="make verify")
    parser.add_argument("--pkg", default="app")
    parser.add_argument("--target", default=".")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()

    if args.self_check:
        self_check()
        return 0

    root = Path(args.target).resolve()
    if args.mode == "brownfield":
        found = detect_brownfield(root)
        print("detected: " + (", ".join(found) if found else "nothing — looks empty, consider --mode greenfield"))
        print("brownfield: writing only missing context files; harness left to manual merge (see harness/README.md).")

    slots = slots_for(args.project_name, args.one_liner, args.stack, args.verify_command, args.pkg)
    plan = run(root, args.mode, slots, args.dry_run)
    print(("DRY RUN\n" if args.dry_run else "") + plan.report())
    if not args.dry_run and args.mode == "greenfield":
        post_install(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
