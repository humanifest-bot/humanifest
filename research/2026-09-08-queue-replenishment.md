# Queue replenishment: independent humanitarian research

The user clarified on 2026-09-08 that waiting PRs should not stall donated work.
Two research opportunities were added across independent maintainer teams.
Current project and opportunity records control their gates and next actions.
Neither has earned implementation approval or a claim of realized impact.

## Work available now

1. **HOT Tasking Manager #7227 — completed-project data access.** Trace the
   archived-project download and extractor lifecycle, then distinguish a small
   availability-message improvement from a privileged refresh feature. A project
   participant explains why completed maps need to be shared with requestors;
   a HOT member identifies archived status as the condition. No cross-referenced
   PR was returned by the issue timeline, but a broader search remains necessary.
   Read `downloadOsmData.js`, the neighboring download tests, and extractor docs
   at the pinned tree before considering setup. Do not trigger live extraction.
2. **KoboToolbox #7259 / PR #7260 — incremental-sync verification.** Support the
   existing author with a bounded source and test-gap investigation. Pin the PR
   head and compare edit, validation, attachment and legacy/query behavior with
   actual tests. Treat the author's reported data-transfer workload as a case
   report, not measured savings. Prepare findings locally; coordinate before
   proposing implementation or publishing a review.

These jobs require public source reading, not a response on CHT or a merge of
Humanifest's control-repository PRs. The new records include prioritization
reasons, primary sources, explicit unknowns, and a planned external-status check
on 2026-09-15. That date does not install a monitor. Source investigation is useful
immediately; repeat status polling can wait.

## Screening avoided duplicate or speculative work

| Candidate screened | Decision and evidence |
| --- | --- |
| HDX Python API | No open issues appeared in the retrieved public open-issue list. Keep HDX as a relevant cause lead; no invented issue or project-specific work item was added. [Repository](https://github.com/OCHA-DAP/hdx-python-api) |
| HOT lock-error #7281 | Discussion links an unmerged, closed prior PR and another volunteer asks to work on the issue. Sensitive task-locking behavior also has special AI constraints. Chose a different research lead. [Issue](https://github.com/hotosm/tasking-manager/issues/7281), [prior PR](https://github.com/hotosm/tasking-manager/pull/7294) |
| Kobo date-display #5771 | Another contributor is actively seeking approval for the narrow fix, with a maintainer-created internal ticket. Do not crowd out that contributor. [Discussion](https://github.com/kobotoolbox/kpi/issues/5771) |
| Kobo edited-record detection #7259 | Existing PR #7260 changes the opportunity from replacement implementation to independent verification support. No competing PR will be prepared. [Issue](https://github.com/kobotoolbox/kpi/issues/7259), [PR](https://github.com/kobotoolbox/kpi/pull/7260) |

## Verification limits

Read-only GitHub metadata, discussions, contribution documents and complete
recursive trees were inspected on 2026-09-08. Initial screens were bounded:
the HOT recent list mixed issues and PRs, while Kobo used issue-only search.
Issue timelines do not prove the absence of unlinked work. Selected source-file
retrieval did not complete, so component/test paths are leads rather than a
finished code audit. No target clone, setup, test, production interaction,
maintainer message or agreement signing occurred.

HOT's own product documentation supports a mapping-to-data-use pathway. UNHCR's
handbook supports Kobo's use in humanitarian assessments. Neither proves the
benefit of these individual proposals. The implementation scores remain zero
while gates are unresolved; queue value lies in the concrete next investigation.
