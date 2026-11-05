# Spec Delta

## MODIFIED Requirements

### Requirement: Recursive Merkle encoding
Protocol `rootprint-v1` SHALL hash each node as UTF-8 RFC 8785 encoding of its tagged representation. Scalars use `["rootprint-v1","value",value]`; arrays use `["rootprint-v1","array",childDigests]`; objects use `["rootprint-v1","object",sortedPairs]`. Child digests SHALL be full lowercase hex strings, and each sorted pair SHALL be `[key,childDigest]`.

#### Scenario: Nested data hashes recursively
- **WHEN** an object contains an array of scalar and object values
- **THEN** each child digest is computed first and included in its parent's representation according to this encoding

#### Scenario: Types and empty containers remain distinct
- **WHEN** inputs are `null`, `false`, `0`, `"0"`, `[]`, or `{}`
- **THEN** their node preimages are distinct and match the shared protocol vectors

#### Scenario: Rename the unpublished protocol
- **WHEN** either implementation calculates a root after the rename
- **THEN** every node uses the `rootprint-v1` tag and the result matches independently recomputed expectations for those bytes

## ADDED Requirements

### Requirement: Rootprint public naming
Both language distributions SHALL be named `rootprint`. The Python import module and both installed CLI commands SHALL be `rootprint`. Maintained repository text and paths SHALL use `rootprint` or the display name `Rootprint`, replacing the retired name without compatibility aliases. Existing Git history SHALL NOT be rewritten.

#### Scenario: Install and use either implementation
- **WHEN** a user installs either built distribution
- **THEN** the documented `rootprint` import and CLI work and the CLI emits the same full identity as its library API

#### Scenario: Inspect maintained project references
- **WHEN** tracked source, configuration, documentation, tests, fixtures, and active change paths are inspected after implementation
- **THEN** they contain no retired project-name references, including case variants
