# Spec Delta

## Purpose

Define interoperable Merkle identities for JSON values so independent language implementations agree on every hashed byte.

## ADDED Requirements

### Requirement: JSON input model
Libraries SHALL accept JSON values and strict JSON text using the RFC 8785 binary64 number model. They SHALL reject duplicate object keys in text, non-finite numbers, unpaired surrogates, cycles, and non-JSON values. Numeric precision beyond binary64 SHALL be documented as unsupported.

#### Scenario: Invalid input is rejected
- **WHEN** text contains duplicate keys, NaN, an overflowing number, or an unpaired surrogate, or a native value contains a cycle or unsupported type
- **THEN** hashing fails with an input error and no successful hash record is emitted

#### Scenario: Equivalent numeric representations
- **WHEN** valid inputs use `1`, `1.0`, and `1e0`, or use negative zero and zero
- **THEN** each equivalent pair has identical Merkle digests

### Requirement: Object canonical ordering
Objects SHALL be treated as key/value pairs sorted lexicographically by unsigned UTF-16 code units, as specified by RFC 8785. Sorting SHALL be locale-independent and SHALL NOT normalize Unicode strings.

#### Scenario: Object insertion order does not matter
- **WHEN** two objects have identical members in different insertion orders, including nested objects and non-BMP keys
- **THEN** their root digests are identical in every supported implementation

#### Scenario: Unicode spellings remain distinct
- **WHEN** keys or values use composed and decomposed Unicode spellings
- **THEN** their original code points are preserved in hashing rather than normalized

### Requirement: Recursive Merkle encoding
Protocol `rootprint-v1` SHALL hash each node as UTF-8 RFC 8785 encoding of its tagged representation. Scalars use `["rootprint-v1","value",value]`; arrays use `["rootprint-v1","array",childDigests]`; objects use `["rootprint-v1","object",sortedPairs]`. Child digests SHALL be full lowercase hex strings, and each sorted pair SHALL be `[key,childDigest]`.

#### Scenario: Nested data hashes recursively
- **WHEN** an object contains an array of scalar and object values
- **THEN** each child digest is computed first and included in its parent's representation according to this encoding

#### Scenario: Types and empty containers remain distinct
- **WHEN** inputs are `null`, `false`, `0`, `"0"`, `[]`, or `{}`
- **THEN** their node preimages are distinct and match the shared protocol vectors

### Requirement: Array ordering
Arrays SHALL preserve index order, including repeated elements. Only object members SHALL be sorted.

#### Scenario: Reordering an array changes its preimage
- **WHEN** an array's unequal elements are swapped
- **THEN** its ordered child digest list changes, whereas permuting object members does not change their sorted pair list

### Requirement: Caller-supplied hash algorithms
Libraries SHALL accept a caller-supplied algorithm identifier, positive digest byte length, and deterministic bytes-to-bytes hash function. SHA-256 with identifier `sha256` SHALL be built in. Identifiers SHALL match `[a-z0-9]+`, denote the complete algorithm configuration, and produce exactly the declared byte length; invalid provider output SHALL fail.

#### Scenario: Custom provider receives protocol bytes
- **WHEN** a caller selects a conforming custom provider
- **THEN** every node uses that provider on the specified bytes without substituting SHA-256 or truncating its output

#### Scenario: Broken provider output
- **WHEN** a provider returns a non-byte value, an empty digest, or a length different from its declaration
- **THEN** calculation fails with an algorithm error

### Requirement: Cross-language conformance
TypeScript and Python libraries SHALL produce identical full digests for shared vectors on Linux, macOS, and Windows. Vectors SHALL include canonical node preimages and expected digests independently checked against the protocol, rather than only comparing the implementations to each other.

#### Scenario: Shared vectors execute
- **WHEN** both implementations execute vectors covering numbers, Unicode ordering, nested and empty containers, rejection cases, and a custom provider
- **THEN** valid preimages and digests match the committed expectations and invalid inputs are rejected

### Requirement: Command-line hashing
Both language packages SHALL provide a CLI accepting strict UTF-8 JSON from a file or standard input. The default algorithm SHALL be SHA-256. Successful output SHALL be one JSON hash record; errors SHALL use standard error and a nonzero exit status without a successful record on standard output. BYO algorithms SHALL be supported through library APIs without executing plugins named by JSON input.

#### Scenario: Pipe a JSON document
- **WHEN** a user pipes valid JSON into either CLI with default options
- **THEN** it emits a record whose full root digest matches the corresponding library calculation
