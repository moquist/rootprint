# Tasks

## 1. Exclude image content

- [x] 1.1 Remove PNG parsing/transport and replace visual checks with image-exclusion and preserved blob-boundary tests; verify reviewer and compact transport checks.
- [x] 1.2 Reconcile active specs, reviewer policy and documentation; verify no current requirement demands image validation or visual acceptance.

## 2. Integration

- [x] 2.1 Run `python3 scripts/check.py` and `git diff --check`, record local evidence and commit verified changes.

## Workflow follow-up

- Owner pushes; current-head hosted CI and independent review precede remote merging.
- Synchronize bootstrap and superseded deltas before archiving this change.
