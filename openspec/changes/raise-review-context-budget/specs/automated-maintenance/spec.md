# Spec Delta

## ADDED Requirements

### Requirement: Hosted review text headroom
Hosted independent review SHALL allow up to 1,200,000 UTF-8 bytes of complete task text, including labels/references, superseding earlier 600,000-byte hosted limits. Standalone coordinator default SHALL remain 600,000 bytes. Per-file limits, credential exclusions, complete structured assessments, freshness, cache invalidation and required App/CI gates SHALL remain enforced. Overflow SHALL block requests without truncation.

#### Scenario: Context between old and hosted ceilings
- **WHEN** complete hosted context exceeds 600,000 bytes but fits 1,200,000
- **THEN** collection proceeds without discarding source or discussions

#### Scenario: Bounds remain enforced
- **WHEN** text exceeds the hosted ceiling or a file exceeds its existing limit
- **THEN** review blocks before model invocation
