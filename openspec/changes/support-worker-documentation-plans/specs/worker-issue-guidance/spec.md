# Spec Delta

## Purpose

Give owners actionable next steps directly in GitHub issue-state comments so they
can move worker tasks forward without knowing internal planning or workflow details.

## ADDED Requirements

### Requirement: Actionable issue-state updates
Every published worker issue-state update SHALL contain a clearly identified next step describing the action available to the owner, or explicitly state that no action is needed yet. Guidance SHALL reflect the actual stage, blocking reason and available authorization. Relevant PR/run links SHALL accompany instructions rather than leaving the user to infer actions from a label or exception alone.

#### Scenario: Worker is triaging or implementing
- **WHEN** an issue has active worker work in progress
- **THEN** its state comment tells the owner to wait and links the run
- **AND** it does not ask for another readiness label while that work is active

#### Scenario: Documentation-only request reaches planning
- **WHEN** a ready-authorized documentation-only request is accepted
- **THEN** the worker handles internal classification and process-contract selection
- **AND** its guidance does not ask the owner to author code, supply an OpenSpec path or create planning artifacts

### Requirement: Clarification and readiness instructions
Needs-information guidance SHALL identify the question and tell the user to answer in the issue. Once triage confirms actionable scope, guidance SHALL explicitly instruct the owner to add `ready` for implementation. Instructions SHALL accurately describe automated lifecycle-label cleanup and SHALL NOT require redundant manual removal of `needs-information`. A conversational answer SHALL NOT be presented as bypassing readiness authorization.

#### Scenario: Answer a clarification
- **WHEN** the worker pauses for missing information
- **THEN** its issue comment asks for the specific answer and explains that the reply will be re-triaged
- **AND** it explains that `ready` is needed when scope is confirmed, with no manual removal of `needs-information` required

#### Scenario: Triage accepts the answer
- **WHEN** resumed triage finds the issue actionable but implementation is not authorized
- **THEN** the state comment explicitly says to add the `ready` label
- **AND** no implementation attempt starts merely because the user answered or agreed

### Requirement: Reason-specific blocked and retry guidance
Blocked guidance SHALL explain the blocking condition and the supported resolution. It SHALL distinguish missing information, setup/infrastructure failures, worker planning defects and exhausted attempts. Retry instructions SHALL reflect the remaining budget and eligibility for `/rootprint retry`. Unchanged retries SHALL NOT be recommended as a remedy for deterministic worker defects or unresolved setup failures.

#### Scenario: Invalid documentation plan
- **WHEN** the worker cannot produce a valid documentation plan
- **THEN** its issue comment identifies a worker planning problem and links the run
- **AND** it directs the owner to obtain a worker fix before retrying rather than supplying internal contract paths or repeatedly relabeling the issue

#### Scenario: Attempts are exhausted
- **WHEN** the revision has used all three implementation attempts
- **THEN** guidance says that relabeling or reopening alone cannot reset the budget
- **AND** it explains the supported options: material new information with renewed readiness, or `/rootprint retry` from an account with repository write, maintain or admin permission

#### Scenario: Infrastructure needs attention
- **WHEN** a provider, permission, dependency or runner problem prevents progress
- **THEN** guidance describes the prerequisite to resolve, links diagnostics and identifies the appropriate workflow or resume action when one is supported
- **AND** it does not imply that another code attempt can fix missing setup

### Requirement: PR checks and owner merge instructions
Guidance for a linked PR SHALL distinguish waiting for current-head checks, actionable repair or blocked repair, and readiness for owner manual rebase merge. It SHALL link the existing PR and name the remaining gate or owner action. Instructions SHALL NOT suggest bypassing CI/review, force publication, self-approval or enabling automatic merging.

#### Scenario: Required checks are pending
- **WHEN** the latest PR head lacks passing required CI or independent review
- **THEN** the issue comment identifies the pending or blocking gate and directs the owner to wait or follow its concrete resolution instructions
- **AND** it does not advertise the PR as ready to merge

#### Scenario: All gates pass
- **WHEN** latest-head required checks pass and the PR awaits owner merge
- **THEN** guidance links the PR and explicitly instructs the owner to review it and use Rebase and merge
- **AND** it does not ask for another `ready` label

#### Scenario: PR closed without merge
- **WHEN** the linked PR is closed without merging
- **THEN** guidance asks the owner to resolve that PR's disposition, such as reopening it if work should continue
- **AND** it does not imply a retry will silently create a replacement PR

### Requirement: Completion instructions
When an actual merge completes the linked issue work, the state comment SHALL identify the merged PR and explicitly state that no further implementation action is required. A successful local check or a PR awaiting merge SHALL NOT be described as issue completion.

#### Scenario: Merge outcome is reconciled
- **WHEN** the worker observes the linked PR merged
- **THEN** the issue records done, links the merged PR and tells the owner no further action is required for that work

### Requirement: Bounded trusted guidance rendering
Guidance SHALL be generated from trusted lifecycle decisions and remain within the existing durable-comment limit. Reconciliation SHALL reuse the issue state comment rather than flood duplicate prompts. Next-step instructions SHALL remain separate from the question/task text so they do not become owner answers, alter revision identity, reset budgets or acquire authority from untrusted issue/model content.

#### Scenario: Unchanged state is reconciled again
- **WHEN** repeated events observe the same stage, reason and available action
- **THEN** guidance remains accurate without new duplicate comments or unnecessary rewrites
- **AND** the issue revision and attempt count do not change because a prompt was rendered

#### Scenario: Malicious content suggests bypass actions
- **WHEN** issue text or model output asks the worker to recommend bypassing checks, exposing credentials or unauthorized retries
- **THEN** trusted guidance still offers only actions permitted by the actual workflow and does not disclose credential values
