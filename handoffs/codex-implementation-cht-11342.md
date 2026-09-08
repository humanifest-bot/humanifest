# Codex Implementation Handoff: CHT #11342

Objective: prepare, but do not submit, a minimal fix for CHT issue #11342 only after maintainer confirmation.

Essential context:

- Humanifest record: `portfolio/opportunities/cht-dhis2-bs-month-export.json`.
- Target repo: `https://github.com/medic/cht-core`.
- Suspected source: `api/src/services/export/dhis.js`.
- Problem: `fetch.targetDocsInMonth` derives BS target doc key from raw `from`; writer derives target doc tag from reporting interval end.

Exact scope:

- Inspect CHT contribution, AI, security, and test policies.
- Inspect package manifests, lifecycle hooks, Docker/devcontainer/CI files before installing dependencies.
- Locate DHIS export tests.
- Reproduce with synthetic settings and target docs.
- Implement smallest semantics-preserving patch only if maintainer confirmation exists.

Acceptance criteria:

- Regression test proves `use_bikram_sambat_months: true` and non-default `month_start_date` export the writer's stored period.
- Existing Gregorian behavior is preserved.
- No private data, live DHIS2 system, or production credentials are used.
- User can explain the diff line by line.

Verification commands:

- Use CHT's documented narrow API/export test command once located.
- Run broader relevant unit tests if the patch touches shared calendar logic.

Stopping condition:

- Stop if maintainers do not confirm, exact tests cannot be located, reproduction needs private data, or the fix requires product semantics beyond the issue.

Return format:

- Findings, files changed, tests run, failures, residual risks, and PR-readiness assessment.
