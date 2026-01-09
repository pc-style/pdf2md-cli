import fs from 'node:fs';
import path from 'node:path';
import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { extractPdfText } from '../utils/pdf.js';
import { convertToMarkdown } from '../utils/gemini.js';
import { getApiKey } from '../utils/config.js';

async function processFile(filePath: string, mode: 'standalone' | 'ai', apiKey: string | null, output?: string) {
  const spinner = ora(`Processing ${path.basename(filePath)}...`).start();
  
  try {
    const text = await extractPdfText(filePath);
    
    let result = text;
    if (mode === 'ai') {
      if (!apiKey) {
        spinner.fail('API Key is required for AI mode. Use "pdf2md config --key <key>" or pass --api-key.');
        return false;
      }
      spinner.text = `Generative AI processing for ${path.basename(filePath)}...`;
      try {
        result = await convertToMarkdown(text, apiKey);
      } catch (e: any) {
         spinner.fail(`AI processing failed: ${e.message}`);
         return false;
      }
    }

    const outputPath = output || filePath.replace(/\.pdf$/i, '.md');
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, result);
    
    spinner.succeed(`Saved to ${outputPath}`);
    return true;
  } catch (error: any) {
    spinner.fail(`Error processing ${filePath}: ${error.message}`);
    return false;
  }
}

async function processDirectory(dirPath: string, mode: 'standalone' | 'ai', apiKey: string | null) {
  const files = fs.readdirSync(dirPath, { recursive: true }) as string[];
  const pdfFiles = files.filter(f => f.toLowerCase().endsWith('.pdf'));
  
  if (pdfFiles.length === 0) {
    console.log(chalk.yellow('No PDF files found in directory.'));
    return;
  }

  console.log(chalk.blue(`Found ${pdfFiles.length} PDF files in ${dirPath}`));
  
  let successCount = 0;
  for (const file of pdfFiles) {
    const fullPath = path.join(dirPath, file);
    // For directory processing, output is always side-by-side
    if (await processFile(fullPath, mode, apiKey)) {
      successCount++;
    }
  }
  
  console.log(chalk.green(`\nCompleted! ${successCount}/${pdfFiles.length} files processed.`));
}

export const convertCommand = new Command('convert')
  .description('Convert PDF to Markdown')
  .argument('<input>', 'Input file or directory')
  .option('-m, --mode <mode>', 'Mode: standalone (text extract) or ai (Gemini)', 'standalone')
  .option('-o, --output <output>', 'Output file path (only for single file)')
  .option('-k, --api-key <key>', 'Gemini API Key (overrides config)')
  .action(async (input, options) => {
    const apiKey = options.apiKey || getApiKey();
    const mode = options.mode;

    // Check if input exists
    if (!fs.existsSync(input)) {
        console.error(chalk.red(`Error: Input "${input}" not found.`));
        process.exit(1);
    }

    const stats = fs.statSync(input);
    
    if (stats.isFile()) {
        await processFile(input, mode, apiKey, options.output);
    } else if (stats.isDirectory()) {
        if (options.output) {
            console.warn(chalk.yellow('Warning: --output is ignored when processing a directory.'));
        }
        await processDirectory(input, mode, apiKey);
    } else {
        console.error(chalk.red('Error: Input is not a file or directory.'));
        process.exit(1);
    }
  });
