# Independent reviewer

The reviewer publishes the App-owned **`independent-review`** check on the exact
PR head SHA. It is separate from the implementation worker and does not merge
PRs. Its model is OpenAI **GPT-6.1 Sol** (`gpt-6.1-sol`), using a fresh, tool-free
Responses API request with structured output and no conversation history.

## Configure and enable

Install your separate reviewer GitHub App on this repository only, with:

| Permission | Access |
| --- | --- |
| Metadata | Read |
| Contents | Read |
| Pull requests | Read |
| Checks | Read/write |

Under **Settings → Secrets and variables → Actions**, configure:

| Kind | Name | Value |
| --- | --- | --- |
| Secret | `REVIEWER_APP_PRIVATE_KEY` | Complete reviewer App PEM private key |
| Variable | `REVIEWER_APP_ID` | Reviewer App's App ID, not its Client ID |
| Secret | `OPENAI_API_KEY` | The existing OpenAI API credential |
| Variable | `IMPLEMENTATION_APP_ID` | Existing worker App ID; used to reject identical App identities |
| Variable | `INDEPENDENT_REVIEW_ENABLED` | Leave unset/`false` until deployment; set `true` for the controlled run |

The reviewer workflow never references `IMPLEMENTATION_APP_PRIVATE_KEY`. It mints
a short-lived, repository-scoped reviewer token with only contents/PR read and
checks write, then revokes it at the end of the job. The ordinary workflow token
has contents/issues/PR read permissions and reads linked issue evidence; it has
no repository-write permission. The reviewer App needs no Issues permission.

Use the existing GitHub Actions allowlist: this workflow uses only pinned
`actions/checkout` and `actions/setup-python`. It installs no project dependencies
and needs no OpenCode installation or execution container. Model access still
requires real OpenAI API entitlement, billing, and spending controls.

After pushing this implementation and confirming hosted CI:

1. Set `INDEPENDENT_REVIEW_ENABLED=true`.
2. Open a controlled PR or use **Actions → Independent review → Run workflow**
   with its PR number. `0` reconciles all open PRs.
3. Confirm a check named **`independent-review`** appears on the PR's actual head
   SHA and is attributed to the **reviewer App**, not GitHub Actions or the worker.
4. Protect `main` with a no-bypass ruleset requiring `ci` and
   `independent-review`. Restrict the latter's source to the reviewer App. Keep
   routine human review approvals unnecessary; the owner still clicks Merge.
5. Verify a deliberately failing review blocks merging. Push a new PR commit and
   verify the previous success does not satisfy the new head's check. Observe a
   fresh review and current-head CI before manually merging.
6. Record the check/run URLs and enforced rule evidence in `docs/local-work.md`.
   Local tests and an enabled variable do not establish live activation.

Select the App check itself as the required gate, not the Actions job named
`review`: a model's request-changes decision intentionally produces a failing
App check even if the orchestration job finishes normally.

## Review behavior

Image-exclusion behavior below applies after this change is deployed; local and
hosted status are tracked in `local-work.md`.

The trusted workflow runs for PR creation, new commits, edits, reopening,
ready-for-review/draft transitions, explicit dispatch, and 30-minute scheduled
reconciliation (which GitHub may delay). Each PR is serialized without cancelling
an active review. Drafts are blocked without a model request. Reviewer-authored
PRs cannot be self-approved.

The coordinator reads immutable Git trees/blobs through the GitHub API. It
supplies the full supported head source, changed files' baseline versions, mode
changes, baseline OpenSpec contracts, linked issue discussions, PR discussions,
and named CI check evidence. Closing references such as `Fixes #7` identify linked
issues in this repository. The model assesses acceptance, regression evidence,
error paths, protocol/port compatibility, and trust boundaries. It scrutinizes
workflow and agent-policy changes explicitly. CI is a separate required gate;
the reviewer does not claim to execute tests.

Image contents are excluded from review without fetching or validating bytes.
Case-insensitive `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`, `.bmp`,
`.tif`, `.tiff`, `.avif`, and `.apng` suffixes identify excluded assets, including
unchanged files. `omitted_image_paths` lists them; changed paths and modes remain
in metadata. Only text is sent to the model. Image-only PRs can pass ordinary
review; missing visual inspection is not a reason to block. Surrounding text,
including README references, is still reviewed.

