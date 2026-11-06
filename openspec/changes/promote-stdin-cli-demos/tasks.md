# Tasks

## 1. Primary README usage

- [x] 1.1 Promote both existing stdin CLI pipelines ahead of all inline API programs in `README.md`; retain local setup prerequisites, installed/file CLI guidance, unpublished status, and package README links. Verify the rendered heading/order makes the CLI demos primary for both ports.
- [x] 1.2 Explain the JSON record's full `digest`, label-only prefix length, and variable current UTC metadata; move both existing inline API programs and their fixed-clock output explanation below the CLIs as explicitly secondary examples. Verify the fixed-clock claim does not apply to CLI runs and setup/all-tests blocks remain intact/current.

## 2. Verification and handoff

- [x] 2.1 Execute both exact README stdin pipelines after setup and parse their JSON stdout to verify `rootprint-v1`, `sha256`, the expected full digest in the delta spec, and the 24-character label suffix. Execute both retained inline API examples and verify their fixed-clock digest/label output; record commands/results in `docs/local-work.md`.
- [x] 2.2 Run `python3 scripts/check.py`, `python3 scripts/package_check.py`, `node_modules/.bin/openspec validate --all --strict`, and `git diff --check` with the configured sandbox interpreter. Record actual results and review the full diff for unchanged CLI behavior, protocol/vector bytes, and current README all-tests instructions.
- [x] 2.3 Record the contract, verification evidence, and remaining latest-revision CI/independent-review/owner-merge gates in `docs/local-work.md`. Leave bootstrap and dependent changes unarchived until their acceptance and baseline synchronization prerequisites are met; do not claim issue completion before owner merge.
