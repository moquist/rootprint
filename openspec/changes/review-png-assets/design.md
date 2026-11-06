# Design

## Context

See `proposal.md` for motivation. `context()` currently decodes every changed blob
as UTF-8 and applies `MAX_FILE=100000`. `ask_model()` sends one JSON text string.
Findings are validated against text-file paths. The current text/credential,
check-history, App-role, and SHA-freshness guards already work and must be reused.

The actual logo is committed on `docs/readme-logo` (`c6f7adc`); it is 425,335 bytes
and renders at 1005 by 419 pixels. This support branch starts at `2c28616` and
does not include the logo/README change. Main specs are absent, so bootstrap's
`automated-maintenance` delta is the baseline; archive it before this additive
delta rather than creating a competing maintenance capability.

## Goals / Non-Goals

**Goals:** make the actual asset reviewable as image data, preserve bounded
resource use and traceable before/after versions, and retain every existing gate.

**Non-Goals:** JPEG/GIF/SVG support, animation, image editing/optimization, a local
raster decoder, a generic asset/plugin framework, and changes to hashing bytes.

## Decisions

### Bounded static PNG inspection with standard-library primitives

Reuse the immutable Git blob API and reject non-regular objects first. Fetch PNG
bytes under a separate 1 MiB ceiling; validate actual length as well as API size.
Use PNG signature, bounded chunk framing, `struct`, and `zlib.crc32` for IHDR,
dimensions, chunk integrity, IDAT presence, and terminal IEND checks. Reject APNG
animation chunks. Do not decompress/rasterize, import, execute, or write the
image on the host. The provider handles rendering; decode/provider errors remain
blocking. Adding Pillow or a home-grown raster decoder is unnecessary.

The initial limits are 4096 pixels per side, 8,000,000 pixels, four attached image
versions, and 2 MiB aggregate decoded bytes. Count baseline/head attachments
against those budgets. Unsupported or over-limit versions fail the whole review,
not an incomplete approximation. Existing text budgets remain unchanged.

### Explicit image versions alongside textual context

Represent each relevant PNG version with path, blob SHA, head/baseline role,
mode, dimensions, size, and its inline base64 data. Keep base64 outside the
600,000-byte text-context accounting and log/summary output. Include head images
for additions, baseline images for deletions, and both sides for modifications
or renames. Preserve identifiers even when the bytes are identical. Unchanged
unneeded PNGs can remain in the existing omitted-path list.

Build one Responses API user message containing `input_text` for the JSON context
and labeled `input_image` blocks with `data:image/png;base64,...` URLs. Do not use
PR-provided network URLs. Preserve `store=false`, no tools, no prior conversation,
strict structured review, and final metadata equality. PNG findings use an
explicit allowed-image path set and line zero; do not pretend pixels are lines.

### Preserve reviewer enforcement and owner control

Extend the existing acceptance checks with generated small static PNG fixtures,
fake transports, and the supplied-logo bytes obtained from the existing local
logo branch. Check actual API image blocks and identity labels, not only a list
of filenames. Existing malformed-output, App-scoping, stale-head, credential-file,
and binary-rejection checks must continue passing.

The owner's instruction is explicit: **agents must not push; the owner performs
all pushes**. Record this durably in `AGENTS.md`/operations docs during apply.
Agents can prepare local branches, verified commits, and commands. Remote branch
rules and workflow activation remain owner-run account operations. Required CI
and reviewer-App checks are not weakened to get the logo through review.

## Risks / Trade-offs

- PNG headers can hide very large raster dimensions → validate byte/dimension/
  pixel limits without host decompression and reject unsupported animation.
- Image input adds provider cost → separate count/byte budgets and existing
  timeout/output/retry limits bound each request.
- Image text can contain prompt injection → treat visual content and labels as
  untrusted task data; preserve tool-free requests and strict output validation.
- The provider may reject an image or lack image entitlement → fail the check and
  record the hosted blocker, without approving an unseen asset.

## Migration Plan

Implement and verify on local `feat/png-review` in a subsequent apply phase. The
owner pushes the support change and deploys it through normal CI/review gates.
Refresh the logo branch against that updated base before its controlled PR.
Confirm visual input and exact-head reviewer attribution on GitHub; keep hosted
acceptance tasks open until evidence exists. Roll back by reverting PNG support
through normal gates, restoring fail-closed binary behavior. No remote action,
automatic merge, or bypass permission is part of this change.
