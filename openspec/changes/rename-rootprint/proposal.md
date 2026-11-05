# Proposal

## Why

The product is named Rootprint, but package names, Python imports, CLI commands,
protocol tags, and repository paths still use the previous name. The owner
explicitly confirmed a complete rename, including protocol bytes and consequently
all hash expectations, before publication.

## What Changes

- **BREAKING**: Rename both packages, Python module, imports, executable commands,
  diagnostics, workspace metadata, and maintained repository references to
  `rootprint` (display name `Rootprint`). Rename affected source and change paths.
- **BREAKING**: Use `rootprint-v1` in record identities and every recursive node
  preimage. Independently recompute all full digests and custom-provider vectors;
  retaining the old digests would be incorrect.
- Preserve the in-progress versioned-label format with `v1` derived from
  `rootprint-v1`. Reconcile bootstrap and `version-hash-labels` planning so their
  byte-preservation clauses refer to the renamed protocol baseline, not the
  superseded pre-publication identity.
- Keep the permanent primary README requirement: simple usage examples for each
  implementation and copy-and-paste setup/all-tests commands, including
  cross-language and installed CLI checks.
- Finish the already-planned synchronization design note without implementing
  synchronization or claiming it is active.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `json-merkle`: Rootprint package/module/CLI naming and `rootprint-v1` recursive
  framing with independently verified, cross-language expectations.
- `hash-records`: `rootprint-v1` record identities and protocol-derived `v1`
  labels, with newly computed full digests.

## Impact

Both packages, Python source directory, lockfile, tests, oracle, package checks,
mutation checks, documentation, agent instructions, OpenSpec config and active
change paths/artifacts are affected. No new runtime dependency or compatibility
alias is needed; neither package is published. Existing Git history and external
account/registry ownership are not rewritten by a repository rename.

There are no main specs yet. Bootstrap introduces both capabilities; this delta
uses its active requirements and the in-progress `version-hash-labels` change as
its baseline. Apply must reconcile all three plans, preserve unrelated incomplete
tasks, and establish one consistent baseline before any dependent archive.
