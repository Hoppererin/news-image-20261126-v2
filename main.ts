// news-image-20261126 v2 — entry program.
//
// The entry is a single pre-rendered image (entry.png) that sums up the
// world's news of Thursday 26 November 2026 as a one-page newspaper.
// This program copies it, byte for byte, to the output directory, then
// verifies the copy: PNG magic, 1024x1024 dimensions, size under 1 MiB,
// and a sha256 identical to the source. It uses only the Node standard
// library and needs no network.
//
// Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const srcPath = join(repoDir, "entry.png");
const dstPath = join(outDir, "entry.png");
const src = readFileSync(srcPath);

if (src.length > 1048576) {
  throw new Error("entry.png is over 1 MiB: " + src.length + " bytes");
}
if (src[0] !== 0x89 || src[1] !== 0x50 || src[2] !== 0x4e || src[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file");
}
const width = src.readUInt32BE(16);
const height = src.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error("entry.png is not 1024x1024: " + width + "x" + height);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(srcPath, dstPath);

const dst = readFileSync(dstPath);
const srcHash = createHash("sha256").update(src).digest("hex");
const dstHash = createHash("sha256").update(dst).digest("hex");
if (srcHash !== dstHash) {
  throw new Error("output copy does not match source: " + dstHash + " != " + srcHash);
}
console.log("wrote entry.png to " + outDir + " (" + dst.length + " bytes, sha256 " + dstHash + ")");
