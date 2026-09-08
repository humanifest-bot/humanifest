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

The schemas describe nested source, evidence, gate, and score shapes as well as
state-dependent gate requirements. Python additionally checks source-ID uniqueness,
evidence references, actual calendar dates, and portfolio relationships. JSON Schema
consumers must enable date format checking for equivalent calendar validation.

No database, server, dashboard, GitHub App, package publishing, or LLM framework is included.

## Why Python

Python was chosen because the first MVP is offline data validation and report generation. The standard library covers JSON parsing, CLI behavior, and unit tests without dependencies. TypeScript may become appropriate later if Humanifest develops a web UI or GitHub App, but that is explicitly deferred.
