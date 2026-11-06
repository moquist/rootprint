# Proposal

## Why

PR #18 needs 683,256 bytes; the hosted 600,000-byte ceiling forces costly staging.
The owner approved raising it while pooling/scoping remain the long-term fixes.

## What Changes

- Hosted reviews use 1,200,000 UTF-8 task-text bytes, still failing on overflow.
- Preserve the standalone coordinator's 600,000-byte default and existing guards.
- Keep PR #18/image exclusion separate; do not rewrite that published branch.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `automated-maintenance`: a larger bounded hosted review budget.

## Impact

Trusted hosted entrypoint/workflow, focused checks and reviewer documentation.
No dependency, per-file limit, model-access or merge-gate change.
