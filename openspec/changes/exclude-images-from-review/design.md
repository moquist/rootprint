# Design

## Context

The approved plan supersedes the completed `review-png-assets` behavior. Main
specs remain absent; bootstrap and active deltas are the implementation contract.
The compact-JSON delta also currently requires image-label accounting.

## Goals / Non-Goals

Remove image-content review and validation. Keep text review, existing security
boundaries, exact-revision checks, and the README logo. No replacement image parser.

## Decisions

Use a small case-insensitive suffix allowlist: .png, .jpg, .jpeg, .gif, .webp,
.svg, .ico, .bmp, .tif, .tiff, .avif, and .apng. Skip regular image blobs in both
head and baseline before fetching bytes, including unchanged images. Report all
excluded paths in `omitted_image_paths`; retain changed path/mode metadata.
Image-only PRs still receive the ordinary structured review of metadata, issues,
and applicable contracts; lack of image content is not a blocking concern.

Credential-path rejection precedes exclusion. Image-named symlinks/submodules
remain unsupported; non-image binary changes remain blocking. SVG is excluded as
an image even though it is text. Suffix exclusion is deliberate, not a claim that
the bytes are valid images. Surrounding text and workflow changes remain reviewed.

Delete PNG parsing, image budgets, image data/labels and image-specific findings;
send one compact JSON text block. Retain generic immutable-blob size/encoding/mode
guards and test them with text files. Replace PNG fixture generation and visual
checks with exclusion checks across add/modify/rename/delete and transport.

Update active deltas in place to remove contradictory ongoing requirements while
retaining historical PNG implementation/hosted evidence as explicitly superseded.
Archive only after bootstrap synchronization; no hosted deployment is claimed.

## Risks / Trade-offs

Image bytes, including text in SVGs, intentionally receive no content review.
The exclusion list is explicit and bounded rather than heuristic MIME detection.
