import { Injectable, Logger } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import { Command } from '../handler';

import { OpenAIAdapter } from '../adapters/openai.adapter';

import GetParametersPrompt, {
  GetParametersContext,
} from './prompts/GetParameters/get-parameters.prompt';
import { GetCommandPromptBuilder } from './prompts/GetCommand/get-command.prompt-builder';
import { CommandRegistry } from '../registry';

@Injectable()
export class Interpreter {
  private readonly logger = new Logger(Interpreter.name);

  constructor(
    private readonly ai: OpenAIAdapter,
    private readonly registry: CommandRegistry,
    private readonly getCommandPromptBuilder: GetCommandPromptBuilder
  ) {}

  public async run(msg: Message) {
    const commandName = await this.getCommandName(msg);
    const command = this.registry.getCommand(commandName);
    const parameters = await this.getCommandParameters(command, msg);

    return command.handler.handle(parameters, msg, command);
  }

  public async getCommandName(msg: Message): Promise<string> {
    const prompt = this.getCommandPromptBuilder.build({ message: msg.text });
    const commandNames = this.registry.getPublicCommandNames();

    this.logger.log(`getting command for message: ${msg.text}`);

    const text = (
      await this.ai.generateTextFromPrompt(prompt, { temperature: 0 })
    ).replaceAll('"', '');

    return (
      commandNames.find((command) => command === text) ||
      commandNames.find((command) => text.includes(command)) ||
      this.registry.getFallbackCommand()
    );
  }

  public async getCommandParameters<T = unknown>(
    command: Command,
    msg: Message
  ): Promise<T> {
    if (command.name === this.registry.getFallbackCommand())
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
