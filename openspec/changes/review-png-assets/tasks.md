# Tasks

## 1. PNG collection and validation

- [x] 1.1 Record the owner's no-agent-push instruction for interactive local work in `AGENTS.md` and operations documentation; verify local work/activation instructions assign pushes to the owner and do not request agent push access.
- [x] 1.2 Add bounded PNG byte retrieval and static structural/header/CRC validation in the existing reviewer; extend its tests and limits documentation to verify valid PNGs above the text ceiling are accepted, while bad signatures/chunks/CRCs, animation, excessive dimensions/pixels/bytes, symlinks, and unsupported binaries block before model invocation.
- [x] 1.3 Collect labeled baseline/head image versions and enforce four-version/2 MiB aggregate budgets separately from text; verify add/modify/rename/delete cases and unchanged text budgets with fake immutable Git blobs and the supplied logo bytes from `docs/readme-logo`.

## 2. Multimodal review and preserved gates

- [x] 2.1 Send the text manifest plus labeled inline PNG image blocks through the existing tool-free Responses request; verify captured fake-transport payloads contain actual image data, correct path/SHA/role labels, no external image URLs, no credentials, no tools, and no conversation history.
- [x] 2.2 Accept image findings only for supplied image paths with line zero, and update the trusted review policy and reviewer/setup documentation; verify blocking findings, malformed/refused output, prompt-like image content, stale-head changes, App identity, credential exclusions, and existing binary rejection remain fail-closed in the reviewer acceptance checks.

## 3. Integrated and hosted acceptance

- [x] 3.1 Run `python3 scripts/check.py` using the configured development environment, strict OpenSpec validation, and `git diff --check`; record results and verified local commits without pushing or claiming hosted activation.
- [ ] 3.2 After the owner pushes and deploys PNG support, refresh the logo branch against the updated base and verify the controlled PR's visual review, exact-head reviewer App attribution, fresh CI/review after another commit, and blocking behavior under the no-bypass ruleset; record actual PR/check/run URLs and leave this task open while hosted evidence is unavailable.

## Workflow follow-up

- The owner performs every push; agents prepare local changes/commits and owner-run commands only.
- Archive/synchronize the bootstrap maintenance baseline before this additive delta, and only after this change's own verification is complete.
- Keep automatic merging disabled during the owner-controlled manual-merge rollout.

## Deployment evidence — 2026-11-06

- Owner rebase-merged https://github.com/moquist/rootprint/pull/8 at `ecbce4f`.
- Reviewer App approved its exact head: https://github.com/moquist/rootprint/actions/runs/42171395028. Two earlier HTTP 429 failures were resolved after the owner added OpenAI credits.
- Implementation rebased onto that base; runtime/policy/test bytes remain identical to the verified original. SSH fetch failed (publickey); authenticated HTTPS fetch succeeded without changing remote configuration.
- Further handoff evidence lives here to avoid adding the large ledger's baseline to this PR. Task 3.2 remains open; no agent push or merge occurred.
- Rebased verification passes: both ports, 29 script tests, Ruff, strict specs, and diff checks. Deployed-reviewer replay fits 600,000 bytes with a 2,048-byte discussion allowance; exact size is recorded in the verification commit.

## Hosted logo acceptance — in progress

- PR: https://github.com/moquist/rootprint/pull/10. Initial head `6dba341` passed visual review from App `5631539`; the review explicitly inspected the PNG motif/wordmark: https://github.com/moquist/rootprint/actions/runs/42172497614. Initial CI passed: https://github.com/moquist/rootprint/actions/runs/42172498444. GitHub reported `CLEAN`/`MERGEABLE`.
- Owner pushed alt-text commit `1c1c2e58fb3699c0598a7fc5b96e1915740039c6`. API inspection captured `BLOCKED` with new-head checks pending and no inherited reviewer approval.
- Fresh CI succeeded from Actions App `15368`: https://github.com/moquist/rootprint/actions/runs/42172939856. Fresh review failed HTTP 429 from App `5631539`: https://github.com/moquist/rootprint/actions/runs/42172937250. GitHub remained `BLOCKED` after CI succeeded; old-head approval did not satisfy the new-head review gate.
- Ruleset `26673301` remains active, bypass actors empty, current user bypass `never`, strict required checks bound to the two App IDs, and rebase-only/linear-history enforcement enabled.
- Task 3.2 stays open until fresh review succeeds on this head. Provider quota/rate-limit diagnosis and an owner-authorized retry remain pending. Evidence is on local `docs/png-review-acceptance`; the pushed logo branch/head is unchanged. No agent push or merge occurred.
