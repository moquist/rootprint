# Spec Delta

## MODIFIED Requirements

### Requirement: UTC calculation label
Labels SHALL use `YYYYMMDD_HHMMSS-<hash-algorithm>-<protocol-version>-<shortened-hash>`. The timestamp SHALL be UTC root-calculation completion time truncated to seconds; `calculatedAt` SHALL represent it as `YYYY-MM-DDTHH:MM:SSZ`. Years SHALL be 0001–9999. An injectable clock SHALL support reproducible checks. Protocol `rootprint-v1` SHALL use the label token `v1`.

#### Scenario: Format a known instant
- **WHEN** SHA-256 calculation completes at `2026-11-02T09:04:05.987Z` with a digest starting `0123456789abcdef`
- **THEN** its default label is `20261102_090405-sha256-v1-0123456789abcdef` and calculatedAt is `2026-11-02T09:04:05Z`

#### Scenario: Local timezone differs
- **WHEN** calculations complete at the same instant in hosts with different local timezones
- **THEN** their timestamp fields are identical

#### Scenario: Caller supplies another hash algorithm
- **WHEN** a conforming custom provider named `sum8` calculates a root under `rootprint-v1`
- **THEN** its label contains `-sum8-v1-`, identifying the provider independently of the hashing protocol

## ADDED Requirements

### Requirement: Label version identifies the hashing protocol
The label version SHALL identify the record's hashing protocol, not its package version, application schema, or transfer format. Versioned-label generation SHALL preserve all `rootprint-v1` node preimages and full digests. Documentation SHALL distinguish root-affecting hashing changes from independently versioned transfer optimizations.

#### Scenario: Add protocol visibility without changing identity
- **WHEN** existing conformance inputs are recalculated with versioned labels and the same providers
- **THEN** their protocol, algorithm, full digest, and canonical node preimages match the existing vectors, while labels include `v1`

#### Scenario: Change a package release or transfer strategy
- **WHEN** a package release or proposed synchronization strategy changes without changing the hashing protocol or provider
- **THEN** the documented identity remains protocol plus algorithm plus full digest, and the label version remains `v1` for `rootprint-v1`
