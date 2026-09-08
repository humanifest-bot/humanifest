# Portfolio Status

Projects: 2
Opportunities: 4
Active implementations: 0/1
Open external PRs: 0/2 (at most 1 per organization)

Status reflects supplied records; source access dates are not a live upstream check.
Scores do not authorize implementation or external writes. Candidates are listed by state and ID, not ranked by raw score.

- cht-10155-edit-user-load-failure: MAINTAINER-CHECK; score=0.0; failed_gates=2
  Next: Record current maintainer confirmation; obtain user authorization before any inquiry or follow-up.
  - behavior_reproducible_or_verifiable: Source-level behavior is mapped, but UI/Karma reproduction has not been run because dependencies are not installed.
  - maintainer_interest_confirmed: Past maintainer interest exists, but no current confirmation to revive or replace stale PR #10824.
- cht-11342-dhis2-bs-month-export: MAINTAINER-CHECK; score=0.0; failed_gates=2
  Next: Record current maintainer confirmation; obtain user authorization before any inquiry or follow-up.
  - maintainer_interest_confirmed: No maintainer has confirmed that this is wanted or chosen a period-label approach.
  - probable_reviewer_identified: No reviewer is assigned on the issue.
- cht-10241-unique-race: PARKED; score=0.0; failed_gates=8
  Next: Keep parked until the stopping reason is resolved and evidence supports reconsideration.
  - behavior_reproducible_or_verifiable: Reproduction depends on timing/resource constraints and was not independently reproduced in this run.
  - code_and_tests_located: Exact code and test surface not yet located.
  - change_bounded: Potential solutions alter concurrency behavior across endpoints.
  - regression_strategy_credible: A credible deterministic concurrency test has not been designed.
  - security_and_licensing_risk_acceptable: Concurrency and API behavior risks remain unresolved.
  - maintainer_interest_confirmed: Maintainer has not selected a desired approach.
  - benefit_justifies_review_cost: Potential benefit is high, but review/design cost is also high.
  - user_can_explain_line_by_line: Not until a bounded approach is selected and reproduced.
- crisiscleanup-1164-success-banner-failure: PARKED; score=0.0; failed_gates=8
  Next: Keep parked until the stopping reason is resolved and evidence supports reconsideration.
  - contribution_policy_understood: Full CONTRIBUTING and CLA terms were not inspected in this run.
  - ai_policy_understood: No AI policy found.
  - problem_current_and_consequential: Issue is from 2024 with no comments; current behavior unconfirmed.
  - behavior_reproducible_or_verifiable: No reproduction performed and may require phone workflow context.
  - code_and_tests_located: Exact frontend source and tests not located.
  - maintainer_interest_confirmed: No maintainer confirmation.
  - probable_reviewer_identified: No reviewer identified.
  - benefit_justifies_review_cost: Staleness and uncertainty make review cost unjustified until confirmed.
