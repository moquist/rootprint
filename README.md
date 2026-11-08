# Rootprint

![Rootprint wordmark beside a tree growing from a fingerprint-shaped footprint](rootprint-horizontal.png)

Rootprint provides deterministic, versioned Merkle hashing for JSON, with
bring-your-own hash functions. Initial implementations: **TypeScript and Python**.
Rust is planned after these implementations pass the same conformance vectors.

The name combines **root**, a Merkle tree's root hash (SHA-256 by default), with
**print**, a fingerprint of the data. Together, **Rootprint** is a play on
**footprint**: a compact mark representing a whole JSON document.

- Objects sort by RFC 8785 UTF-16 key order; arrays preserve order.
- Numbers use finite IEEE-754 binary64 semantics (not exact arbitrary precision).
- SHA-256 is the default; libraries accept custom fixed-output hash providers.
- Full content identity is `(protocol, algorithm, digest)`. UTC labels aid recognition:
  `20261102_090405-sha256-v1-d331f806a7ada530`.

`calculatedAt` is descriptive metadata and does not affect deterministic content identity.

## Setup and run all tests

From the repository root, with Node.js 22+, Python 3.11+, and OpenSSL on `PATH`,
copy and paste this block (Linux/macOS). OpenSpec 1.16.0 is pinned locally.

```sh
npm ci
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check.py
.venv/bin/python scripts/package_check.py
.venv/bin/python scripts/vector_reference.py --check
.venv/bin/python scripts/clean_check.py --mutations
```

On Windows PowerShell, use:

```powershell
npm ci
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe scripts/check.py
.venv\Scripts\python.exe scripts/package_check.py
.venv\Scripts\python.exe scripts/vector_reference.py --check
.venv\Scripts\python.exe scripts/clean_check.py --mutations
```

`check.py` builds/type-checks TypeScript, runs both language conformance suites,
cross-language integration (including timezone and source CLI checks), Python
static checks, and strict validation of every active OpenSpec change.
`package_check.py` builds and installs both distributions and tests their real
console entry points and API examples. The last two commands independently
verify vectors with OpenSSL and reproduce setup/tests in a disposable source
copy, including intentional mutations of canonical bytes, array order, and
prefix length. The mutation failures are expected regression evidence.

For the issue worker's additional execution-boundary checks, use Linux with
Docker and OpenCode 1.19.4 installed on `PATH`:

```sh
python3 scripts/worker_sandbox.py build
python3 scripts/worker_runtime_check.py
```

These checks need no GitHub/OpenAI credentials and make no model requests.
They verify isolation, the real OpenCode/MCP connection, and offline integrated
and packaged CLI checks. For rootless Podman, add `--runtime podman` to both
commands. See [worker setup and operation](docs/issue-worker.md).

The standard `scripts/check.py` command also includes the credential-free
independent-reviewer checks. To run those alone:

```sh
python3 -m unittest discover -s scripts -p test_independent_review.py
```

See [reviewer setup and check attribution](docs/independent-review.md).

## Simple usage

Run setup above first. Packages are not yet published, so these examples use the
local TypeScript workspace and editable Python installation.

### Hash JSON from stdin (CLI)

TypeScript / Node.js:

```sh
printf '%s\n' '{"b":2,"a":1}' | node packages/typescript/dist/cli.js --prefix-length 24
```

Python:

```sh
printf '%s\n' '{"b":2,"a":1}' | .venv/bin/python -m rootprint --prefix-length 24
```

Each command writes one JSON hash record to stdout. Its `digest` is the full
SHA-256 Merkle root:
`d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`.
`--prefix-length 24` shortens only the display label's digest prefix, never the
full `digest`. The CLI uses the current UTC clock, so `calculatedAt` and the
label's timestamp vary with calculation time; they do not affect the root.

Both CLIs also accept a JSON file. After installing either built distribution,
the command is `rootprint [--prefix-length N] [FILE|-]` (stdin by default).

### Secondary examples: library APIs

#### TypeScript / Node.js

```sh
node --input-type=module -e '
import { hash, hashJson } from "rootprint";
const record = hash({ b: 2, a: 1 }, {
  clock: () => new Date("2026-11-02T09:04:05.987Z"),
});
console.log(record);
if (hashJson("{\"a\":1,\"b\":2}").digest !== record.digest) throw Error("digest mismatch");
'
```

#### Python

```sh
.venv/bin/python -c '
from datetime import datetime, timezone
from rootprint import hash_value, hash_json
record = hash_value({"b": 2, "a": 1}, clock=lambda: datetime(
    2026, 11, 2, 9, 4, 5, 987000, tzinfo=timezone.utc))
print(record)
assert hash_json("{\"a\":1,\"b\":2}")["digest"] == record["digest"]
'
```

Both API examples use a fixed clock and produce full SHA-256 digest
`d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`
and label `20261102_090405-sha256-v1-d331f806a7ada530`.

More API and custom-provider examples:
[TypeScript](packages/typescript/README.md), [Python](packages/python/README.md).

## Protocol, versions, and status

`v1` identifies the hashing protocol `rootprint-v1`, not the package release,
application schema, or future transfer format. Algorithm identifiers identify the
complete hash configuration. Label-only, package, and transfer-only changes do
not change full content identity. The owner-approved pre-publication protocol
rename does change prior local digests; recalculate them.

Each call currently recalculates all nodes and returns the root record; no tree
store or incremental-update API is implemented. Persistent tree storage needs a
separate change before synchronization. The [manifest-first synchronization
note](docs/synchronization.md) is a proposed design, not an active feature.

See [protocol](docs/protocol.md), [verification](docs/verification.md), and
[local work ledger](docs/local-work.md). The project is under initial
implementation; no packages have been published. Publication awaits registry
setup and verified release automation.

## AI-driven development

OpenSpec defines behavior; AI agents author implementation and maintenance.
Read [AGENTS.md](AGENTS.md). Locally, agent work is interactive and checks run on
this host. Hosted cross-platform CI, separate-App independent review and
no-bypass merge gates have recorded acceptance evidence. The issue worker has
completed a documentation issue-to-PR-to-manual-merge run; broader worker
acceptance, automatic merging and publishing remain incomplete.

Run `python scripts/activation.py` for outstanding requirements. The
[issue worker](docs/issue-worker.md) is implemented for owner-selected issues and
manual merging, with OpenAI GPT-6.1 Sol and isolated code execution. Its workflow
is disabled by default for new deployments. The [independent reviewer](docs/independent-review.md)
is implemented with a separate
App and tool-free model requests. The activation report links dated hosted
evidence and remaining requirements; it does not probe live service health.
Automatic merging and releases remain separate integrations. See
[automation activation](docs/automation.md).

Bounded repairs to an existing worker PR are implemented locally, pending hosted
deployment/acceptance. They share the issue's three-attempt budget, require fresh
CI/review after each commit, and stop at your manual rebase-merge decision.

## License

Rootprint is licensed under the [Eclipse Public License 2.0](LICENSE)
(`EPL-2.0`). Both language packages include the license text and source code.
