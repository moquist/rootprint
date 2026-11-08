# Tasks

## 1. Regression evidence

- [x] 1.1 Add an offline lifecycle regression based on #23: worker question, short owner agreement, fresh worker, generic triage/attempt status save, then captured model context. Observe failure before fixing because the question is missing while the answer remains; reference bootstrap's existing automated-issue-lifecycle requirement and record the command/output in `docs/local-work.md`.

## 2. Durable clarification context

- [x] 2.1 Capture, validate and deduplicate clarification history in the shared durable-state path used by every needs-information result. Recover a still-present legacy question before status overwrite and retain history through later saves/restarts/retries. Verify multiple distinct questions survive, identical saves do not duplicate records, malformed/spoofed history is rejected, erased legacy text is not invented, and a candidate over the 60,000-character state limit cannot replace the last valid record. Document migration and state ceilings in the worker guide.
- [x] 2.2 Supply retained questions with complete bounded human answers and ordering/provenance to initial/resumed triage, downstream phases and existing-PR repair. Remove discussion clipping that can sever the pair while retaining the final 90,000-character guard on every request. Verify the regression passes after generic saves and fresh instances; long comments/more than ten replies are either complete or explicitly blocked; unanswered ambiguity still pauses; a stub triager sees question plus short answer and proceeds only with existing authorization; bot updates do not reset revision/budgets or retrigger unchanged work. Update trusted worker policy and operations guidance for untrusted clarification data and unchanged `ready`/retry/manual-merge behavior.

## 3. Verification and deployment evidence

- [x] 3.1 Run focused lifecycle/repair tests, credential-free `python3 scripts/check.py`, strict OpenSpec validation and `git diff --check`; inspect the complete affected flow/diff and record actual results before committing intended changes. Verify primary README usage/setup/all-tests commands remain current and no protocol/package/dependency/permission or unrelated activation requirement changed.
- [x] 3.2 After owner deployment through current-head CI and independent review, verify a fresh controlled issue asks a question, receives a short answer, waits for `ready`, and produces its linked PR without repeating the resolved question. Record issue/run/PR evidence and unchanged retry/manual-merge gates. Leave this task open until exercised; do not mutate #23 or treat its owner-managed workaround as deployed-fix acceptance.

## Workflow follow-up

- Apply this fix only after a separate implementation request; all five tasks remain unchecked during planning.
- Owner performs pushes and manual rebase merges; independent automated review and current-head CI remain required.
- Archive through the archive workflow after this change's acceptance is verified; no requirement delta needs syncing. Leave unrelated bootstrap/repair acceptance tasks open.
