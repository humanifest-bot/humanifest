# Contribution Protocol

Humanifest represents external work through this pipeline:

```text
QUEUED
→ PROJECT-AUDIT
→ OPPORTUNITY-RESEARCH
→ SHORTLISTED
→ MAINTAINER-CHECK
→ ENVIRONMENT-READY
→ REPRODUCED
→ BUILDING
→ ADVERSARIAL-REVIEW
→ HUMAN-REVIEW
→ PR-OPEN
→ MERGED / RELEASED / PARKED / DECLINED
```

## Hard Gates

No opportunity may reach `BUILDING` unless every gate in `humanifest.models.HARD_GATES` passes:

- humanitarian relevance is supported;
- repository and affected subsystem are active;
- external contributions are accepted;
- contribution and AI policies are understood;
- problem is current and consequential;
- behavior is reproducible or objectively verifiable;
- relevant code and tests are located;
- change is bounded;
- regression protection is credible;
- no private operational data are required;
- security and licensing risks are acceptable;
- environment setup is feasible;
- maintainer has indicated the work is wanted or appropriate;
- probable reviewer exists;
- benefit justifies review cost;
- user can explain the change line by line.

## Stopping Conditions

Validation enforces maintainer confirmation from `ENVIRONMENT-READY` through
`RELEASED`, and every hard gate from `BUILDING` through `RELEASED`. `PARKED` and
`DECLINED` records retain their unresolved gates without being treated as active
work. Gate results must be booleans with non-empty rationales. Generated handoffs
include failed gates and explicitly block implementation while any gate fails.

Gate rationales can cite evidence using an optional `source_ids` list. If present,
the list must be non-empty, contain unique non-empty IDs, and reference entries in
the opportunity's own `sources` list. A passing `maintainer_interest_confirmed`
gate requires this list in every state. Link the actual confirmation and explain
the agreed scope in the rationale; an issue being open or labelled "help wanted"
does not establish current maintainer interest.

For example, after inspecting an actual confirmation and adding its source entry:

```json
"maintainer_interest_confirmed": {
  "passed": true,
  "rationale": "The maintainer confirmed the bounded approach described in this record.",
  "source_ids": ["maintainer-confirmation"]
}
```

The `maintainer-confirmation` source must include its real URL and access date.
The validator checks traceability, not the source's meaning, author identity, or
continuing relevance. A reviewer must still verify those claims. Unconfirmed gates
remain false and do not need invented citations. Existing records with a passing
maintainer gate but no citation must add verified evidence or correct that gate
before validation, scoring, or handoff generation can succeed.

Park the work if the issue is stale, already assigned, already under PR, too broad, security-sensitive without the target disclosure path, or dependent on private data.

## Portfolio Capacity

`validate` and `report` enforce one active implementation across `BUILDING`,
`ADVERSARIAL-REVIEW`, and `HUMAN-REVIEW`. A `PR-OPEN` record occupies one of two
portfolio PR slots and its organization's single PR slot. Stopped and completed
records occupy neither kind of slot. These checks use recorded states; they do not
query upstream PR status or track unrecorded work.

For GitHub repository URLs, the review organization defaults to
`github.com/<owner>` in lowercase, shared across that owner's repositories.
Projects on other hosts must supply a non-empty `review_organization` before an
opportunity reaches `PR-OPEN`. This optional project field also groups an
organization spread across hosts: use the same stable value on every affected
project. Explicit values are compared without surrounding whitespace or case.
Only use an override supported by the project's actual review ownership; do not
split one organization into different values to evade the limit.

Single-record scores and handoffs do not establish portfolio capacity or grant
authorization. Validate the full portfolio and check actual upstream status before
starting an implementation or opening a PR. Parked, declined, merged, and released
records have zero implementation score even if their historical gates all pass.
