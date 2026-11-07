# GitHub automation setup

Use GitHub-hosted runners for CI, an OpenCode issue worker for implementation,
and an independent automated review gate before merging.

Start with AI-prepared PRs that you merge manually after the required checks
pass. Enable automatic merging later, when you are comfortable with the flow.
This is a staged rollout toward the specified fully automated workflow.

The repository contains CI, issue forms, and an issue worker that is disabled by
default for new deployments. Recorded hosted evidence for `moquist/rootprint`
includes the CI matrix, independent reviewer App attribution and merge gates, and
a documentation issue-to-manual-merge run. See `docs/local-work.md` for evidence
and remaining worker acceptance. This guide describes setup for a deployment;
`python scripts/activation.py` reports historical evidence, not live health.
Automatic merging remains a later integration.

Existing-PR repairs are implemented locally and require deployment plus controlled
hosted acceptance. Initial `ready` covers bounded repairs on the same worker PR,
sharing three attempts with initial implementation. The workflow's token gains
only explicit Actions/checks/PR/contents/issues read permissions for diagnostics;
App writes and the manual owner merge remain unchanged. See the worker guide for
legacy authorization, operational blockers and publication recovery.

## Rollout stages

1. **CI only:** verify that GitHub tests PRs successfully.
2. **AI-prepared PRs, manual merging:** you choose issues by applying `ready`;
   the worker implements them and opens PRs. CI and independent automated review
   must pass, then you click **Merge** when ready.
3. **Automatic merging:** explicitly enable the worker to request auto-merge
   after verifying a controlled automatic merge run.

The manual merge click is a temporary owner-controlled activation step, not a
required human code-review approval. The implementation and review pipeline is
the same in stages 2 and 3.

## 1. Create the repository and push

Create a GitHub repository with your preferred visibility.
The owner runs every push during interactive local work; agents prepare verified
local commits and commands, without pushing or requesting push credentials.
From the local repository, replace `OWNER` and `REPOSITORY` and run:

```sh
git remote add origin git@github.com:OWNER/REPOSITORY.git
git push -u origin main
```

If `origin` already exists, check it with `git remote -v` before changing it.

## 2. Enable Actions and permit the required actions

Open **Settings → Actions → General → Actions permissions**.

The current `.github/workflows/ci.yml` uses exactly these actions:

| Action | Purpose |
| --- | --- |
| `actions/checkout` | Check out repository source |
| `actions/setup-node` | Install Node.js |
| `actions/setup-python` | Install Python |

Choose one of these configurations:

- **Allow all actions and reusable workflows**; or
- **Allow OWNER, and select non-OWNER, actions and reusable workflows**, then
  enable **Allow actions created by GitHub**. All three actions above are
  maintained by GitHub.

For a narrower allowlist, use **Allow specified actions and reusable workflows**
and enter:

```text
actions/checkout@*,
actions/setup-node@*,
actions/setup-python@*
```

The workflow pins each action to a specific commit SHA. The `@*` allowlist permits
those pinned references.

Keep the default workflow token permission **read-only**. Organization policies
may also restrict available actions and must permit these actions.

## 3. Verify hosted CI

You do not need to register runners. The workflow requests GitHub-hosted runners
automatically through `runs-on`.

The current matrix runs:

- Linux, macOS, and Windows with Node.js 22 and Python 3.11.
- An additional Linux job with Node.js 24 and Python 3.14.

It runs both language suites, cross-language checks, static checks, OpenSpec
validation, and packaged CLI checks. The aggregate check is named **`ci`**.

Open the **Actions** tab after pushing and confirm every matrix job and `ci`
succeed. Private repositories may require an Actions spending budget for hosted
runner minutes.

## 4. Create the automation identities

Create a GitHub App for the implementation worker and install it only on this
repository. Give it these repository permissions:

| Permission | Access | Purpose |
| --- | --- | --- |
| Metadata | Read | Repository information |
| Issues | Read/write | Triage, questions, labels, and evidence |
| Contents | Read/write | Push implementation branches |
| Pull requests | Read/write | Create/update PRs; later, request auto-merge |

