#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { hashJson } from "./index.js";

try {
  const { values, positionals } = parseArgs({
    options: { "prefix-length": { type: "string" }, help: { type: "boolean", short: "h" } },
    allowPositionals: true,
  });
  if (values.help) {
    console.log("Usage: rootprint [--prefix-length N] [FILE|-]\nHash strict UTF-8 JSON. Default: stdin, SHA-256.");
  } else {
    if (positionals.length > 1) throw new Error("Expected at most one file");
    const rawLength = values["prefix-length"];
    if (rawLength !== undefined && !/^[0-9]+$/.test(rawLength)) throw new Error("Prefix length must be an integer");
    const path = positionals[0];
    const bytes = readFileSync(path === undefined || path === "-" ? 0 : path);
    const text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
    console.log(JSON.stringify(hashJson(text, { prefixLength: rawLength === undefined ? undefined : Number(rawLength) })));
  }
} catch (error) {
  console.error(`rootprint: ${error instanceof Error ? error.message : "Calculation failed"}`);
  process.exitCode = 1;
}
