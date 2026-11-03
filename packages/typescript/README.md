# Xmerkle for TypeScript

Node.js 22+. SHA-256 is built in; every Merkle node uses RFC 8785 canonical bytes.

```js
import { hash, hashJson, digest } from "xmerkle";

const record = hash({ b: 2, a: 1 });
console.log(record.label);   // UTC calculation label with a 16-hex prefix
console.log(record.digest);  // full deterministic root digest
console.log(hashJson('{"a":1,"b":2}').digest === record.digest); // true
console.log(digest({ a: 1, b: 2 }) === record.digest); // true
```

Custom provider:

```js
import { createHash } from "node:crypto";
import { hash } from "xmerkle";

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

CLI after installation: `xmerkle [--prefix-length N] [FILE|-]`. Defaults to
stdin/SHA-256 and emits one JSON record. In the repository:
`node packages/typescript/dist/cli.js data.json`.

Numbers are finite binary64 (large integers can round), arrays are ordered,
objects sort by UTF-16 keys, and strings are not normalized. Input nesting is
limited to 256 container edges. Only plain objects and dense arrays with ordinary
enumerable data properties are supported. Full identity is protocol + algorithm
+ full digest. Labels may collide and are never identity or authenticated time.
Package publication and a project license are pending.
