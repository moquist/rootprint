# Verification

Install dependencies as shown in the root README. Run `python scripts/check.py`
using the Python environment containing `requirements-dev.txt`.

Individual checks:

```sh
npm run build
npm test
python -m unittest discover -s packages/python/tests
python -m ruff check packages/python scripts
npm exec -- openspec validate --all --strict
python -m build packages/python
npm pack --workspace packages/typescript --dry-run
python scripts/package_check.py
python scripts/vector_reference.py --check
python scripts/clean_check.py --mutations
```

Use Python 3.11+ and Node.js 22+. Shared vectors, fixed-clock records, malformed
input rejection, custom providers, and packaged CLIs form the acceptance suite.
Hosted Windows/macOS verification and named remote merge gates remain pending
until GitHub activation; passing local Linux checks does not prove those runs.

`package_check.py` builds and installs both distributions into temporary
environments, then exercises CLI trust boundaries and documented API examples.
`vector_reference.py --check` additionally needs OpenSSL to independently verify
the fixture preimages. `clean_check.py --mutations` reproduces installation and
checks without local dependencies or Git metadata, then confirms that changes to
canonical bytes, array order, and label shortening fail the expected tests in a
disposable copy; it never mutates the working source.

The prepared GitHub workflow runs both language suites and integration checks on
Ubuntu, macOS, and Windows with Node 22/Python 3.11, plus Ubuntu Node 24/Python
3.14. Required aggregate status: `ci`. Independent automated review will be
`independent-review` once implemented and verified; it is not currently active.
