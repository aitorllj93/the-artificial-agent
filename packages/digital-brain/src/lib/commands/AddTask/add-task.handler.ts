import { Injectable } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  Command,
  CommandHandler,
  OpenAIAdapter,
  PersonalityRegistry,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';

import { NotifyPrompt } from '@the-artificial-agent/chat';

import { ObsidianAdapter } from '../../adapters/obsidian/obsidian.adapter';

@Injectable()
export class AddTaskHandler implements CommandHandler<AddTaskCommand> {
  constructor(
    private readonly bot: TelegramBotAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly brain: ObsidianAdapter,
    private readonly personalities: PersonalityRegistry
  ) {}

  async handle(
    { text }: AddTaskCommand,
    msg: Message,
    { personality }: Command
  ) {
    await this.brain.insertAssistantContent(`- [ ] ${text}`);

    const personalityPrompt =
      this.personalities.getPersonalityPrompt(personality);

    const prompt = NotifyPrompt({
      text: `Task "${text}" added to daily notes`,
      personality: personalityPrompt,
    });

    const notification = await this.ai.generateTextFromPrompt(prompt);

    this.bot.sendTextMessage(notification);
  }
}

export type AddTaskCommand = {
  text: string;
};
