# Spec Delta

## ADDED Requirements

### Requirement: Visual review of changed PNG assets
Independent review SHALL supply supported changed static PNG files to the model as image input associated with their repository path, Git blob SHA, and head or baseline role. Additions SHALL include the head image, deletions the baseline image, and modifications or renames the applicable before/after images. The reviewer SHALL NOT approve a PNG merely by omitting its content.

#### Scenario: Review a new logo and README reference
- **WHEN** a PR adds the owner's valid 425,335-byte Rootprint PNG and references it from the README
- **THEN** the model receives the head image and its exact path/blob identity alongside the textual change context
- **AND** its structured review still determines whether independent-review passes

#### Scenario: Review modified or removed images
- **WHEN** a supported PNG is modified, renamed, or deleted
- **THEN** the model receives the applicable baseline/head versions with distinct, unambiguous labels
- **AND** findings can reference the affected image path with line zero

### Requirement: Bounded PNG review input
PNG review SHALL allow at most 1 MiB per image version, four versions and 2 MiB decoded bytes per request. Each image SHALL have positive dimensions no greater than 4096 per side and 8,000,000 pixels. Text SHALL retain its existing 100,000-byte per-file and 600,000-byte serialized-context limits, accounted separately from image payloads. Exceeded limits SHALL block review without silently dropping images.

#### Scenario: Include an image larger than the text limit
- **WHEN** a valid PNG is larger than 100,000 bytes but within all PNG limits
- **THEN** the image is processed under the PNG budget without increasing the text budget

#### Scenario: Reject an over-budget image set
- **WHEN** any per-image, dimension, pixel, count, or aggregate image limit is exceeded
- **THEN** independent-review fails before a model request and no image is silently omitted

### Requirement: PNG validation without privileged raster execution
Supported PNGs SHALL be regular Git blobs with a case-insensitive .png suffix, PNG signature, valid bounded chunk framing and CRCs, a valid IHDR, image data, and terminal IEND. Animated PNGs, malformed or truncated PNGs, symlinks, submodules, and other changed binary formats SHALL fail closed. PR images SHALL NOT be executed, imported, raster-decoded, or extracted onto the privileged host filesystem.

#### Scenario: Reject a disguised or malformed asset
- **WHEN** a changed .png contains non-PNG data, bad chunk bounds/CRC, invalid dimensions, animation, or missing terminal structure
- **THEN** independent-review fails before any model request

#### Scenario: Keep other binaries unsupported
- **WHEN** a PR changes a JPEG, executable, or other unsupported binary
- **THEN** PNG support does not bypass its existing rejection

### Requirement: Preserve image review isolation and freshness
PNG model input SHALL use inline image data from immutable Git blobs, not PR-provided external URLs. The model SHALL have no tools or prior implementation conversation. Image content and labels SHALL be untrusted task data. Separate reviewer App identity, credential-file exclusion, complete structured assessments, current head/base validation, final metadata freshness, and independent required checks SHALL remain mandatory.

#### Scenario: Instructions embedded in a logo
- **WHEN** a PNG contains apparent instructions to disclose credentials, execute code, or approve the PR
- **THEN** image input grants no tools or access to App credentials and cannot override the trusted review policy

#### Scenario: A commit changes an image during review
- **WHEN** the PR head or other material review metadata changes before the result is published
- **THEN** the result is blocked as stale and cannot approve the new head
