# Tasks

## 1. Consistent planning and public names

- [x] 1.1 Reconcile bootstrap and version-hash-labels artifacts to the approved Rootprint protocol baseline, rename bootstrap's change path, and retain unrelated incomplete tasks and archive dependencies; verify all active changes with strict OpenSpec validation and inspect their identity/byte-preservation clauses for consistency.
- [x] 1.2 Rename package metadata, Python source package, imports, CLI commands/diagnostics, workspace/lockfile entries, and maintained documentation/configuration references; reinstall local package metadata and verify both builds and language suites use the renamed package and rootprint-v1 identity.

## 2. Renamed protocol evidence and documentation

- [x] 2.1 Recompute shared literal preimages, full SHA-256 digests, custom-provider preimages/digests, and fixed-clock records independently of both implementations; verify the OpenSSL reference check, exact-label/provider checks, timezone/prefix/collision tests, and both language suites.
- [x] 2.2 Update root and package README examples, protocol/version-domain documentation, and the proposed synchronization note; execute each primary README usage example and its complete copy-and-paste setup/test commands, covering both implementations, cross-language integration, installed CLIs, independent vectors, and clean-source mutations.

## 3. Integrated acceptance

- [x] 3.1 Update package/integration and mutation checks for renamed imports/distributions/entry points and stable regression-test names; run `.venv/bin/python scripts/check.py`, `.venv/bin/python scripts/package_check.py`, `.venv/bin/python scripts/vector_reference.py --check`, and `.venv/bin/python scripts/clean_check.py --mutations` successfully.
- [x] 3.2 Inspect the complete diff and case-insensitively scan maintained content and tracked paths for retired-name references; verify strict validation for all active changes and record the approved protocol incompatibility, actual verification evidence, pending commit/archive requirements, and inactive remote/synchronization status in the local ledger.

## Workflow follow-up

- Complete the in-progress versioned-label tasks against the renamed protocol baseline, marking only verified work complete.
- Always commit verified changes under the owner's standing local-commit authorization; obtain independent automated review before any remote merge.
- Bootstrap must supply the main capabilities before dependent changes are archived. Reconcile archive ordering, use the OpenSpec archive workflow, and verify main specs; preserve bootstrap's incomplete remote activation tasks.
- Specify persistent tree storage and concrete synchronization/chunking parameters in separate changes before implementing transfer APIs.
