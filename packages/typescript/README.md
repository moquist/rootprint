# Rootprint for TypeScript

Node.js 22+. SHA-256 is built in; every Merkle node uses RFC 8785 canonical bytes.

```js
import { hash, hashJson, digest } from "rootprint";

const record = hash({ b: 2, a: 1 });
console.log(record.label);   // UTC calculation label with a 16-hex prefix
console.log(record.digest);  // full deterministic root digest
console.log(hashJson('{"a":1,"b":2}').digest === record.digest); // true
console.log(digest({ a: 1, b: 2 }) === record.digest); // true
```

Custom provider:

```js
import { createHash } from "node:crypto";
import { hash } from "rootprint";

const provider = {
  algorithm: "sha512",
  digestLength: 64,
  hash: bytes => createHash("sha512").update(bytes).digest(),
};
console.log(hash([1, 2], { provider, prefixLength: 24 }));
```

`hash`/`hashJson` accept `clock: () => Date` for reproducibility. `digest` returns
only the full root hex. `parseJson` detects duplicate keys; plain `JSON.parse`
cannot recover duplicates already discarded. Invalid input raises `InputError`;
invalid providers raise `AlgorithmError`.

Labels use `YYYYMMDD_HHMMSS-<algorithm>-v1-<digest-prefix>`: for `{b:2,a:1}`
at `2026-11-02T09:04:05.987Z`, `20261102_090405-sha256-v1-d331f806a7ada530`.
The `v1` token identifies `rootprint-v1`, independently of package/transfer versions.
Label formatting alone never changes full digests or preimages. The pre-publication
protocol rename intentionally changes prior local roots; recalculate them.

CLI after installation: `rootprint [--prefix-length N] [FILE|-]`. Defaults to
stdin/SHA-256 and emits one JSON record. In the repository:
`node packages/typescript/dist/cli.js data.json`.

Numbers are finite binary64 (large integers can round), arrays are ordered,
objects sort by UTF-16 keys, and strings are not normalized. Input nesting is
limited to 256 container edges. Only plain objects and dense arrays with ordinary
enumerable data properties are supported. Full identity is protocol + algorithm
+ full digest. Labels may collide and are never identity or authenticated time.
Licensed under the Eclipse Public License 2.0 (`EPL-2.0`); see `LICENSE`.
Source code is included in the package's `src/` directory under the same license.
Package publication is pending.
