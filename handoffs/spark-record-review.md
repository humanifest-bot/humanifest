# Spark Record Review Handoff

Objective: quickly review Humanifest JSON records and docs for internal consistency.

Scope:

- `portfolio/projects/*.json`
- `portfolio/opportunities/*.json`
- `schemas/*.schema.json`
- `docs/contribution-protocol.md`

Acceptance criteria:

- Every opportunity has all hard gates.
- Every failed gate has a rationale.
- Sources use URLs and access dates.
- No opportunity is recommended for implementation unless all gates pass.

Verification:

```bash
python3 -m humanifest.cli validate --root .
python3 -m humanifest.cli report --root .
```

Return format:

- Problems found, suggested minimal fixes, commands run.
