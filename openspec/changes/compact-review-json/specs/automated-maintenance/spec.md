# Spec Delta

## ADDED Requirements

### Requirement: Exact compact review transport
Independent review SHALL use compact UTF-8 JSON and reject requests exceeding 600,000 bytes of task text before model invocation. Serialization SHALL preserve exact included source text, discussions, and revision identities. Image contents SHALL be excluded as specified by `exclude-images-from-review`. Existing text per-file limits, credential exclusions, tool-free requests, App attribution, cache invalidation and freshness checks SHALL remain enforced.

#### Scenario: Exact text boundary
- **WHEN** complete transmitted task text fits the limit
- **THEN** it is accepted without changing embedded contents
- **AND** exceeding that limit blocks the model request without truncation
