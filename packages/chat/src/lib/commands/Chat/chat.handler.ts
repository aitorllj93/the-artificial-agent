import { Injectable } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  History,
  OpenAIAdapter,
  TelegramBotAdapter,
  CommandHandler,
  Command,
} from '@the-artificial-agent/core';

import { ChatPromptBuilder } from './chat.prompt-builder';

@Injectable()
export class ChatHandler implements CommandHandler<ChatCommand> {
  constructor(
    private readonly bot: TelegramBotAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly history: History,
    private readonly promptBuilder: ChatPromptBuilder
  ) {}

  async handle(
    { message }: ChatCommand,
    msg: Message,
    { personality }: Command
  ) {
    const prompt = this.promptBuilder.build({ message, personality });

    let text = await this.ai.generateTextFromPrompt(prompt);

    // TODO: this is a hack, fix it
    if (text.startsWith('You:')) {
      text = text.replace('You:', '');
    }

    this.history.storeMessage({
      text,
      author: 'You',
      time: Date.now(),
    });

    this.bot.sendTextMessage(text);
  }
}

export type ChatCommand = {
  message: string;
};
