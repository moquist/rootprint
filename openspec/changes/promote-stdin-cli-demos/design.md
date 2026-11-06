# Design

## Context

The primary README currently places multi-line inline API programs first under
`Simple usage`, with two stdin pipelines only after those programs. Setup already
builds the TypeScript workspace and installs editable Python. The existing local
commands are `node packages/typescript/dist/cli.js` and
`.venv/bin/python -m rootprint`. Installed distributions expose `rootprint`.
Both entry points read strict UTF-8 JSON, call their library's JSON hashing API,
and serialize one hash record, including the full SHA-256 digest. Errors go to
stderr with a nonzero exit code. Source and installed tests share `cli_checks`.

Applicable contracts are bootstrap's `automated-maintenance` (README usage and
all-tests), `json-merkle` (command-line hashing), and `hash-records` (full digest
versus label), plus `version-hash-labels`' metadata clarification. No runtime
contract needs to change.

## Goals / Non-Goals

Goals: make stdin hashing the first usage demo for each existing implementation;
make the full root easy to identify; keep direct library examples available lower
in the README and preserve runnable setup/test instructions.

Non-goals: a new executable, bare-digest stdout, flags or output schema changes,
CLI installation/publishing changes, new ports, or any hashing-byte changes.

## Decisions

### Reorder and clarify existing examples, not the CLI

Within `Simple usage`, show both existing stdin pipeline commands before any
inline API program. Use the existing repository-local invocations, since packages
are not published. Keep the current `--prefix-length 24` examples; explain that
this shortens only the display label, not `digest`. Keep installed-command and
file/stdin guidance nearby. Keep the existing setup section before usage rather
than introducing another setup procedure.

Describe stdout as a JSON record and identify `digest` as the full root. For
`{"b":2,"a":1}`, the full SHA-256 digest is
`d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`.
Do not imply CLI timestamps or labels are fixed. Keep the fixed-clock label
explanation attached to the secondary API examples, not the live CLI examples.
No extraction program or new digest-only mode is necessary.

### Retain secondary API examples and platform setup

Move the existing Node and Python inline programs intact under an explicitly
secondary library/API heading after the CLI examples. Retain package README
links and the fixed-clock digest/label expectations. Preserve Linux/macOS and
PowerShell setup/all-tests blocks and their cross-language/packaged-test scope.
Usage commands remain the existing POSIX shell demos; this change does not claim
new Windows/macOS execution evidence.

## Verification

During implementation, inspect README order and run both exact primary stdin
pipelines after documented setup. Parse their stdout as JSON and assert protocol
`rootprint-v1`, algorithm `sha256`, the full expected digest, and a 24-character
label suffix matching its prefix. Do not compare current timestamps or whole
records for equality. Execute both retained API examples and check their
fixed-clock digest/label output.

Run `python3 scripts/check.py`, `python3 scripts/package_check.py`, strict
OpenSpec validation, and `git diff --check` using the sandbox development
interpreter. Existing shared vectors/source CLI/installed CLI checks provide
runtime compatibility coverage; no new dependencies or runtime tests are needed
for a documentation-only reorder. Record exact commands and results in
`docs/local-work.md`. A final diff review must confirm setup/all-tests commands
remain current and no implementation or vector bytes changed.

## Risks / Rollback / Dependencies

Readers may confuse label prefixes with full roots or the API's fixed clock with
CLI time; the adjacent explanations address both risks. Rollback is a README
revert, with no data migration. Bootstrap remains incomplete and supplies the
baseline capability: do not archive it or this dependent delta prematurely.
No remote requests, pushes, publication, gate bypass, or automation activation
are part of this change. Latest-revision CI and independent automated review,
followed by owner merge, remain external completion gates.
