# Xmerkle

Deterministic, versioned Merkle hashing for JSON, with bring-your-own hash
functions. Initial implementations: **TypeScript and Python**. Rust is planned
after these implementations pass the same conformance vectors.

- Objects sort by RFC 8785 UTF-16 key order; arrays preserve order.
- Numbers use finite IEEE-754 binary64 semantics (not exact arbitrary precision).
- SHA-256 is the default; libraries accept custom fixed-output hash providers.
- Full digests identify content. UTC labels aid recognition:
  `20261102_090405-sha256-0123456789abcdef`.

## Local development

Requires Node.js 22+ and Python 3.11+. OpenSpec 1.16.0 is pinned locally.

```sh
npm ci
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check.py
```

On Windows use `.venv\Scripts\python.exe` instead of `.venv/bin/python`.
The checker uses its own Python interpreter for Python package checks.

See [protocol](docs/protocol.md), [verification](docs/verification.md), and
[local work ledger](docs/local-work.md). The project is under initial
implementation; no packages have been published. A license has not yet been
selected, so publication is not enabled.

## AI-driven development

OpenSpec defines behavior; AI agents author implementation and maintenance.
Read [AGENTS.md](AGENTS.md). Locally, agent work is interactive and checks run on
this host. GitHub issue events, hosted multi-OS checks, independent PR review,
automatic merging, and publishing are **not active** until remote setup is
completed. Local development does not weaken those intended merge gates, but
cannot demonstrate them or provide unattended GitHub maintenance.

Run `python scripts/activation.py` for outstanding requirements. See
[automation activation](docs/automation.md): pushing enables CI, but the remaining
agent/reviewer/merge/release integrations still need implementation and live
verification.
