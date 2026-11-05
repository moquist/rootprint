import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { createHash } from "node:crypto";
import { AlgorithmError, InputError, digest, hash, hashJson, sha256 } from "../dist/index.js";

const vectors = JSON.parse(readFileSync(new URL("../../../conformance/v1/vectors.json", import.meta.url), "utf8"));
const clock = () => new Date("2026-11-02T09:04:05.987Z");

test("shared fixed-clock records include hashing protocol in labels", () => {
  const records = JSON.parse(readFileSync(new URL("../../../conformance/v1/records.json", import.meta.url), "utf8"));
  const providers = { sha256, sum8: { algorithm: "sum8", digestLength: 1,
    hash: bytes => Uint8Array.of(bytes.reduce((a, b) => a + b, 0) % 256) } };
  for (const { json, record } of records.cases) {
    assert.deepEqual(hashJson(json, { provider: providers[record.algorithm], clock: () => new Date(records.instant) }), record);
  }
});

test("shared canonical preimages and full digests", () => {
  for (const vector of vectors.valid) {
    let last;
    const provider = { ...sha256, hash(bytes) { last = Buffer.from(bytes).toString("utf8"); return sha256.hash(bytes); } };
    assert.equal(hashJson(vector.json, { provider, clock }).digest, vector.digest, vector.json);
    assert.equal(last, vector.preimage, vector.json);
  }
  for (const source of vectors.invalid) assert.throws(() => hashJson(source), InputError, source);
});

test("native invalid values, cycles, shared references and no mutation", () => {
  const cycle = {}; cycle.self = cycle;
  const accessor = Object.defineProperty({}, "x", { enumerable: true, get() { throw Error("must not invoke"); } });
  const extraArray = [1]; extraArray.x = 2;
  for (const value of [undefined, NaN, Infinity, 1n, new Date(), new Map(), () => 1, Symbol(),
    { x: undefined }, [undefined], Array(1), cycle, accessor, extraArray, { [Symbol()]: 1 }, "\ud800"]) {
    assert.throws(() => digest(value), InputError);
  }
  const child = Object.freeze({ b: 2, a: 1 });
  const value = Object.freeze([child, child]);
  assert.equal(digest(value), digest([{ a: 1, b: 2 }, { a: 1, b: 2 }]));
  assert.deepEqual(Object.keys(child), ["b", "a"]);
  let deep = null;
  for (let i = 0; i < 257; i++) deep = [deep];
  assert.throws(() => digest(deep), InputError);
  assert.equal(hashJson('{"__proto__":1}').digest, digest(JSON.parse('{"__proto__":1}')));
});

test("custom providers and invalid configurations", () => {
  const calls = [];
  const provider = { algorithm: "sum8", digestLength: 1, hash(bytes) {
    calls.push(Buffer.from(bytes).toString("utf8"));
    return Uint8Array.of(bytes.reduce((a, b) => a + b, 0) % 256);
  } };
  const record = hashJson(vectors.custom.json, { provider, clock });
  assert.equal(record.digest, vectors.custom.digest);
  assert.equal(record.label, "20261102_090405-sum8-v1-6f");
  assert.deepEqual(calls, vectors.custom.preimages);
  const sha512 = { algorithm: "sha512", digestLength: 64, hash: b => createHash("sha512").update(b).digest() };
  assert.equal(digest(null, sha512).length, 128);
  for (const broken of [{ ...provider, algorithm: "sha-256" }, { ...provider, algorithm: "sha256\n" }, { ...provider, digestLength: 0 },
    { ...provider, hash: () => "aa" }, { ...provider, hash: () => new Uint8Array() },
    { ...provider, hash: () => new Uint8Array(2) }, { ...provider, hash: () => { throw Error("failed"); } }]) {
    assert.throws(() => digest(null, broken), AlgorithmError);
  }
});

test("UTC labels, prefix bounds, collision metadata, and deterministic identity", () => {
  const fixed = { algorithm: "fixed", digestLength: 16, hash: () => Buffer.from("0123456789abcdef0123456789abcdef", "hex") };
  const record = hash(null, { provider: fixed, clock });
  assert.equal(record.label, "20261102_090405-fixed-v1-0123456789abcdef");
  assert.equal(record.calculatedAt, "2026-11-02T09:04:05Z");
  assert.equal(hash(null, { provider: fixed, clock, prefixLength: 24 }).label.split("-").at(-1).length, 24);
  assert.equal(hash(null, { clock }).digest, hash(null, { clock: () => new Date("2027-01-01Z") }).digest);
  for (const prefixLength of [0, -1, 1.5, 65, NaN, Infinity]) assert.throws(() => hash(null, { prefixLength }), InputError);
  for (const instant of [new Date(NaN), new Date("0000-01-01T00:00:00Z"), new Date("+010000-01-01T00:00:00Z")]) {
    assert.throws(() => hash(null, { clock: () => instant }), InputError);
  }
  assert.equal(hash(null, { clock: () => new Date("0001-01-01T00:00:00Z") }).calculatedAt, "0001-01-01T00:00:00Z");
  const other = { ...fixed, hash: () => Buffer.from("0123456789abcdef1123456789abcdef", "hex") };
  const collision = hash(null, { provider: other, clock });
  assert.equal(record.label, collision.label);
  assert.notEqual(record.digest, collision.digest);
  const later = hash(null, { provider: fixed, clock: () => new Date("2026-11-02T09:04:06Z") });
  assert.ok(record.label < later.label);
});
