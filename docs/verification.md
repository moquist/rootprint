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
Hosted Windows/macOS verification and named remote merge gates have recorded
acceptance evidence in [the ledger](local-work.md); local Linux checks remain
separate from those hosted observations.

`package_check.py` builds and installs both distributions into temporary
environments, then exercises CLI trust boundaries and documented API examples.
`vector_reference.py --check` additionally needs OpenSSL to independently verify
the fixture preimages. `clean_check.py --mutations` reproduces installation and
checks without local dependencies or Git metadata, then confirms that changes to
canonical bytes, array order, and label shortening fail the expected tests in a
disposable copy; it never mutates the working source.

The GitHub workflow runs both language suites and integration checks on
Ubuntu, macOS, and Windows with Node 22/Python 3.11, plus Ubuntu Node 24/Python
3.14. Required aggregate status: `ci`. All four jobs passed on PR #14's published
head; the ledger records the exact SHA and run. The
[independent reviewer](independent-review.md) publishes `independent-review`
through its own App. Local checks cover review decisions and SHA freshness;
hosted evidence also records App attribution, new-head invalidation and failure
blocking. `python scripts/activation.py` links those historical observations and
reports remaining work without claiming current remote health or full autonomy.
