# Spec Delta

## Purpose

Carry authorized worker PRs through bounded repairs and fresh verification while
preserving isolated execution, an auditable attempt budget and owner-controlled merging.

## ADDED Requirements

### Requirement: Repair authorization and scope
Initial owner `ready` authorization SHALL cover implementation and bounded repairs of the linked worker PR for the authorized issue revision. Automation SHALL repair only that open, same-repository worker PR and branch. Changed requirements, closed issues, draft PRs, foreign branches or missing authorization evidence SHALL pause repair with a concrete status rather than implicitly adopt new work.

#### Scenario: Authorized PR fails
- **WHEN** an authorized worker PR has an actionable current-head failure
- **THEN** the worker can attempt repair without another owner approval for each attempt
- **AND** it retains the same issue, branch and PR

#### Scenario: Scope or authorization changes
- **WHEN** the issue revision changes, the issue closes, the PR becomes draft, or its identity no longer matches the authorized worker PR
- **THEN** the worker pauses and records what needs owner attention
- **AND** new issue information requires renewed `ready` authorization or an authorized retry before repair resumes

#### Scenario: Existing PR has no repair authorization record
- **WHEN** reconciliation finds a pre-deployment PR without durable authorization for repairs
- **THEN** it monitors the PR but does not launch repair until the owner explicitly authorizes it

### Requirement: Actionable current-head failure evidence
Repairs SHALL use complete, bounded diagnostics for the current PR head from expected CI and independent-review identities. Stale, spoofed, pending or missing checks SHALL NOT authorize a repair. Infrastructure failures, unavailable diagnostics and ambiguous requirements SHALL produce a blocked or needs-information state rather than speculative source changes. Review infrastructure errors SHALL be distinguishable from actionable rejection.

#### Scenario: CI or review identifies a code problem
- **WHEN** completed current-head CI from the expected Actions identity reports an actionable failure or the expected reviewer App supplies blocking findings
- **THEN** repair planning receives the failure identity, diagnostics, head/base identities and applicable contract

#### Scenario: Checks are pending or have been superseded
- **WHEN** checks are missing, pending, attached to an earlier head or replaced by a newer result
- **THEN** the worker waits or uses only the latest applicable evidence and does not repair from obsolete failures

#### Scenario: Infrastructure cannot supply actionable evidence
- **WHEN** review fails from a provider error, diagnostics are incomplete or oversized, or the failure cannot be classified as actionable
- **THEN** the worker records a bounded explanation and waits for intervention or new evidence without speculative commits

#### Scenario: An unrelated App reports failure
- **WHEN** a check with a familiar name comes from an unexpected identity
- **THEN** it cannot authorize a repair or satisfy a required gate

### Requirement: Shared durable attempt budget
Initial implementation and repair attempts SHALL share the maximum of three attempts per authorized issue revision. Each attempt SHALL be reserved durably before model execution. Worker commits, check reruns, duplicate events and restarts SHALL NOT reset that budget. Exhaustion SHALL block further implementation until new information is authorized or an eligible owner explicitly requests retry.

#### Scenario: Initial implementation used one attempt
- **WHEN** its PR needs repeated repairs under the same authorized revision
- **THEN** at most two additional implementation attempts are available
- **AND** unsuccessful attempts and interrupted model runs consume their reservations

#### Scenario: Duplicate events reconcile one failure
- **WHEN** scheduled and event-driven runs observe the same head and failure evidence
- **THEN** durable state and per-issue serialization prevent duplicate active attempts or duplicate publication

#### Scenario: Budget is exhausted
- **WHEN** three attempts have been reserved for the revision
- **THEN** the worker records blocked status, diagnostics and run links and does not launch a fourth attempt
- **AND** relabeling or reopening alone cannot reset the budget

### Requirement: Isolated repair planning and verification
Repairs SHALL start from the exact diagnosed PR head inside a credential-free execution sandbox using trusted orchestration. Planning, implementation and completion SHALL remain separate phases. Bug repairs SHALL have a runnable check observed failing before the fix and passing afterward. The exact completed tree SHALL pass applicable regression, integrated and package checks before publication. Untrusted diagnostics SHALL NOT alter trusted policy.

