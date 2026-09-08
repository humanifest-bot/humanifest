# Humanifest

Humanifest converts donated AI-assisted engineering capacity into verified, maintainer-approved, low-burden contributions to humanitarian and public-interest open-source software.

It is deliberately a thin coordination layer. Its job is to help decide what not to do, then prepare a small number of excellent upstream contributions only after evidence and maintainer interest support the work.

## Current Status

This repository contains the first deterministic MVP:

- JSON records for projects and opportunities.
- Hard gates that prevent premature implementation.
- Transparent scoring from supplied evidence.
- Candidate brief, handoff, and portfolio report generation.
- Unit tests for validation, gates, scoring, and handoff generation.

Current records contain no opportunity ready for implementation. Run `report` for
each candidate's blockers and next permitted action; upstream status must be
rechecked before outreach or implementation.

## Principles

- One active implementation at a time.
- At most one open pull request per external organization.
- At most two open external pull requests across the portfolio.
- No nontrivial implementation before current maintainer interest is confirmed.
- No external writes without explicit user authorization.
- No private patient, survivor, volunteer, employee, or operational data.
- Every contribution must be minimal, issue-linked, reproducible, tested, and explainable line by line.

## Use

Python 3.11 or newer is required. The commands below run directly from this
checkout without installing dependencies.

```bash
python3 -m humanifest.cli validate --root .
python3 -m humanifest.cli report --root .
python3 -m humanifest.cli score portfolio/opportunities/cht-dhis2-bs-month-export.json
python3 -m humanifest.cli brief portfolio/opportunities/cht-dhis2-bs-month-export.json
python3 -m humanifest.cli handoff portfolio/opportunities/cht-dhis2-bs-month-export.json --target codex
```

For an installed `humanifest` command, create a virtual environment and install
the local app:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/humanifest report --root .
```

The installed package contains the Python app. Records, schemas, and research stay
in the checkout; pass `--root /path/to/humanifest` when running portfolio commands
from elsewhere. Installation does not publish a package.

Every command validates its input before producing output. Invalid records return
exit code `1` with diagnostics on stderr; argument errors return `2`. `score`
prints JSON for use by other tools. `validate` and `report` require both portfolio
record directories and check unique record IDs, opportunity-to-project links, and
the implementation and PR capacity limits above. Single-record commands cannot
check portfolio capacity; validate the full portfolio before starting work.

Reports show capacity, blockers, and state-specific next actions in state/ID order.
To refresh the saved status after validating records:

```bash
python3 -m humanifest.cli report --root . > /tmp/humanifest-status.md && cp /tmp/humanifest-status.md portfolio/status.md
```

Sources need unique IDs, absolute HTTP(S) or local `file://` URLs, and real access
dates in `YYYY-MM-DD` form. Evidence must reference a source in the same record.
These checks validate record consistency; they do not fetch sources or establish
that a claim is true. Reports and handoffs never advance opportunity states.

## Repository Map

- `humanifest/`: deterministic Python core.
- `schemas/`: public JSON schema documents.
- `portfolio/projects/`: audited project records.
- `portfolio/opportunities/`: issue-level opportunity records.
- `portfolio/contributions/`: future contribution records.
- `docs/`: protocol, methodology, research, and governance.
- `handoffs/`: bounded prompts for Codex, Spark, Cursor, and reviewers.
- `tests/`: offline unit tests.

## License

No license has been applied yet. See `docs/licensing.md` for options requiring owner approval before outside contributions are accepted.

## Non-Goals

Humanifest is not a dashboard, hosted service, autonomous GitHub bot, issue spammer, database server, LLM framework, or impact-ranking oracle.
