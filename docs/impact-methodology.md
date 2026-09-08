# Impact Methodology

Humanifest scores opportunities from supplied evidence, not from scraped popularity alone.

Evidence types:

- `measured`: independently observed outcome or direct operational measurement.
- `modeled`: estimate derived from an explicit model.
- `self_reported`: project, steward, or organization claim.
- `inferred`: reasonable proxy that does not directly measure the claimed outcome.

Scores are directional and auditable. They are not causal estimates, funding recommendations, or claims that a particular pull request will improve lives.

The initial weights are:

- humanitarian benefit: `0.30`
- acceptance probability: `0.20`
- technical confidence: `0.20`
- review burden: `-0.20`
- deployment probability: `0.10`

Hard gates dominate scores. If any hard gate fails, the implementation score is zero.

Parked, declined, merged, and released records also have zero implementation score.
Raw scores remain available for auditing the supplied inputs, but reports list
candidates by state and ID rather than ranking blocked work by raw score.
Eligibility in single-record output covers only gates and state; portfolio capacity
and authorization remain separate requirements.
