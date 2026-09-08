# Comparative Research Memorandum

Access date for all current-source checks: 2026-09-06.

## Candidates Reviewed

The first audit started from CommCare, Community Health Toolkit, OpenMRS, Crisis Cleanup, and DHIS2. The two strongest candidates for issue-level audit were Community Health Toolkit and Crisis Cleanup because both combine humanitarian relevance, public repositories, visible contribution pathways, and current or recent repository activity.

## Community Health Toolkit

CHT has strong public-interest fit: Medic reports the platform supported more than 180,000 community health workers across 24 countries by the end of 2025. The project has current contributor documentation, a public GitHub organization, active issues, release documentation, security disclosure routes, and visible community discussion.

The strongest audited opportunity is #11342, a DHIS2 export bug involving Bikram Sambat reporting months and non-default `month_start_date`. It is current, bounded, source-locatable, and likely testable with synthetic data. It does not clear implementation because the product semantics need maintainer confirmation and no reviewer is identified.

CHT #10241 has potentially greater operational importance, but it is parked because the concurrency design is unresolved and a maintainer explicitly questioned a broad queue approach.

CHT #11413 is consequential and well reproduced, but it already has PR #11414. Humanifest should not duplicate active work.

## Crisis Cleanup

Crisis Cleanup has strong disaster-response relevance and the repository README reports substantial volunteer and household reach. However, the public issue candidates found during this pass were mostly older, assigned, broad, or stale. The clearest issue, #1164, reports a success banner after a failed phone workflow request, but current behavior is unconfirmed and the exact code surface was not located.

This makes Crisis Cleanup a good future candidate for maintainer inquiry, but weaker than CHT #11342 for the first Humanifest action.

## Ranked Opportunities

1. `cht-11342-dhis2-bs-month-export`: best next maintainer inquiry; do not implement yet.
2. `cht-10241-unique-race`: high potential value, parked for design risk.
3. `crisiscleanup-1164-success-banner-failure`: plausible but stale and unconfirmed.

## Recommendation

Ask CHT maintainers whether #11342 is wanted and whether the interval-derived lookup semantics are the preferred approach. If yes, prepare a Tier 3 environment and reproduce with synthetic target docs before implementation.
