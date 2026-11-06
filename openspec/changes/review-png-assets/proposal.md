# Proposal

## Why

The owner wants the supplied Rootprint logo and a short name explanation to form
the first approval-path test PR. The current reviewer rejects its 425,335-byte
PNG because all changed files must be UTF-8 text below 100,000 bytes.

## What Changes

- Review bounded static PNG assets as actual image input, alongside source and
  specifications, instead of rejecting them as text or approving them unseen.
- Include identifiable before/after image versions for additions, modifications,
  renames, and deletions without decoding raster data or executing PR content on
  the privileged host.
- Keep text limits, credential-file exclusions, other unsupported-binary
  rejection, separate App identity, exact-head checks, and fail-closed behavior.
- Add targeted image-input checks and document the PNG limits and controlled
  logo-PR activation sequence.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `automated-maintenance`: extend independent review to bounded static PNG input.
  This capability currently lives in the bootstrap delta because main specs have
  not been synchronized. Bootstrap remains the baseline and must be archived or
  synchronized before archiving this additive delta.

## Impact

Touches `scripts/independent_review.py`, its existing acceptance checks,
`automation/reviewer-policy.md`, and reviewer/setup documentation. Uses the
existing OpenAI Responses API image-input feature and Python standard library;
no new dependency, App permission, or hashing-protocol change is needed.

The owner explicitly performs **all pushes**; agents must not push. Work stays on
local `feat/png-review`, separate from the prepared `docs/readme-logo` branch.
This proposal does not activate automation, change remote settings, or claim a
hosted review. Implementation is a subsequent apply phase.
