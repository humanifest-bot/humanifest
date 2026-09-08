# Architecture

The MVP is intentionally small:

- JSON records are the durable data store.
- Python standard library code validates, scores, and renders text outputs.
- JSON schema files document the public record shape.
- Unit tests exercise deterministic behavior.

No database, server, dashboard, GitHub App, package publishing, or LLM framework is included.

## Why Python

Python was chosen because the first MVP is offline data validation and report generation. The standard library covers JSON parsing, CLI behavior, and unit tests without dependencies. TypeScript may become appropriate later if Humanifest develops a web UI or GitHub App, but that is explicitly deferred.
