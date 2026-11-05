# Proposal

## Why

Rootprint records already identify the hashing protocol, but their human-readable labels omit it. Exposing that version makes the encoding contract recognizable independently of the hash function and leaves room for efficient synchronization without confusing transport changes with changes to content identity.

## What Changes

- **BREAKING**: Change generated labels to `YYYYMMDD_HHMMSS-<algorithm>-<protocol-version>-<digest-prefix>`, for example `20261102_090405-sha256-v1-0123456789abcdef`.
- Map the current `xmerkle-v1` record protocol to the label token `v1`; keep full root digests, canonical node preimages, timestamps, and shortening rules unchanged.
- Document separate version domains for hash functions/configurations, hashing protocols, package releases, and future synchronization formats.
- Record a manifest-first synchronization design: exchange a target identity and ordered chunk manifest, request missing chunks in a batch, transfer those chunks, reconstruct, and verify the target root. Prefer whole-document transfer when cheaper.
- Keep synchronization at the design/documentation stage in this change. Concrete chunk boundaries, wire encoding, resource budgets, and network APIs need a separately specified implementation change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `hash-records`: Include the hashing-protocol version in UTC display labels, independently of algorithm and package version.

## Impact

Both language record constructors, fixed-clock/custom-provider expectations, CLI integration checks, README examples, protocol documentation, and the local ledger are affected. No new dependency is needed. Existing content digests and shared digest vectors must remain unchanged; consumers parsing the previous label shape must adapt.

Dependency: `hash-records` is introduced by the still-active `bootstrap-xmerkle-ecosystem` change, not yet present in main specs. This delta uses that change's implemented contract as its baseline and supersedes its UTC label requirement when applied. Bootstrap's overlapping planning examples must be reconciled during apply; do not archive this modification before its baseline capability exists in main specs.
