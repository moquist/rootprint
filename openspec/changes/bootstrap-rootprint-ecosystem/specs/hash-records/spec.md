# Spec Delta

## Purpose

Represent hash calculations with recognizable UTC labels while preserving complete, deterministic Merkle identities for verification.

## ADDED Requirements

### Requirement: Complete hash record
A successful calculation SHALL return `protocol`, `algorithm`, `digest`, `calculatedAt`, and `label`. Protocol SHALL be `rootprint-v1`; digest SHALL be the full lowercase hexadecimal root digest. Deterministic identity SHALL consist of protocol, algorithm, and full digest, never the label alone.

#### Scenario: Same content calculated twice
- **WHEN** the same value and provider are used at two different times
- **THEN** protocol, algorithm, and full digest match while calculation metadata can differ

### Requirement: UTC calculation label
Labels SHALL use `YYYYMMDD_HHMMSS-<hash-algorithm>-<protocol-version>-<shortened-hash>`. The timestamp SHALL be the UTC root-calculation completion time truncated to seconds. `calculatedAt` SHALL represent the same instant as `YYYY-MM-DDTHH:MM:SSZ`. Years SHALL use four digits in the range 0001–9999. An injectable clock SHALL support reproducible checks. Protocol `rootprint-v1` SHALL use the label token `v1`.

#### Scenario: Format a known instant
- **WHEN** SHA-256 calculation completes at `2026-11-02T09:04:05.987Z` with a digest starting `0123456789abcdef`
- **THEN** its default label is `20261102_090405-sha256-v1-0123456789abcdef` and calculatedAt is `2026-11-02T09:04:05Z`

#### Scenario: Local timezone differs
- **WHEN** calculations complete at the same instant in hosts with different local timezones
- **THEN** their timestamp fields are identical

### Requirement: Explicit digest shortening
The shortened hash SHALL be the first 16 lowercase hex characters by default, or the complete digest if shorter. Callers SHALL be able to select an integer prefix length from 1 through the full digest's hex length. Invalid requested lengths SHALL fail rather than silently clamp. Full digests SHALL never be discarded or used in shortened form for verification.

#### Scenario: Custom prefix length
- **WHEN** a caller requests 24 characters for a 64-character digest
- **THEN** the label contains exactly its first 24 hex characters and the record retains all 64

#### Scenario: Invalid prefix length
- **WHEN** the requested length is zero, non-integral, or longer than the full hex digest
- **THEN** record creation fails with a validation error

### Requirement: Display labels are not unique identities
Timestamp and label fields SHALL be excluded from every Merkle preimage. Documentation SHALL state that label sorting orders reported UTC seconds, not guaranteed event order, and that clock skew, same-second calculations, and prefix collisions prevent labels from serving as unique identifiers or authenticated timestamps.

#### Scenario: Identical prefixes collide
- **WHEN** two different full digests share the chosen prefix and are calculated in the same UTC second with the same algorithm
- **THEN** their labels can match but their full deterministic identities remain distinct

#### Scenario: Chronological display order
- **WHEN** valid labels with different recorded UTC seconds are sorted lexicographically
- **THEN** their timestamp portions sort in recorded chronological order regardless of algorithm
