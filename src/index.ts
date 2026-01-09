#!/usr/bin/env bun
import { Command } from 'commander';
import { convertCommand } from './commands/convert.js';
import { configCommand } from './commands/config.js';
import packageJson from '../package.json' with { type: "json" };

const program = new Command();

program
  .description('Convert PDFs to Markdown using Bun and Gemini 3 Flash Preview AI')
  .version(packageJson.version)
  .addCommand(convertCommand, { isDefault: true })
  .addCommand(configCommand);

program.parse();
