# Maintainer Inquiry Draft: CHT #11342

Do not send without explicit user approval.

Hi CHT maintainers,

I am evaluating whether to prepare a small, tested contribution for [#11342](https://github.com/medic/cht-core/issues/11342), where DHIS2 export appears to read the wrong Bikram Sambat target month when `use_bikram_sambat_months` is enabled and `month_start_date` is not `1`.

Before doing implementation work, I wanted to check whether this is currently wanted and whether the intended direction is:

- derive the target-doc lookup key from the same reporting interval semantics used by the target writer, rather than from the raw selected `from` date;
- preserve existing Gregorian behavior;
- add a focused regression test using synthetic settings/target docs for non-default `month_start_date`.

If that direction is not right, I would be grateful for the preferred approach or a pointer to the right owner. I will avoid opening a PR unless a maintainer confirms the work is appropriate.

AI assistance disclosure: I am using OpenAI Codex for code reading and planning, with human review and line-by-line responsibility for any proposed patch.
