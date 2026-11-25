// Entry for news-image-20261124: the picture of Tuesday 24 November 2026.
//
// The finished picture is entry.png, drawn by generate.py from the
// day's verified headlines. The grader runs this program with no
// network on Node 22 (standard library only), so all it does is
// deliver the picture: copy entry.png into the output directory
// under the same name. The gate accepts it as a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const entry = new URL("entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(entry, join(outDir, "entry.png"));
