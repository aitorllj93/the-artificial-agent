import { Injectable, Logger } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  InterpreterRunner,
  OpenAIAdapter,
  SlashCommandRegistry,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';
import { ObsidianAdapter } from '../adapters/obsidian/obsidian.adapter';

@Injectable()
export class FreeWritingInterpreterRunner implements InterpreterRunner {
  private logger = new Logger(FreeWritingInterpreterRunner.name);

  constructor(
    private readonly slashRegistry: SlashCommandRegistry,
    private readonly digitalBrain: ObsidianAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly bot: TelegramBotAdapter
  ) {}

  public async run(msg: Message) {
    if (msg.text.startsWith('/')) {
      return this.runSlashCommand(msg);
    }

    await this.digitalBrain.addFreeWriting(msg.text);

    const completionSuggestion = await this.ai.generateTextFromPrompt(
      `You're a writer with more than 20 years of experience. You write any kind of texts. Continue the following text: ${msg.text}`
    );

    return this.bot.sendTextMessage(completionSuggestion);
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
}
