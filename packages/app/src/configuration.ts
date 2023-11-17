import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import * as yaml from 'js-yaml';
import yargs from 'yargs/yargs';
import { hideBin } from 'yargs/helpers';
import { Logger } from '@nestjs/common';

const logger = new Logger('Configuration');

const args = yargs(hideBin(process.argv))
  .options({
    config: {
      alias: 'c',
      type: 'string',
      description: 'Path to config file',
      default: undefined,
    },
  })
  .parse() as Record<string, string>;

const BASE_PATH = 'config';
const YAML_CONFIG_FILENAME = `${BASE_PATH}/config${
  args.config ? `.${args.config}` : ''
}.yml`;

export default () => {
  logger.log(`Loading configuration from ${YAML_CONFIG_FILENAME}`);
  const data = yaml.load(
    readFileSync(join(YAML_CONFIG_FILENAME), 'utf8')
  ) as Record<string, any>;

  data.source = args.config;

  return data;
};
