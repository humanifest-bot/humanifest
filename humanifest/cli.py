"""Command line interface for Humanifest."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .models import (
    generate_candidate_brief,
    generate_handoff,
    iter_records,
    portfolio_report,
    score_opportunity,
    validate_opportunity,
    validate_project,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="humanifest", description="Validate and score humanitarian OSS contribution opportunities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--root", default=".", help="Repository root")

    score_parser = subparsers.add_parser("score")
    score_parser.add_argument("path", help="Opportunity JSON path")

    brief_parser = subparsers.add_parser("brief")
    brief_parser.add_argument("path", help="Opportunity JSON path")

    handoff_parser = subparsers.add_parser("handoff")
    handoff_parser.add_argument("path", help="Opportunity JSON path")
    handoff_parser.add_argument("--target", choices=["codex", "spark", "cursor-red-team"], required=True)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--root", default=".", help="Repository root")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return _validate(Path(args.root))
    if args.command == "score":
        from .models import load_json

        print(score_opportunity(load_json(Path(args.path))))
        return 0
    if args.command == "brief":
        from .models import load_json

        print(generate_candidate_brief(load_json(Path(args.path))))
        return 0
    if args.command == "handoff":
        from .models import load_json

        print(generate_handoff(load_json(Path(args.path)), args.target))
        return 0
    if args.command == "report":
        root = Path(args.root)
        projects = [record for _, record in iter_records(root / "portfolio" / "projects")]
        opportunities = [record for _, record in iter_records(root / "portfolio" / "opportunities")]
        print(portfolio_report(projects, opportunities))
        return 0
    return 2


def _validate(root: Path) -> int:
    issues = []
    for path, record in iter_records(root / "portfolio" / "projects"):
        issues.extend(validate_project(record, str(path)))
    for path, record in iter_records(root / "portfolio" / "opportunities"):
        issues.extend(validate_opportunity(record, str(path)))
    if issues:
        for issue in issues:
            print(f"{issue.record}: {issue.message}", file=sys.stderr)
        return 1
    print("validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
