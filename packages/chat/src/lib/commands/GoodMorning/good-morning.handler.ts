import { Injectable } from '@nestjs/common';
import {
  Command,
  CommandHandler,
  History,
  OpenAIAdapter,
  PersonalityRegistry,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';
import GoodMorningPrompt from './good-morning.prompt';

@Injectable()
export class GoodMorningHandler implements CommandHandler {
  constructor(
    private ai: OpenAIAdapter,
    private history: History,
    private bot: TelegramBotAdapter,
    private personalities: PersonalityRegistry
  ) {}

  public async handle(params, msg, { personality }: Command) {
    const personalityPrompt =
      this.personalities.getPersonalityPrompt(personality);
    const prompt = GoodMorningPrompt({
      personality: personalityPrompt,
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
