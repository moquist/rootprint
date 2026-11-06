# Proposal

## Why

The original reviewer cannot fit the pooling deployment. A compact-only probe
with the full pooling plan still costs 608,169 bytes including discussion headroom.

## What Changes

- Compact UTF-8 JSON and exact task/label accounting before source pooling.
- Carry this small plan; leave the full pooling plan for its later PR.
- Preserve source text, discussions, version identities, limits and review gates.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `automated-maintenance`: compact review transport; baseline in bootstrap/PNG deltas.

## Impact

Reviewer and focused transport check; no dependency or package/protocol change.
