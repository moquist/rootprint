# Tasks

## 1. Compact stage

- [x] 1.1 Assemble the minimal candidate from `4cb1791`; verify only this plan, compact code and focused check differ, with original pooling/history preserved.
- [x] 1.2 Verify captured UTF-8 transport, unchanged inline contents/PNG versions, exact label-inclusive byte boundaries and existing enforcement; run `python3 scripts/check.py`, strict specs and `git diff --check`.
- [ ] 1.3 Replay the exact immutable candidate through the original collector with 8,192-byte discussion headroom; record size/commits in Git and the pooling ledger, pausing on overflow.
- [ ] 1.4 After owner deployment, verify fresh exact-head CI and reviewer App evidence; keep open until hosted results exist.

## Workflow follow-up

- Apply separately; then refresh/verify pooling under `deduplicate-review-context`.
- Owner pushes/merges; synchronize bootstrap/PNG before archiving this delta.