Use short-lived installation tokens. App-generated branch pushes and PRs trigger
normal CI. Events generated with the workflow's ordinary `GITHUB_TOKEN` generally
do not trigger additional workflows, apart from documented exceptions such as
explicit workflow dispatch.

Create a separate reviewer App with read access to contents and pull requests,
and write access to checks. It will produce **`independent-review`**. Keep its
credential out of the implementation worker.

Store its PEM as Actions secret **`REVIEWER_APP_PRIVATE_KEY`** and its App ID as
Actions variable **`REVIEWER_APP_ID`**. After deploying the reviewer, set variable
**`INDEPENDENT_REVIEW_ENABLED=true`** for a controlled PR. It uses the existing
**`OPENAI_API_KEY`**, with a fresh tool-free GPT-6.1 Sol request. See
[reviewer setup](docs/independent-review.md) for exact permissions, checks,
retry behavior, and hosted acceptance steps. The reviewer workflow does not
receive the implementation App's private key.

Provision model access and a spending limit for the trusted orchestration
service. Installing Apps and provisioning credentials are account-owner setup
steps. The worker uses OpenAI **GPT-6.1 Sol** (`openai/gpt-6.1-sol`). Store the
provider credential as Actions secret **`OPENAI_API_KEY`**, the implementation
App's PEM as **`IMPLEMENTATION_APP_PRIVATE_KEY`**, and its App ID as Actions
variable **`IMPLEMENTATION_APP_ID`**. The worker does not receive the reviewer
App's credential. See [the worker guide](docs/issue-worker.md) for the complete
setup and execution boundary.

## 5. Configure the issue worker

Use the existing forms in `.github/ISSUE_TEMPLATE/` for bugs and new requirements.
The included `.github/workflows/issue-worker.yml` provides trusted orchestration
for:

- New and reopened issues: triage and likely-duplicate detection.
- Issue edits and relevant comments: resume when missing information arrives.
- Scheduled reconciliation: recover missed events and interrupted work.

Keep the Actions variable **`ISSUE_WORKER_ENABLED`** unset or `false` until you
are ready for the controlled run. Set it to `true` to enable triage and
reconciliation; implementation still requires your `ready` label. The workflow
builds a credential-free container and checks isolation, the OpenCode/MCP
connection, and offline baseline tests before supplying worker credentials.
GitHub App/API access and real OpenAI model access require live verification.

The intended flow is:

```text
Issue
  → triage
  → request missing information, or mark ready
  → OpenCode plan/spec phase
  → separate implementation phase
  → sandboxed verification
  → App pushes branch and opens linked PR
  → CI + independent review
  → owner clicks Merge (initially); automatic merge later
  → issue outcome recorded
```

Follow `docs/automation.md` and the automated-maintenance specification under
`openspec/changes/bootstrap-rootprint-ecosystem/specs/`:

- For bugs, reference the existing requirement and demonstrate a failing
  regression check before fixing it.
- For new behavior, create or update an OpenSpec change before implementation.
- Ask a focused issue question when requirements have material ambiguity.
- Keep TypeScript, Python, and shared conformance vectors compatible.
- Use durable states: `triage`, `needs-information`, `ready`, `in-progress`,
  `blocked`, and `done`.
- Permit one worker per issue and enforce a 30-minute run timeout.
- Allow at most three failed implementation attempts per issue revision.
- Persist attempt counts and run links. Reopening an unchanged issue must not
  reset an exhausted attempt budget.
- Deduplicate failure tracking instead of opening an issue for every repeated
  failure.

Initially, have the owner apply `ready` to controlled test issues. Enable
automatic readiness decisions separately, after verifying the complete flow.
For the manual-merge stage, the worker must stop at a checked, independently
reviewed PR and wait for the owner to merge it. It must not call the merge API
or request auto-merge. Record the issue as done only after the PR is merged.

## 6. Isolate credentials from code execution

A disposable GitHub-hosted VM does not isolate secrets from commands executing
in the same job. Use these boundaries:

