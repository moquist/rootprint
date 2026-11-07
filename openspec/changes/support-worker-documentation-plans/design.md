# Design

## Context

See `proposal.md` and `specs/worker-issue-guidance/spec.md`. Observed at `01295c9`:
- Report validation already supports `maintenance`, but initial triage policy only
  describes bug/feature and `develop()` permits maintenance only in repair context.
- Every plan must cite an existing `openspec/` contract. There is no policy example
  showing how a prose-only request should satisfy that process requirement.
- The documentation output check exists only in `repair_pr()` and accepts broad
  suffixes, including Markdown that may actually be executable agent policy.
- `save()` renders a state/run footer, while callers supply ad hoc action prose.
  Generic exception advice suggests new information or retry even for planning bugs.
- Adding `ready` is enough: an authorized attempt's state save removes other
  lifecycle labels. Asking owners to remove `needs-information` manually is redundant.

The offline `/tmp/opencode/reproduce_documentation_plan.py` gives initial work a
maintenance report, an existing maintenance process contract and acceptance command.
It fails with `Maintenance classification is restricted to non-code repair acceptance`.
Issue #23's observed invalid-contract failure is another symptom of the missing route;
its exact model phase report is not available and is not inferred here.

## Goals / Non-Goals

**Goals:** Let an ordinary documentation issue reach a verified PR, and make each
published issue state tell its owner the supported next action or waiting condition.

**Non-Goals:** General code maintenance without bug/feature checks, automatic merging,
new retry authority, new credentials/services, editing #23 during planning, or folding
the separate clarification-history implementation into this change.

## Decisions

### 1. Reuse maintenance classification and existing process contracts

Teach triage/plan policy to select `maintenance` for documentation-only work with
unchanged runtime behavior and normative requirements. Permit that kind in initial
work and repair through the same `develop()` path. Keep classification agreement
between triage and plan; do not silently convert an invalid bug/feature plan into
maintenance to get past a guard.

The worker selects the existing automated-maintenance process contract: main spec
when present, otherwise bootstrap's unarchived maintenance delta. Keep `contract`
as a real OpenSpec reference; it describes the development process, while the issue
and approved comments supply the requested prose/scope. A `README.md` contract
value is still invalid, but the worker must now know the correct route without
asking a human to find internal paths.

Planning records target documentation, intended edits and runnable acceptance in
the existing structured report. Reuse `regression` for a sandbox acceptance command
(for example a short `python3 -c` assertion); maintenance does not need that command
to fail before editing or require a new permanent test file. No new OpenSpec change
or requirement delta is required for wording-only work. Code bugs still need failing-
before evidence; new behavior or requirement changes still need their feature plan.
Retain separate plan, implementation and completion plus final integrated/package checks.

### 2. Enforce documentation scope for both publication paths

Use one shared final-output check for maintenance, after completion has made all
its edits and before either initial publication or repair publication. Validate the
complete exported diff, not the model's description or only its implementation phase.

The current repository's documentation corpus is root `README.md`,
`github-automation-setup-instructions.md`, the two package `README.md` files, and
Markdown/text/reStructuredText under `docs/` (including the work ledger). Maintenance
additions/modifications remain regular non-executable files. Source, tests, package
metadata, workflows, `AGENTS.md`, `automation/` policy, `.opencode/` instructions and
normative OpenSpec artifacts are outside this route even when named `.md`.

Path/mode checks prevent executable/configuration changes; policy and independent
review must still distinguish editorial fixes from proposed normative behavior
changes in documentation. Do not weaken existing patch validation, contract checks
or required CI/review to accept a mislabeled task.

### 3. Render trusted next-step guidance in the existing issue comment

Use a small shared renderer at the state-comment boundary. Callers provide the
actual stage/blocking category and supported action, rather than guessing from
model-authored exception text. Keep the task question/reason separate from a clear
`Next step` section. No model call, new label, UI service or permission lookup is
needed just to render guidance. Include concrete issue/PR/run/workflow links where known.

| Situation | Guidance shown in the issue |
| --- | --- |
| Active triage, implementation or repair | Wait; follow the run link. No new readiness action while work is active. |
| Needs information | Answer the focused question here. The reply is re-triaged; add `ready` once scope is confirmed. Label cleanup is automatic. |
| Actionable but awaiting authorization | Add `ready`; the worker will consume it and start the authorized attempt. |
| Operational/setup blocker | Resolve the named prerequisite first; show the supported workflow/resume action for this initial-work or PR-repair context. |
| Deterministic invalid worker plan | Request a worker fix and follow diagnostics; do not ask the owner for internal paths or encourage an unchanged retry. |
| Retryable work with attempts left | Explain the remaining budget and the actual resume action; a readiness label does not reset attempts. |
| Exhausted attempts | Supply material new information and renewed readiness, or a write/maintain/admin collaborator explicitly uses `/rootprint retry`. Reopen/relabel alone does not reset it. |
| PR checks pending or repair ongoing | Link the PR/run, name the gate or repair stage and say to wait or resolve the specific blocker. |
| PR gates passed | Link the PR and tell the owner to review and Rebase and merge; no new `ready` label. |
| PR closed unmerged | Resolve the existing PR's disposition, such as reopen it if work should continue; no promise of an automatic replacement PR. |
| Merged/done | Link the merged PR; no further implementation action required. |

Centralize the wording, not the worker's decision-making. Known deterministic guard
failures must identify the worker/plan problem; unknown exceptions should conservatively
request investigation rather than promise a useful retry. Reviewer infrastructure
errors can point an eligible owner to Independent review dispatch with the PR number
and `retry` enabled after resolving setup. Never advise bypassing named gates.

Use the existing state comment and avoid rewrites for unchanged stage/reason/action.
Count guidance against its 60,000-character ceiling and preserve the per-phase
90,000-character input guard. If the coordinator cannot publish an issue comment,
it must not claim that it did; existing Actions diagnostics remain the fallback.

### 4. Compose with clarification history and existing authorization

`preserve-worker-clarification-context` is independently planned on another branch.
Both touch `save()`/policy, so reconcile against whichever version is merged first.
Preserved question history should contain the question, not this procedural footer;
rendered guidance is neither a human answer nor material new issue information.
Guidance must not reset attempts, grant `ready` or alter reviewer freshness rules.

## Risks / Trade-offs

- Model labels code/policy as documentation → shared final path/mode checks plus
  classification/contract validation and independent review; no suffix-only bypass.
- Vague or harmful retry prompts → trusted reason/action selection and scenario
  tests for both remaining and exhausted budgets, plus setup and planning defects.
- Prompt/status churn causes loops → reuse one comment and suppress identical updates.
- Guidance and clarification retention get conflated → separate rendering from
  retained task text and test both initial and repair pause paths.

## Migration Plan

Implement only in a separate apply phase. First reproduce the documentation route
failure in the permanent offline lifecycle tests, then land policy/route, shared
scope checks, guidance and corresponding tests/docs. Owner publishes through fresh
CI/independent review and manual rebase merge. Exercise a controlled self-contained
README-only request to isolate this route from the separate clarification defect;
verify a linked PR, useful issue prompts and continued manual approval. Record live
evidence separately. Keep unrelated activation tasks open and preserve state on rollback.
