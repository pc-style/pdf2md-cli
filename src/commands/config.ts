import { Command } from 'commander';
import { setApiKey, getApiKey, deleteApiKey } from '../utils/config.js'; // Note .js extension for native ESM in Bun
import chalk from 'chalk';

export const configCommand = new Command('config')
  .description('Configure PDF2MD settings')
  .option('-k, --key <key>', 'Set Gemini 3 Flash Preview API Key')
  .option('-d, --delete', 'Delete stored API Key')
  .option('-s, --show', 'Show current API Key (masked)')
  .action((options) => {
    if (options.key) {
      setApiKey(options.key);
      console.log(chalk.green('API Key saved successfully!'));
    } else if (options.delete) {
      deleteApiKey();
      console.log(chalk.yellow('API Key removed.'));
    } else if (options.show) {
      const key = getApiKey();
      if (key) {
        const masked = key.slice(0, 4) + '*'.repeat(key.length - 8) + key.slice(-4);
        console.log(`Current API Key: ${chalk.cyan(masked)}`);
      } else {
        console.log(chalk.red('No API Key set.'));
      }
    } else {
      console.log('Use --key, --delete, or --show.');
    }
  });