| Component | Access |
| --- | --- |
| Trusted orchestrator | Model access, scoped App token, issue/run state |
| Implementation sandbox | Source and test tools; no provider, repository-write, or publishing credentials |
| Independent reviewer | Diff/spec evidence and model access; no execution of PR code |
| CI runners | Read-only checkout and test tools; no provider, repository-write, or publishing credentials |

The orchestrator can collect a patch from the sandbox and push it using the App.
Do not place provider credentials and repository-write credentials beside an
unrestricted agent shell. Treat issue text, PR text, and repository content as
untrusted input.

Use a fresh review context to assess acceptance scenarios, regression evidence,
error paths, protocol compatibility, and trust boundaries. Attach its result to
the exact PR head SHA and rerun review after each new commit.

## 7. Configure merge gates

After verifying the reviewer App publishes `independent-review` on a controlled
PR's head SHA, open
**Settings → Rules → Rulesets** and protect `main` with:

- Require a pull request.
- Allow only **Rebase and merge** and require linear history. In repository
  settings, enable rebase merging and disable squash merging and merge commits.
- Require the **`ci`** status check.
- Require **`independent-review`**, restricted to the reviewer App as its source.
- Block force pushes and branch deletion.
- Configure no bypass actors.
- Do not require routine human approval.

Check that the repository's visibility and GitHub plan support the required
ruleset enforcement.

Initially, leave **Allow auto-merge** disabled in repository settings and keep
the worker's merge operations disabled. You click **Merge** after the required
checks pass on the latest revision. Keep all the gates above in place for
manual merges as well as automatic merges.

## 8. Verify one controlled issue-to-manual-merge run

Use a small bug report to demonstrate:

1. Triage and a linked existing contract.
2. A regression check failing before the fix.
3. A linked implementation PR.
4. Successful hosted CI across the configured matrix.
5. Independent review passing on the latest PR head SHA.
6. A subsequent commit requiring fresh review and CI evidence.
7. You click **Merge** after the required checks pass, and the worker records
   the outcome on the issue.

Also verify that missing-information reports pause, exhausted attempts become
blocked, and malicious issue content cannot obtain credentials or bypass policy.

Record live evidence in `docs/local-work.md`; do not claim activation based on a
push alone. You can remain at this stage for as long as you like, selecting
issues with `ready` and merging the resulting PRs yourself. This verifies the
manual-merge stage, not automatic merging or full autonomous maintenance.

Image assets such as the README logo are excluded from automated content review.
No image validation or visual acceptance sequence is required. The reviewer still
reviews README text and changed path metadata; see
[image exclusion](docs/independent-review.md#review-behavior). The owner performs
all pushes; ordinary current-head CI and independent review remain required.

## 9. Enable automatic merging later

When you are ready:

1. Enable **Allow auto-merge** in repository settings.
2. Implement and enable the worker's auto-merge request for one controlled PR,
   using rebase merging. GitHub must enforce the same required checks and
   rebase-only, linear-history policy.
3. Verify that failed, missing, or stale CI/review checks prevent merging, and
   that new commits require fresh checks and independent review.
4. Verify that the controlled PR merges automatically only after all required
   checks pass on its latest revision, and its issue records the outcome.
5. Record the evidence in `docs/local-work.md`, then enable unattended merging.

Automatic readiness decisions and unattended issue handling can be enabled
separately; enabling auto-merge does not require giving up owner-selected issues.
To return to manual merging, disable the worker's merge operations and repository
auto-merge, and cancel any pending auto-merge requests.

## 10. Keep publishing as a separate setup step

CI and issue automation do not publish packages. Configure npm/PyPI ownership,
publishing identities, and verified release automation separately, following
`docs/automation.md`.

## Existing project references

- `.github/workflows/ci.yml`: prepared hosted CI.
- `.github/ISSUE_TEMPLATE/`: bug and feature intake forms.
- `AGENTS.md`: agent operating instructions.
- `docs/automation.md`: activation sequence and worker contract.
- `docs/local-work.md`: verification evidence and remaining activation work.
- `openspec/changes/bootstrap-rootprint-ecosystem/specs/automated-maintenance/spec.md`:
  automation requirements.
- `python scripts/activation.py`: current activation-status report.
