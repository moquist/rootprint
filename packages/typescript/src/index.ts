import { createHash } from "node:crypto";
import canonicalizeModule from "canonicalize";
import { parseTree, type Node, type ParseError } from "jsonc-parser";

// canonicalize's CJS export has a callable default at runtime.
const canonicalize = canonicalizeModule as unknown as (value: unknown) => string;
export const PROTOCOL = "rootprint-v1";
export class InputError extends Error {}
export class AlgorithmError extends Error {}

export interface HashProvider {
  readonly algorithm: string;
  readonly digestLength: number;
  hash(data: Uint8Array): Uint8Array;
}

export const sha256: HashProvider = Object.freeze({
  algorithm: "sha256",
  digestLength: 32,
  hash: (data: Uint8Array) => createHash("sha256").update(data).digest(),
});

export interface HashRecord {
  protocol: typeof PROTOCOL;
  algorithm: string;
  digest: string;
  calculatedAt: string;
  label: string;
}

export interface HashOptions {
  provider?: HashProvider;
  prefixLength?: number;
  clock?: () => Date;
}

function validString(value: string): void {
  if (/[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/.test(value)) {
    throw new InputError("Unpaired Unicode surrogate");
  }
}

/** Parse without losing duplicate-key evidence. Native JSON.parse alone cannot do this. */
export function parseJson(text: string): unknown {
  if (typeof text !== "string") throw new InputError("JSON text must be a string");
  try {
    const errors: ParseError[] = [];
    const root = parseTree(text, errors, { disallowComments: true, allowTrailingComma: false });
    if (!root || errors.length) throw new InputError("Invalid strict JSON");
    function check(node: Node, depth: number): void {
      if (depth > 512) throw new InputError("JSON nesting exceeds supported depth");
      if (node.type === "object") {
        const names = new Set<string>();
        for (const property of node.children ?? []) {
          const key = property.children![0]!.value as string;
          if (names.has(key)) throw new InputError("Duplicate object key");
          names.add(key);
        }
      }
      for (const child of node.children ?? []) check(child, depth + 1);
    }
    check(root, 0);
    return JSON.parse(text) as unknown;
  } catch (error) {
    if (error instanceof InputError) throw error;
    throw new InputError("Invalid JSON or unsupported nesting");
  }
}

/** Full deterministic root digest. No clock or shortening participates. */
export function digest(value: unknown, provider: HashProvider = sha256): string {
  if (!provider || typeof provider.algorithm !== "string" || !/^[a-z0-9]+$/.test(provider.algorithm)
      || !Number.isSafeInteger(provider.digestLength) || provider.digestLength < 1 || typeof provider.hash !== "function") {
    throw new AlgorithmError("Invalid hash provider");
  }
  const ancestors = new Set<object>();
  function node(v: unknown, depth: number): string {
    if (depth > 256) throw new InputError("JSON nesting exceeds supported depth");
    let representation: unknown;
    if (v === null || typeof v === "boolean" || typeof v === "string" || typeof v === "number") {
      if (typeof v === "string") validString(v);
      if (typeof v === "number" && !Number.isFinite(v)) throw new InputError("Number must be finite binary64");
      representation = [PROTOCOL, "value", v];
    } else if (typeof v === "object") {
      const array = Array.isArray(v);
      if (!array && Object.getPrototypeOf(v) !== Object.prototype && Object.getPrototypeOf(v) !== null) {
        throw new InputError("Only plain JSON objects are supported");
      }
      if (ancestors.has(v)) throw new InputError("Cyclic input");
      ancestors.add(v);
      try {
        const descriptors = Object.getOwnPropertyDescriptors(v);
        const keys = Reflect.ownKeys(v);
        for (const key of keys) {
          if (array && key === "length") continue;
          if (typeof key !== "string") throw new InputError("Symbol keys are not JSON");
          const property = descriptors[key]!;
          if (!("value" in property) || !property.enumerable) throw new InputError("Only enumerable data properties are JSON");
          validString(key);
        }
        if (array) {
          if (keys.length !== v.length + 1) throw new InputError("Sparse arrays and array properties are not JSON");
          const children: string[] = [];
          for (let i = 0; i < v.length; i++) {
            if (!Object.hasOwn(descriptors, String(i))) throw new InputError("Sparse array");
            children.push(node(descriptors[String(i)]!.value, depth + 1));
          }
          representation = [PROTOCOL, "array", children];
        } else {
          const pairs = (keys as string[]).sort().map(key => [key, node(descriptors[key]!.value, depth + 1)]);
          representation = [PROTOCOL, "object", pairs];
        }
      } finally {
        ancestors.delete(v);
      }
    } else {
      throw new InputError("Unsupported non-JSON value");
    }
    const preimage = new TextEncoder().encode(canonicalize(representation));
    let output: Uint8Array;
    try { output = provider.hash(preimage); }
    catch { throw new AlgorithmError("Hash provider failed"); }
    if (!(output instanceof Uint8Array) || output.byteLength !== provider.digestLength) {
      throw new AlgorithmError("Hash provider returned invalid bytes or digest length");
    }
    return Buffer.from(output).toString("hex");
  }
  return node(value, 0);
}

export function hash(value: unknown, options: HashOptions = {}): HashRecord {
  const provider = options.provider ?? sha256;
  const full = digest(value, provider);
  const length = options.prefixLength ?? Math.min(16, full.length);
  if (!Number.isInteger(length) || length < 1 || length > full.length) throw new InputError("Invalid prefix length");
  const now = (options.clock ?? (() => new Date()))();
  if (!(now instanceof Date) || !Number.isFinite(now.getTime()) || now.getUTCFullYear() < 1 || now.getUTCFullYear() > 9999) {
    throw new InputError("Clock must return a valid UTC instant in years 0001–9999");
  }
  const calculatedAt = now.toISOString().slice(0, 19) + "Z";
  const date = calculatedAt.slice(0, 10).replaceAll("-", "");
  const time = calculatedAt.slice(11, 19).replaceAll(":", "");
  return { protocol: PROTOCOL, algorithm: provider.algorithm, digest: full, calculatedAt,
    label: `${date}_${time}-${provider.algorithm}-${PROTOCOL.slice("rootprint-".length)}-${full.slice(0, length)}` };
}

export function hashJson(text: string, options: HashOptions = {}): HashRecord {
  return hash(parseJson(text), options);
}
