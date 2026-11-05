# Design

## Context

See proposal.md for the confirmed scope. The root README already displays
Rootprint, while package metadata, Python's source directory, imports, CLI names,
protocol constants, the independent vector oracle, and bootstrap's change path
retain the retired name. No packages or main specifications are published.

The worktree also contains unverified versioned-label implementation work and
shared record fixtures. Bootstrap label planning has been reconciled and the
permanent README requirement has been recorded in AGENTS.md and bootstrap's
maintenance specification. Preserve that work and finish it under the new name.

## Goals / Non-Goals

**Goals:** One consistent name across maintained files and paths; explicit new
protocol bytes; independent fixture evidence; runnable README examples and all
test commands; accurate unfinished automation and synchronization status.

**Non-Goals:** Compatibility shims, rewriting Git history, claiming registry-name
ownership, publishing, activating GitHub automation, implementing transfer APIs,
or renaming unrelated external tools or dependencies.

## Decisions

### Rename maintained surfaces together

Use `rootprint` for npm/Python distribution names, the Python import package, CLI
commands, diagnostic prefixes, temporary-directory prefixes, and workspace name;
use `Rootprint` for headings. Move the Python package directory and bootstrap
change directory to the corresponding new paths and update every caller/link.
Regenerate the npm lockfile using npm, then reinstall editable Python metadata
and build both packages. Do not retain legacy aliases: nothing is published and
the owner requested the complete rename.

The acceptance scan covers maintained text and tracked paths, including hidden
project configuration. Git's internal history and disposable dependency/build
environments are not maintained source; refresh generated metadata as necessary
rather than rewriting caches or history. The checkout's host directory is not a
portable repository path and must not leak into documentation or package data.

### Treat the protocol rename as a new pre-publication baseline

Both implementations use `rootprint-v1` for every scalar/container tag. Keep
canonicalization, ordered arrays, UTF-16 key order, provider configuration,
validation, UTC metadata, and prefix rules unchanged. Derive label token `v1`
from the renamed protocol constant, not a package version or duplicated literal.

Replace protocol literals in the independent reference oracle first, compute
literal SHA-256 expectations using its hashlib/OpenSSL cross-check, and commit
those reviewed expectations to the shared vectors. Recompute container children,
not just root tags. Independently sum the custom-provider preimages and update
the shared SHA-256/sum8 record fixtures. Never regenerate expectations using
either implementation under test. No extra vector generation framework is needed.

### Reconcile the active plans before applying code

Update bootstrap and `version-hash-labels` naming and their claims about immutable
bytes: label formatting alone preserves the renamed protocol bytes, but this
owner-approved protocol rename intentionally changes the previous unpublished
hashes. Preserve unrelated task state; revisit label-task evidence after the
rename. Their planning dependencies remain explicit until main specs exist.

Bootstrap must establish the baseline main capabilities before modifying deltas
are archived. The later label and rename changes must be reconciled to the same
`rootprint-v1` baseline so archive ordering cannot restore an obsolete identity.
Do not archive bootstrap while its remote acceptance tasks remain incomplete.

### Keep documentation executable and status accurate

The primary README includes simple examples for TypeScript and Python using
local packages, plus a single copy-and-paste setup/all-tests block covering the
integrated checker, installed packages, independent oracle, and clean-source
mutation reproduction. Include Windows interpreter instructions. Execute the
examples and commands rather than relying on prose inspection alone.

Finish the protocol version-domain discussion and proposed manifest-first
synchronization note from the existing label plan. Recomputed example digests
must agree with the renamed shared records. No synchronization API is active.

## Risks / Trade-offs

- Mechanical replacement can leave stale imports or distribution paths → Check
  installed artifacts and both console entry points, plus a case-insensitive
  maintained-reference/path scan.
- Hash fixtures can agree with a shared implementation mistake → Use literal
  framing and OpenSSL via the independent oracle, including custom-provider sums.
- A new test changes mutation-test numbering → Replace fragile ordinal assertions
  with stable test names where necessary and rerun all intentional mutations.
- Overlapping changes could restore old protocol bytes at archive → Reconcile
  plans before code, preserve dependencies, and validate all active changes.
- Existing local roots differ from renamed ones → State the pre-publication
  incompatibility in the ledger; never silently label old bytes as the new protocol.

## Migration Plan

Apply the rename to both ports, fixtures, callers, docs, and planning artifacts
together. Reinstall local package metadata, run integrated and installed-package
checks, verify independent vectors and clean-source mutations, and inspect the
maintained-reference scan. Record only checks that actually pass.

Existing local consumers must update imports/commands and recalculate roots;
there is no published-data migration or legacy emitter. Roll back the complete
rename together if needed, never a partial tag-only or fixture-only rollback.
Remote merge still requires independent automated review and current-head checks.
