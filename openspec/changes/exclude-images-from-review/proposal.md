# Proposal

## Why

The owner wants a README logo, not automated visual inspection or a custom PNG
validator. The approved plan removes image review and makes that exclusion explicit.

## What Changes

- Exclude common image assets from review content without fetching or validating
  their bytes; retain changed paths and modes as metadata.
- Remove PNG parsing, budgets, visual transport, and image-specific findings.
- Reconcile active PNG and compact-JSON requirements, policy, tests, and docs.

## Capabilities

### Modified Capabilities

- `automated-maintenance`: explicitly exclude image content from independent review.

## Impact

Reviewer script, acceptance checks, trusted policy, and operational documentation.
The README logo stays. No dependencies, protocol changes, or remote operations.
