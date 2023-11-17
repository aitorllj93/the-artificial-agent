import { Injectable } from '@nestjs/common';
import {
  Command,
  CommandHandler,
  History,
  OpenAIAdapter,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';
import GoodMorningPrompt from './good-morning.prompt';

@Injectable()
export class GoodMorningHandler implements CommandHandler {
  constructor(
    private ai: OpenAIAdapter,
    private history: History,
    private bot: TelegramBotAdapter
  ) {}

  public async handle(params, msg, { personality }: Command) {
    const prompt = GoodMorningPrompt({
      personality,
    });
    const text = await this.ai.generateTextFromPrompt(prompt);

    this.history.storeMessage({
      text,
      author: 'You',
      time: Date.now(),
    });

    this.bot.sendTextMessage(text);
  }
}
