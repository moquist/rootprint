# Design

## Context

See proposal. Compact transport/checks already exist in `ec80fd0`; its oversized
snapshot also carries the full pooling plan and a changed ledger baseline.

## Goals / Non-Goals

**Goal:** reviewable compact-only stage. **Non-goals:** pooling, new limits/dependencies.

## Decisions

Reuse `compact()`/`model_content()` for accounting and transport, rather than two
serializations. Keep inline source, separate logical PNG blocks and existing labels.
Assemble from `4cb1791` with only this plan, compact code and focused check. Preserve
the full pooling plan and handoffs on the pooling/backup branches and in Git;
keep the candidate ledger at its tested base to avoid another baseline copy.

## Risks / Trade-offs

Sizing may still fail → measure exact trees with 8,192 bytes discussion headroom;
pause on overflow. Snapshot assembly is not omission from collected context.

## Migration Plan

Owner deploys ledger, compatible tests, this stage, then pooling through fresh CI
and App review; no agent push. Record evidence on the pooling ledger and in local
commit messages. Roll back through normal gates. Sync bootstrap/PNG before archive.
