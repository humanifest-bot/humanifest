"""Command line interface for Humanifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .models import (
    generate_candidate_brief,
    generate_handoff,
    load_json,
    load_portfolio,
    portfolio_report,
    score_opportunity,
    validate_opportunity,
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

    try:
        if args.command in {"validate", "report"}:
            projects, opportunities, issues = load_portfolio(Path(args.root))
            if _print_issues(issues):
                return 1
            print("validation ok" if args.command == "validate" else portfolio_report(projects, opportunities))
        else:
            record = load_json(Path(args.path))
            if _print_issues(validate_opportunity(record, args.path)):
                return 1
            if args.command == "score":
                print(json.dumps(score_opportunity(record), indent=2, allow_nan=False))
            elif args.command == "brief":
                print(generate_candidate_brief(record))
            else:
                print(generate_handoff(record, args.target))
    except (OSError, ValueError) as error:
        print(f"humanifest: {error}", file=sys.stderr)
        return 1
    return 0


def _print_issues(issues) -> bool:
    for issue in issues:
        print(f"{issue.record}: {issue.message}", file=sys.stderr)
    return bool(issues)


if __name__ == "__main__":
    raise SystemExit(main())
