# Design

## Context

See proposal. The deployed reviewer must review this bridge under its old ceiling.
Changing both the coordinator and its large existing test fixture adds substantial
baseline copies; the workflow already supplies a trusted source SHA for cache keys.

## Goals / Non-Goals

**Goal:** one reviewable budget bridge. **Non-goals:** image policy, pooling/scoping,
new dependencies, higher per-file limits or a claim about provider token capacity.

## Decisions

Use a small trusted hosted entrypoint to set the coordinator's existing
`MAX_CONTEXT` to 1,200,000 before calling its unchanged `main()`. Route only hosted
review execution through it; retain discovery and standalone defaults. Keep trusted
default-branch checkout and `REVIEW_SOURCE_SHA`, so deployment invalidates caches.
Document the hosted/default distinction and test the actual entrypoint with fake
orchestration, above-old/below-new input, exact boundaries and per-file rejection.

## Risks / Trade-offs

More input can cost more or exceed provider capacity → bounded input/output/time
limits and provider failures still block; pooling/scoping/usage work remains open.
Self-review may overflow → replay exact snapshots under the deployed collector;
do not bypass it. Store verbose evidence on the pooling ledger rather than adding
a ledger baseline to this small candidate.

## Migration Plan

Owner pushes/rebase-merges after CI/App approval; then refresh PR #18 on that base
and measure actual new context before requesting fresh checks. No automatic retry,
agent push or published-history rewrite. Sync baseline deltas before archive.
