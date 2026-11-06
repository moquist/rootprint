# Spec Delta

## ADDED Requirements

### Requirement: Image content excluded from independent review
Independent review SHALL exclude regular image blobs from model content without fetching, parsing, validating, or rendering their bytes. It SHALL identify excluded paths and retain changed path/mode metadata. It SHALL NOT block solely on image exclusion or require visual acceptance evidence. Surrounding text SHALL remain subject to review.

#### Scenario: Identify excluded image assets
- **WHEN** a regular blob has a case-insensitive .png, .jpg, .jpeg, .gif, .webp, .svg, .ico, .bmp, .tif, .tiff, .avif, or .apng suffix
- **THEN** its content is excluded, including unchanged assets and text-based SVGs

#### Scenario: Add a README logo
- **WHEN** a PR adds an image and references it from README text
- **THEN** review includes the README text and changed image path but no image bytes
- **AND** image size, malformed image bytes, or lack of visual inspection do not block review

#### Scenario: Modify, rename, or delete images
- **WHEN** a PR modifies, renames, or deletes image assets, including an image-only PR
- **THEN** neither baseline nor head image bytes are fetched or sent to the model
- **AND** excluded paths and changed path/mode metadata remain available

### Requirement: Preserve review enforcement during image exclusion
Credential exclusions, unsupported object modes, non-image binary rejection, text limits, structured assessments, App identity, and revision freshness SHALL remain enforced when images are excluded.

#### Scenario: Preserve object and credential boundaries
- **WHEN** a changed image path is a symlink, submodule, or credential-file path
- **THEN** image exclusion does not bypass existing rejection
