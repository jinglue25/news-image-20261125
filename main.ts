import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const source = new URL('./entry.png', import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

if (!existsSync(source)) {
  throw new Error(`Missing file: ${fileURLToPath(source)}. Run draw.py first to generate entry.png next to main.ts.`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, `${outputDir}/entry.png`);
