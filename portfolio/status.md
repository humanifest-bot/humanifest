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
  - maintainer_interest_confirmed: Rechecked 2026-09-08: no current invitation to replace closed, unmerged PR #10824 was found in the inspected discussions.
- cht-11342-dhis2-bs-month-export: MAINTAINER-CHECK; score=0.0; failed_gates=2
  Next: Record current maintainer confirmation; obtain user authorization before any inquiry or follow-up.
  - maintainer_interest_confirmed: Rechecked 2026-09-08: the issue has no comments or assignees; no issue-level confirmation was found.
  - probable_reviewer_identified: No reviewer is assigned on the issue.
- cht-10241-unique-race: PARKED; score=0.0; failed_gates=8
  Next: Keep parked until the stopping reason is resolved and evidence supports reconsideration.
  - behavior_reproducible_or_verifiable: Reproduction depends on timing/resource constraints and was not independently reproduced in this run.
  - code_and_tests_located: Exact code and test surface not yet located.
  - change_bounded: Potential solutions alter concurrency behavior across endpoints.
  - regression_strategy_credible: A credible deterministic concurrency test has not been designed.
  - security_and_licensing_risk_acceptable: Concurrency and API behavior risks remain unresolved.
  - maintainer_interest_confirmed: Rechecked 2026-09-08: the inspected discussion still contains no selected approach following the maintainer objection to a global queue.
  - benefit_justifies_review_cost: Potential benefit is high, but review/design cost is also high.
  - user_can_explain_line_by_line: Not until a bounded approach is selected and reproduced.
- crisiscleanup-1164-success-banner-failure: PARKED; score=0.0; failed_gates=8
  Next: Keep parked until the stopping reason is resolved and evidence supports reconsideration.
  - contribution_policy_understood: Full CONTRIBUTING and CLA terms were not inspected in this run.
  - ai_policy_understood: No AI policy found.
  - problem_current_and_consequential: Rechecked 2026-09-08: open but last updated 2024-10-02, with no comments; current behavior remains unconfirmed.
  - behavior_reproducible_or_verifiable: No reproduction performed and may require phone workflow context.
  - code_and_tests_located: Exact frontend source and tests not located.
  - maintainer_interest_confirmed: Rechecked 2026-09-08: no comments or assignees; no current maintainer confirmation was found.
  - probable_reviewer_identified: No reviewer identified.
  - benefit_justifies_review_cost: Staleness and uncertainty make review cost unjustified until confirmed.
