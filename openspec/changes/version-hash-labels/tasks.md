# Tasks

## 1. Versioned hash records in both ports

- [x] 1.1 Reconcile bootstrap's overlapping UTC-label requirement and proposal/design examples with this change, preserving unrelated incomplete tasks and documenting the baseline/archive dependency; verify both changes pass strict OpenSpec validation and describe the same generated label format.
- [x] 1.2 Add shared fixed-clock record expectations for SHA-256 and the existing `sum8` provider, derive the `v1` label token from `rootprint-v1` in both record constructors, and update each package's API documentation; verify both conformance suites pass exact-label, timezone, prefix, and collision checks while label formatting alone preserves the renamed protocol's digest/preimage vectors.
- [x] 1.3 Update the common CLI/integration expectations for `-<algorithm>-v1-<prefix>`; verify cross-language fixed-clock records and both installed `rootprint` console entry points through `scripts/test_integration.py` and `scripts/package_check.py`.

## 2. Protocol and synchronization documentation

- [x] 2.1 Update README and `docs/protocol.md` with versioned label examples and separate algorithm, hashing-protocol, package-release, and transfer-format identities; verify examples match the shared fixed-clock expectations and the documentation preserves `rootprint-v1` identity and bytes under label-only changes.
- [x] 2.2 Write `docs/synchronization.md` describing ordered chunk manifests, batched missing-chunk requests, whole-document cost fallback, independent transfer versioning, and final root verification; update the local ledger and link the design note from README. Verify the document explicitly marks synchronization as proposed, accounts for metadata/round-trip costs, and identifies the concrete chunking/wire/budget decisions required by a later implementation change.

## 3. Integrated acceptance

- [x] 3.1 Run `.venv/bin/python scripts/check.py`, `.venv/bin/python scripts/package_check.py`, and strict validation for all active changes; verify both ports and packaged CLIs generate the new label shape, label formatting alone preserves all renamed-protocol digest/preimage expectations, no synchronization feature is falsely reported active, and verified changes are committed.

## Workflow follow-up

- Preserve the archive dependency: bootstrap supplies the main `hash-records` capability before this modifying change is archived and synchronized.
- After implementation and the applicable review requirements are satisfied, archive through the OpenSpec workflow and verify the resulting main requirements retain the versioned label and independent identities.
- Specify concrete synchronization/chunking parameters and acceptance measurements in a separate implementation proposal before building transfer APIs.
