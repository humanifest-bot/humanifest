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

Park the work if the issue is stale, already assigned, already under PR, too broad, security-sensitive without the target disclosure path, or dependent on private data.
