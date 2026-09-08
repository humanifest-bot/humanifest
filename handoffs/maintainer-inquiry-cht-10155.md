# Maintainer Inquiry: CHT #10155

Authorized by the user on 2026-09-08, including routine follow-ups and a tested
PR after maintainer confirmation. Sent as `humanifest-bot` on 2026-09-08 at
19:02:19 UTC through the verified browser session. [Published comment](https://github.com/medic/cht-core/issues/10155#issuecomment-5590328371).
Do not send a duplicate. Await maintainer response. See
[current authorization](../docs/contribution-protocol.md#communication-authorization).

Hi CHT maintainers,

I saw that [#10155](https://github.com/medic/cht-core/issues/10155) is still open and that the previous PR [#10824](https://github.com/medic/cht-core/pull/10824) was closed stale rather than merged.

Would a replacement PR still be welcome for this? My planned scope is narrow:

- show a spinner while the edit-user modal is loading the required user details;
- do not render empty editable fields until the details are loaded;
- surface an error through the existing modal error path if loading fails;
- prevent submit while loading or after load failure;
- add focused admin controller tests for those states;
- follow the current translation process, including fluent-speaker validation where required.

I will avoid opening a PR unless this is still wanted.

AI assistance disclosure: Humanifest uses OpenAI Codex for source reading, patch preparation, and GitHub coordination. Any proposed PR will disclose the assistance used and the testing and review actually completed.
