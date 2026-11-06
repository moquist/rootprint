# Worker build-context startup repair

The first worker run for issue #12 failed before triage or coordinator/model use:
https://github.com/moquist/rootprint/actions/runs/42175502467

```text
ERROR: failed to build: ambiguous Dockerfile source: both stdin and flag correspond to Dockerfiles
docker build -t rootprint-issue-worker:local -f automation/worker.Dockerfile -
```

This fixes the existing bootstrap sandbox/credential-isolation contract, not the
requested CLI behavior in issue #12. The coordinator never reserved an
implementation attempt or posted issue state in that failed run.

## Cause and fix

Buildx peeks at 1,024 stdin bytes. BuildKit recognizes compression signatures or
tries `archive/tar.Reader.Next` on that prefix. Python's PAX header and payload
can occupy the whole prefix, leaving no following file header: the probe returns
EOF and the archive is mistaken for a Dockerfile. Podman accepted the same input.

The shared builder now gzip-compresses the same filtered tar. Its signature is
recognized immediately; PAX/long paths, Git-tracked-file selection, credential
exclusions, and the cleared runtime environment are preserved.

## Verification

- `python3 -m unittest discover -s scripts -p test_worker_build.py` failed before
  the fix on the bounded PAX-header probe and passes after it. It also checks both
  runtime invocations, full archive contents/long paths, and credential exclusions.
- A Go standard-library probe of the actual repository context reproduced the
  Docker error (`tar` probe EOF) before and recognized gzip after the fix.
- `python3 scripts/check.py` passes both ports, 30 script tests, Ruff, and strict
  specs in the development virtualenv.
- Real `python3 scripts/worker_sandbox.py build --runtime podman` and
  `python3 scripts/worker_runtime_check.py --runtime podman` pass, including
  isolation/hostile-artifact probes, MCP startup, and offline integrated/package
  checks. No provider or GitHub credentials were supplied to these checks.

Docker is unavailable locally; full hosted Docker execution remains pending.
After the owner deploys the fix through CI/review and rebase-merges it, dispatch
`gh workflow run issue-worker.yml -f issue=12` to resume the controlled run.
Issue #12 remains untriaged; this repair does not authorize its implementation.
