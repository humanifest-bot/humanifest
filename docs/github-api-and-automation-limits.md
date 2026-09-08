# GitHub API And Automation Limits

Humanifest must treat GitHub metadata as fallible.

Risks:

- search results can be stale or incomplete;
- labels such as `help wanted` do not prove maintainer capacity;
- issue openness does not prove the problem is current;
- comments can hide design decisions or ownership claims;
- rate limits and secondary limits make bulk automation fragile;
- content-generating API calls can trigger abuse controls;
- automated outreach can become spam even when technically allowed.

GitHub REST primary rate limits are higher for authenticated requests than unauthenticated requests, but search and content creation have stricter and secondary limits. GitHub also warns that continuing after rate limiting can lead to integration bans.

Humanifest response:

- prefer bounded read-only queries;
- cache source URLs and access dates;
- never automate issue comments, PRs, or maintainer messages without explicit user approval;
- treat maintainer confirmation as a hard gate;
- use GitHub metadata as a signal, not a decision.

Source: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api, accessed 2026-09-06.
