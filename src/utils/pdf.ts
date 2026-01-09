import fs from 'node:fs';
import { extractText } from 'unpdf';

export async function extractPdfText(filePath: string): Promise<string> {
  const dataBuffer = fs.readFileSync(filePath);
  const data = await extractText(new Uint8Array(dataBuffer));
  return Array.isArray(data.text) ? data.text.join('\n\n') : '';
}