#### Scenario: Repair the diagnosed revision
- **WHEN** an attempt starts
- **THEN** the sandbox contains the diagnosed head, including its existing changes and deletions, rather than only default-branch source
- **AND** provider/write credentials and privileged execution remain outside that sandbox

#### Scenario: Repair violates an existing requirement
- **WHEN** a CI failure or blocking finding identifies a bug
- **THEN** planning references the existing contract and demonstrates a failing runnable regression before implementation
- **AND** completion verifies that regression and the final integrated/package checks

#### Scenario: Feedback needs a behavioral decision
- **WHEN** feedback requires a materially ambiguous requirement change
- **THEN** the worker asks a focused question and does not invent the decision

#### Scenario: Hostile feedback or source
- **WHEN** PR source or diagnostics request secrets, host execution or bypassed checks
- **THEN** they cannot change the credential boundary, allowed tools or required gates

### Requirement: Non-overwriting publication and recovery
A verified repair SHALL append a commit to the existing worker branch with the diagnosed head as parent, using a non-force update. The worker SHALL recheck issue revision, PR identity, head, base and failure applicability before publication. Changed inputs SHALL stop stale publication. Pending commit/publication identity SHALL be durable so lost responses are reconciled without creating another PR or overwriting intervening commits.

#### Scenario: Owner or another process changes the PR
- **WHEN** the head, base, issue revision or applicable failure changes during repair
- **THEN** the stale result is not published and reconciliation records the changed input
- **AND** intervening branch edits are preserved

#### Scenario: Branch changes during publication
- **WHEN** another commit races the repair's branch update
- **THEN** publication cannot force the repair over that commit
- **AND** the worker records the conflict instead of silently overwriting it

#### Scenario: Publication response is lost
- **WHEN** a repair commit or branch-update response is lost after the operation succeeds
- **THEN** reconciliation uses durable publication identity and the actual branch to recover the outcome
- **AND** it neither repeats model work for an already-published repair nor creates a second PR

### Requirement: Fresh checks and manual owner merge
Each repaired head SHALL require fresh CI and independent automated review under existing no-bypass, App-bound gates. This repair rollout SHALL NOT request merge or auto-merge, approve its own PR, or enable repository auto-merge. Once checks pass, the worker SHALL report readiness for the owner's manual rebase merge and mark the issue done only after observing an actual merge.

#### Scenario: Repair checks pass
- **WHEN** required CI and independent review pass for the latest repaired head
- **THEN** the existing PR remains open awaiting the owner's manual merge
- **AND** reconciliation records that it is ready for owner merge

#### Scenario: Old approval exists
- **WHEN** repair adds a commit after a successful review
- **THEN** old-head approval cannot satisfy the new head's gates
- **AND** missing, pending, failed or stale required checks prevent readiness for merge

#### Scenario: Owner merges or closes the PR
- **WHEN** reconciliation observes the owner has rebase-merged the PR
- **THEN** it records the merge and marks the linked issue done
- **AND** a PR closed without merging is recorded as blocked rather than repaired or recreated

### Requirement: Observable repair status
One durable issue state record SHALL identify repair authorization, issue revision, attempt number, diagnosed head, failure identity, run link and pending or published commit. Status SHALL distinguish waiting for checks, repairing, blocked or needs-information, and ready for owner merge without flooding duplicate comments. Activation reporting SHALL distinguish local checks, hosted acceptance and unverified behavior.

#### Scenario: Inspect a repair outcome
- **WHEN** an owner reads the issue state and linked PR
- **THEN** they can identify what failed, which attempt addressed it, the resulting commit and what action or check remains

#### Scenario: Local verification precedes deployment
- **WHEN** only local tests have passed
- **THEN** status does not claim that deployed automatic repair or hosted acceptance is complete
