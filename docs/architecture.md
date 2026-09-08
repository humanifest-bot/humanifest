# Architecture

The MVP is intentionally small:

- JSON records are the durable data store.
- Python standard library code validates, scores, and renders text outputs.
- JSON schema files document the public record shape.
- Unit tests exercise deterministic behavior.

All CLI commands validate before rendering. Portfolio loading collects per-file
errors, checks unique IDs within each record collection, and resolves project
references. Missing portfolio directories are errors; existing empty directories
are allowed. JSON loading rejects duplicate keys and non-standard numeric
constants instead of silently accepting ambiguous records.

Portfolio validation also enforces implementation and PR workload limits from the
contribution protocol. Organization grouping uses GitHub owners or the project's
explicit `review_organization`. Reports expose capacity, blockers, and next actions
without changing records. Candidate briefs and handoffs preserve source URLs and
access dates so a fresh reviewer can inspect the evidence.

The schemas describe nested source, evidence, gate, and score shapes as well as
state-dependent gate requirements. Python additionally checks source-ID uniqueness,
evidence references, actual calendar dates, and portfolio relationships. JSON Schema
consumers must enable date format checking for equivalent calendar validation.

No database, server, dashboard, GitHub App, package publishing, or LLM framework is included.

GitHub Actions runs the offline suite, public JSON Schema validation, a generated
status comparison, and a wheel installation smoke test on Python 3.11 and 3.14.
Schema validation uses a pinned development dependency; application installation
and use still require no runtime dependencies. See `CONTRIBUTING.md` for local
equivalents. The scripts under `scripts/` are development checks and are excluded
from the installed app.

## Why Python

Python was chosen because the first MVP is offline data validation and report generation. The standard library covers JSON parsing, CLI behavior, and unit tests without dependencies. TypeScript may become appropriate later if Humanifest develops a web UI or GitHub App, but that is explicitly deferred.
