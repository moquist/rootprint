# Proposal

## Why

Issue #12 requests a simple stdin-to-Merkle-root CLI demonstration. The owner's
clarifying comment asks to promote the existing CLI examples to the primary
README demos and demote inline Node/Python programs to secondary examples.
Both CLIs already provide this behavior; the remaining change is discoverability.

## What Changes

- Lead the primary README's usage section with short JSON stdin pipeline examples
  for both TypeScript/Node.js and Python, using the existing local CLI commands.
- Explain that stdout is one JSON hash record whose `digest` is the full Merkle
  root; the UTC timestamp and label vary between runs.
- Move the existing inline API examples below the CLI demos as secondary usage,
  retaining their fixed-clock explanation and links to package API documentation.
- Preserve setup, all-tests commands, file/installed CLI guidance, and unpublished
  package status. No new CLI, output mode, dependency, or protocol change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `automated-maintenance`: require CLI-first primary README usage examples for
  the existing ports. The baseline requirement currently lives in
  `bootstrap-rootprint-ecosystem/specs/automated-maintenance/spec.md`; main specs
  are not synchronized. Do not archive this dependent delta before that baseline.

## Impact

Implementation is expected to touch only `README.md` plus planning/verification
records. Existing `scripts/test_integration.py` source CLI checks and
`scripts/package_check.py` installed CLI checks remain the behavioral coverage.
Both ports, shared vectors, and published `rootprint-v1` bytes remain unchanged.
Implementation belongs to a subsequent phase. No remote activation is required
for the documentation itself; current-head CI and independent review remain
required before the owner merges the eventual PR.
