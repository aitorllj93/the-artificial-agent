import { Injectable } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  Command,
  CommandHandler,
  OpenAIAdapter,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';

import { NotifyPrompt } from '@the-artificial-agent/chat';

import { ObsidianAdapter } from '../../adapters/obsidian/obsidian.adapter';

@Injectable()
export class AddNoteHandler implements CommandHandler<AddNoteCommand> {
  constructor(
    private readonly bot: TelegramBotAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly brain: ObsidianAdapter
  ) {}

  async handle(
    { text }: AddNoteCommand,
    msg: Message,
    { personality }: Command
  ) {
    await this.brain.insertAssistantContent(text);

    const prompt = NotifyPrompt({
      text: `Note "${text}" added to daily notes`,
      personality,
    });

    const notification = await this.ai.generateTextFromPrompt(prompt);

    this.bot.sendTextMessage(notification);
  }
}

export type AddNoteCommand = {
  text: string;
};
