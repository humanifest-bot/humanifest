# Opportunity recheck: 2026-09-08

This is an evidence synthesis. The updated opportunity records remain controlling
for candidate decisions. All four pipeline states and implementation scores remain
unchanged; no maintainer messages, target PRs, dependency installs, or target test
runs were performed.

## Scope and method

Read-only `gh issue view` queries retrieved state, assignees, labels, update times,
and comments for all four recorded issues. `gh pr view` retrieved PR #10824's
state, merge time, comments, and review status. Paginated issue timeline queries
checked cross-references for #10155 and #11342. These bounded queries do not prove
the absence of competing work elsewhere.

The remote CHT `master` ref and the existing local checkout both resolved to
`35b2bb6dac0844bee3228476591d08d56c5dd10d`. Relevant committed source and tests
were inspected without executing them. The local checkout remains on branch
`10155-edit-user-load-state` with nine modified files; its patch is uncommitted
preparation, not upstream behavior. The original 2026-09-06 access dates and
observations were preserved; new source IDs carry this recheck's date.

## Claim ledger

| Claim | Type / strength | Primary support | Limits and disconfirming evidence |
| --- | --- | --- | --- |
| CHT #10155 remains open, unassigned, with six comments. | Observed / A | [Issue](https://github.com/medic/cht-core/issues/10155), accessed 2026-09-08 | Last reported update: 2026-06-26. Open status and the Help wanted label do not establish current capacity. A new assignment, invitation, or replacement PR would change the next action. |
| PR #10824 is closed and unmerged. | Observed / A | [PR](https://github.com/medic/cht-core/pull/10824), accessed 2026-09-08 | Closed 2026-06-26; `mergedAt` is null. It was the only cross-reference returned by the inspected #10155 timeline. That is not an exhaustive competing-PR search. |
| The prior loading-flow fix needs visible reproduction evidence. | Interpretation / B | [April 22 review comment](https://github.com/medic/cht-core/pull/10824#issuecomment-4298432595), accessed 2026-09-08 | Reviewer could not see the fix and asked for a short video. The later contributor screenshot is a self-report, not independent reproduction. No Humanifest UI test or video was run. |
| CHT #11342 has no issue-level maintainer confirmation in its discussion. | Observed / A for retrieved discussion | [Issue](https://github.com/medic/cht-core/issues/11342), accessed 2026-09-08 | Open, unassigned, zero comments; last update 2026-08-26. No cross-references were returned. Private or unlinked conversations were not inspected. |
| The DHIS source and a concrete regression-test location are known. | Observed / A | [Pinned source](https://github.com/medic/cht-core/blob/35b2bb6dac0844bee3228476591d08d56c5dd10d/api/src/services/export/dhis.js#L81-L98), [pinned test](https://github.com/medic/cht-core/blob/35b2bb6dac0844bee3228476591d08d56c5dd10d/api/tests/mocha/services/export/dhis.spec.js#L513-L555), accessed 2026-09-08 | Lookup uses the selected timestamp; the explicit test setting uses `month_start_date: 1`. This locates work but does not prove the proposed non-default fix, writer semantics, or end-to-end behavior. |
| CHT #10241 still lacks a chosen concurrency design in the inspected discussion. | Interpretation / B | [Issue](https://github.com/medic/cht-core/issues/10241), [design objection](https://github.com/medic/cht-core/issues/10241#issuecomment-4204494893), accessed 2026-09-08 | Open, unassigned, six comments; last update 2026-04-08. Maintainer opposed a global queue; later alternatives remain proposals. Keep parked unless maintainers select a bounded approach. |
| Crisis Cleanup #1164 is still insufficiently current for implementation. | Interpretation / C | [Issue](https://github.com/CrisisCleanup/crisiscleanup-4-web/issues/1164), accessed 2026-09-08 | Open, unassigned, zero comments, last update 2024-10-02. It could still be real, or the observed outage could have been transient. A synthetic reproduction and maintainer interest would weaken the stopping rationale. |

## Policy correction

The [April 21 PR comment](https://github.com/medic/cht-core/pull/10824#issuecomment-4291383055)
prohibited AI-generated translations at that time. The current
[translation guide](https://docs.communityhealthtoolkit.org/community/contributing/translations/),
accessed 2026-09-08 and labelled updated May 7, 2026, permits tool-assisted drafts
but requires fluent-speaker validation before merge. Preserve the comment as
history and use the later published guidance for preparation. English placeholders
alone are not evidence that the current translation process is complete. Any
forum validation request remains an external message requiring user authorization.

The [AI guidelines](https://docs.communityhealthtoolkit.org/community/contributing/ai-guidelines/)
require disclosure of the tool and its role while retaining contributor
responsibility for understanding, review, tests, and dependency compatibility.
The [workflow](https://docs.communityhealthtoolkit.org/community/contributing/code/workflow/)
requires a reviewed PR, issue linkage, and testing evidence. Both were accessed
2026-09-08 and are now cited by the CHT policy gates instead of merely being
described as identified documents.

## Next decision and best test

The existing #10155 inquiry draft is ready for owner review with the translation
wording corrected. It has historical reviewer guidance and a local preparation
patch, but needs current confirmation and independent UI/test execution before
advancing. Do not treat the prior contributor's CI-flakiness claim as established.

If #11342 is confirmed instead, the highest-value test is a synthetic non-default
Bikram Sambat month-start case in the pinned DHIS test file, checked against the
writer's interval semantics. The root package defines `npm run unit-api`, but
setup hooks and services must be inspected before running target setup. Neither
candidate has earned an implementation go-ahead in this recheck.
