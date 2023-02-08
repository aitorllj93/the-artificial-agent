import { Injectable, Logger } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import { Command } from '../../commands/types';
import { CommandRegistry } from '../../commands/registry';

import { SlashCommandRegistry } from '../../slash-commands/registry';

import { OpenAIAdapter } from '../../adapters/openai.adapter';

import GetParametersPrompt, {
  GetParametersContext,
} from './prompts/GetParameters/get-parameters.prompt';
import { GetCommandPromptBuilder } from './prompts/GetCommand/get-command.prompt-builder';
import { InterpreterRunner } from '../types';

@Injectable()
export class AIInterpreterRunner implements InterpreterRunner {
  private readonly logger = new Logger(AIInterpreterRunner.name);

  constructor(
    private readonly ai: OpenAIAdapter,
    private readonly slashRegistry: SlashCommandRegistry,
    private readonly aiRegistry: CommandRegistry,
    private readonly getCommandPromptBuilder: GetCommandPromptBuilder
  ) {}

  public async run(msg: Message) {
    if (msg.text.startsWith('/')) {
      return this.runSlashCommand(msg);
    }

    return this.runAICommand(msg);
  }

  public async runSlashCommand(msg: Message) {
    const [slashedCommand, ...parametersList] = msg.text
      .split(' ')
      .map((text) => text.trim());

    const command = this.slashRegistry.getCommand(slashedCommand);
    const parameters = command.parameters.reduce(
      (acc, parameter, index) =>
        Object.assign(acc, { [parameter]: parametersList[index] }),
      {}
    );

    return command.handler.handle(parameters, msg, command);
  }

  public async runAICommand(msg: Message) {
    const commandName = await this.getAICommandName(msg);
    const command = await this.aiRegistry.getCommand(commandName);
    const parameters = await this.getAICommandParameters(command, msg);

    return command.handler.handle(parameters, msg, command);
  }

  private async getAICommandName(msg: Message): Promise<string> {
    const prompt = this.getCommandPromptBuilder.build({ message: msg.text });
    const commandNames = this.aiRegistry.getPublicCommandNames();

    this.logger.log(`getting command for message: ${msg.text}`);

    const text = (
      await this.ai.generateTextFromPrompt(prompt, { temperature: 0 })
    ).replaceAll('"', '');

    return (
      commandNames.find((command) => command === text) ||
      commandNames.find((command) => text.includes(command)) ||
      this.aiRegistry.getFallbackCommand()
    );
  }

  private async getAICommandParameters<T = unknown>(
    command: Command,
    msg: Message
  ): Promise<T> {
    if (command.name === this.aiRegistry.getFallbackCommand())
      return {
        message: msg.text,
      } as T;

    const prompt = GetParametersPrompt({
      message: msg.text,
      context: GetParametersContext({
        examples: command.examples,
        propertyNames: command.parameters,
      }),
    });

    this.logger.log(`getting parameters for command: ${command}`);

    const text = await this.ai.generateTextFromPrompt(prompt);

    try {
      return JSON.parse(text);
    } catch (e) {
      console.error(`Error parsing parameters: ${text}`);
      return {
        message: msg.text,
        failed: true,
      } as T;
    }
  }
}
