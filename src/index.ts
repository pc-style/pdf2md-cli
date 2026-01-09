#!/usr/bin/env bun
import { Command } from 'commander';
import { convertCommand } from './commands/convert.js';
import { configCommand } from './commands/config.js';
import packageJson from '../package.json' with { type: "json" };

const program = new Command();

program
  .name('pdf2md')
  .description('Convert PDFs to Markdown using Bun and Gemini AI')
  .version(packageJson.version)
  .addCommand(convertCommand, { isDefault: true })
  .addCommand(configCommand);

program.parse();
