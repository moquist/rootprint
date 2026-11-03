# Proposal

## Why

JSON Merkle implementations need one precise wire protocol to produce identical hashes across languages and platforms. Xmerkle will establish that contract first and use OpenSpec-driven AI maintenance so routine development, issue handling, and fixes require no human-written code.

## What Changes

- Specify versioned, domain-separated Merkle hashing for JSON, using RFC 8785 scalar encoding, sorted object keys, and ordered arrays.
- Support caller-supplied deterministic hash algorithms, with SHA-256 available out of the box.
- Provide TypeScript and Python libraries plus command-line entry points and shared cross-platform conformance vectors.
- Represent calculations with a full digest and a human-readable UTC label, `YYYYMMDD_HHMMSS-<hash-algorithm>-<shortened-hash>`. Calculation timestamps and truncation do not affect Merkle identity.
- Establish GitHub/OpenCode issue triage, spec-driven agent implementation, independent checks, automatic merging, and auditable failure handling.
- Document setup, protocol, agent instructions, and release workflow; keep publishing behind successful automated verification.

## Capabilities

### New Capabilities

- `json-merkle`: Canonical JSON validation, versioned recursive hashing, algorithm injection, and interoperable libraries and CLI behavior.
- `hash-records`: Full hash identities and timestamped, shortened display labels.
- `automated-maintenance`: OpenSpec-driven AI issue processing, verification, merging, and release automation.

### Modified Capabilities

None; the repository has no existing specifications or implementation.

## Impact

Introduces a protocol document, shared vectors, TypeScript and Python packages, CLI entry points, root contributor/agent guidance, and GitHub workflows. Requires a GitHub repository, an OpenCode-compatible provider credential, and repository automation permissions during activation. No application dependencies or language toolchains are currently configured. Inclusion proofs, additional language ports, incremental persistence, and a hosted service are outside this first change.
