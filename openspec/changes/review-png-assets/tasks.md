# Tasks

## 1. PNG collection and validation

- [ ] 1.1 Record the owner's no-agent-push instruction for interactive local work in `AGENTS.md` and operations documentation; verify local work/activation instructions assign pushes to the owner and do not request agent push access.
- [ ] 1.2 Add bounded PNG byte retrieval and static structural/header/CRC validation in the existing reviewer; extend its tests and limits documentation to verify valid PNGs above the text ceiling are accepted, while bad signatures/chunks/CRCs, animation, excessive dimensions/pixels/bytes, symlinks, and unsupported binaries block before model invocation.
- [ ] 1.3 Collect labeled baseline/head image versions and enforce four-version/2 MiB aggregate budgets separately from text; verify add/modify/rename/delete cases and unchanged text budgets with fake immutable Git blobs and the supplied logo bytes from `docs/readme-logo`.

## 2. Multimodal review and preserved gates

- [ ] 2.1 Send the text manifest plus labeled inline PNG image blocks through the existing tool-free Responses request; verify captured fake-transport payloads contain actual image data, correct path/SHA/role labels, no external image URLs, no credentials, no tools, and no conversation history.
- [ ] 2.2 Accept image findings only for supplied image paths with line zero, and update the trusted review policy and reviewer/setup documentation; verify blocking findings, malformed/refused output, prompt-like image content, stale-head changes, App identity, credential exclusions, and existing binary rejection remain fail-closed in the reviewer acceptance checks.

## 3. Integrated and hosted acceptance

- [ ] 3.1 Run `python3 scripts/check.py` using the configured development environment, strict OpenSpec validation, and `git diff --check`; record results and verified local commits without pushing or claiming hosted activation.
- [ ] 3.2 After the owner pushes and deploys PNG support, refresh the logo branch against the updated base and verify the controlled PR's visual review, exact-head reviewer App attribution, fresh CI/review after another commit, and blocking behavior under the no-bypass ruleset; record actual PR/check/run URLs and leave this task open while hosted evidence is unavailable.

## Workflow follow-up

- The owner performs every push; agents prepare local changes/commits and owner-run commands only.
- Archive/synchronize the bootstrap maintenance baseline before this additive delta, and only after this change's own verification is complete.
- Keep automatic merging disabled during the owner-controlled manual-merge rollout.
