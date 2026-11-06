# Spec Delta

## ADDED Requirements

### Requirement: Exact compact review transport
Independent review SHALL use compact UTF-8 JSON and reject requests exceeding 600,000 bytes across all task-text and image-label blocks before model invocation. Serialization SHALL preserve exact source text, discussions, and version identities. Existing per-file/image limits, credential exclusions, tool-free requests, App attribution, cache invalidation and freshness checks SHALL remain enforced.

#### Scenario: Exact text boundary
- **WHEN** complete transmitted task and label text fits the limit
- **THEN** it is accepted without changing embedded contents
- **AND** exceeding that limit blocks the model request without truncation
