#!/usr/bin/env node
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";

const SCHEMA_VERSION = "motus.work-receipt-envelope.v0.1";
const CANONICALIZATION = "json.sorted.compact.v0";

function usage() {
  console.error("usage: emit-receipt.mjs --input <path> --output <path>");
}

function parseArgs(argv) {
  const args = {};
  for (let index = 2; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key || !key.startsWith("--") || !value) {
      usage();
      process.exit(2);
    }
    args[key.slice(2)] = value;
  }
  if (!args.input || !args.output) {
    usage();
    process.exit(2);
  }
  return args;
}

function sortForJson(value) {
  if (Array.isArray(value)) {
    return value.map(sortForJson);
  }
  if (value && typeof value === "object" && value.constructor === Object) {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortForJson(value[key])]),
    );
  }
  return value;
}

function canonicalBytes(value) {
  return Buffer.from(JSON.stringify(sortForJson(value)), "utf8");
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function sha256Document(value) {
  return sha256(canonicalBytes(value));
}

function digestText(value, canonicalization) {
  return {
    algorithm: "sha256",
    value: sha256(Buffer.from(value, "utf8")),
    canonicalization,
  };
}

function digestDocument(value, canonicalization) {
  return {
    algorithm: "sha256",
    value: sha256Document(value),
    canonicalization,
  };
}

function receiptDigestDocument(document) {
  const base = JSON.parse(JSON.stringify(document));
  delete base.receipt_id;
  if (base.hashes && typeof base.hashes === "object") {
    delete base.hashes.receipt;
  }
  return base;
}

function buildReceipt(source) {
  const eventsDigest = digestDocument(source.events, CANONICALIZATION);
  const receipt = {
    schema_version: SCHEMA_VERSION,
    receipt_id: `sha256:${"0".repeat(64)}`,
    run_id: source.run_id,
    work_id: source.work_id,
    actor: source.actor,
    runtime: {
      name: "motus-receipt-only-node",
      kind: "sdk",
      version: "0.1.0",
    },
    trigger: source.trigger ?? { kind: "manual" },
    instruction_ref: {
      kind: source.instruction.kind,
      summary: source.instruction.summary ?? "",
      digest: digestText(source.instruction.canonical_text, "utf8.instruction.v0"),
    },
    events_ref: {
      uri: source.events.uri,
      digest: eventsDigest,
    },
    evidence_refs: source.evidence_refs ?? [],
    tool_refs: source.tool_refs ?? [],
    outcome: source.outcome,
    acceptance: source.acceptance,
    route_summary: source.route_summary ?? { status: "complete" },
    handoff: source.handoff ?? { status: "none" },
    canonicalization: {
      method: CANONICALIZATION,
      volatile_fields: ["created_at"],
    },
    hashes: {
      receipt: {
        algorithm: "sha256",
        value: "0".repeat(64),
        canonicalization: CANONICALIZATION,
      },
      source_export: eventsDigest,
    },
    redaction: source.redaction ?? { status: "none" },
    created_at: source.created_at,
  };
  const receiptDigest = sha256Document(receiptDigestDocument(receipt));
  receipt.receipt_id = `sha256:${receiptDigest}`;
  receipt.hashes.receipt.value = receiptDigest;
  return receipt;
}

const args = parseArgs(process.argv);
const source = JSON.parse(readFileSync(args.input, "utf8"));
const receipt = buildReceipt(source);
writeFileSync(args.output, `${JSON.stringify(sortForJson(receipt), null, 2)}\n`, "utf8");
console.log(receipt.receipt_id);