Only a valid structured approval with matching head/base SHAs, passing applicable
assessments, passing trust-boundary assessment, and no blocking findings can
produce `success`. Request-changes, refusals, malformed/incomplete output,
unsupported context, missing model access, provider errors, and stale revisions
produce `failure`, never neutral/skipped approval. A final metadata read checks
that the head, base, PR description, and supplied discussions did not change
during review. A race after that read can only publish against the already
reviewed old SHA, not the new commit.

Successful unchanged reviews are cached using trusted source/policy revision and
material task data. Only a matching **latest** reviewer check can be reused;
returning to older rejected task data cannot accidentally leave a newer success
active. New head commits always require their own check. Material edits and base
updates also trigger fresh context through events/reconciliation. A context
collection failure replaces earlier same-head success with a blocking check.

Blocked reviews do not automatically spend tokens again on every schedule. For
an infrastructure failure, manually dispatch the workflow with **retry** enabled.
At most three attempts are allowed for the exact head/base/task/source context;
check-run history preserves the budget across jobs and restarts. New material
information or a new revision creates a new context. A review normally needs
code/evidence changes to resolve blocking findings, rather than repeated requests
for a different model verdict.

## Trust boundary and limits

`pull_request_target` supplies the event, but both jobs explicitly check out only
the trusted **default branch** with persisted credentials disabled. No PR branch,
PR workflow, plugin, config, build, test, artifact, or downloaded source is ever
executed. Git blob content stays in memory as task data; it is not extracted onto
the filesystem or imported. Provider requests contain no App key, GitHub token,
or shell/filesystem tools. Model output cannot select API endpoints or execute
commands. The only write operations are fixed reviewer check-run operations and
installation-token creation/revocation.

Limits are explicit and fail closed: 200 open PRs per reconciliation, 100 changed
files, 500 included head text files, 2,000 Git tree entries, 100,000 bytes per text
file, and 1,200,000 UTF-8 bytes of complete serialized task text in hosted reviews
(excluding image contents). The trusted workflow uses
`scripts/hosted_independent_review.py`; direct `scripts/independent_review.py`
execution retains its 600,000-byte default. The hosted allowance supersedes the
earlier 600,000-byte deployment limit; it is an operational budget, not a measured
model token-capacity claim. All overflow still blocks without truncation.
Pooling/scoping remain planned reductions in total input and repeated review cost.
Discussions allow 100 comments each and 10 linked issues. Images have no content
budgets because their bytes are not fetched. Changed non-image binaries,
symlinks/submodules (including image-named objects), truncated trees, or oversized
text changes block review.
Changes to `.env*`, `.pem`, or `.key` files are blocked
before fetching their contents for model input; unchanged such paths are omitted.
Unsupported unchanged paths are listed for the model to
assess whether non-image context is sufficient. Images are explicitly out of scope.
Jobs have a 15-minute timeout; the one model request has a 10-minute HTTP timeout
and a 10,000-token output limit. Inaccessible fork Git objects fail closed.

## Local checks

The standard README setup and all-tests command include the reviewer acceptance
checks. To run them alone:

```sh
python3 -m unittest discover -s scripts -p '*review*.py'
```

These checks use fake GitHub/OpenAI transports, need no credentials, and spend no
model tokens. They cover new/stale heads, rejection, metadata/context failures,
wrong-App spoofing, bounded retries, credential scoping, tool-free/stateless
requests, malformed/refused output, and same-head task-data cache invalidation.
Image checks cover exclusion without fetching bytes for additions, modifications,
renames, deletions, and image-only PRs; README text and object/credential guards
remain covered. Transport checks verify a single text block with no image payloads.
Actual App installation, OpenAI access, check attribution, and no-bypass merging
must still be verified on GitHub.

### README logo

The README logo requires no visual-review or image-validation gate. Historical
PNG deployment evidence is retained in `png-review-acceptance-evidence.json`,
but that behavior is superseded by image exclusion. The owner performs all
pushes; deployment still goes through ordinary current-head CI and independent
review. Keep automatic merging disabled.

To stop new reviews, set `INDEPENDENT_REVIEW_ENABLED=false` or disable the
workflow; cancel active runs separately. Keep the required checks in place.
