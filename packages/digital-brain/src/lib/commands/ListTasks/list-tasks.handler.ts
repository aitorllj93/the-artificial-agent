import { Injectable } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  Command,
  CommandHandler,
  OpenAIAdapter,
  PersonalityRegistry,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';

import { EnumeratePrompt } from '@the-artificial-agent/chat';

import { ObsidianAdapter } from '../../adapters/obsidian/obsidian.adapter';

@Injectable()
export class ListTasksHandler implements CommandHandler<ListTasksCommand> {
  constructor(
    private readonly bot: TelegramBotAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly brain: ObsidianAdapter,
    private readonly personalities: PersonalityRegistry
  ) {}

  async handle(
    { completed, space }: ListTasksCommand,
    msg: Message,
    { personality }: Command
  ) {
    const tasks = await this.brain.getTasks({
      completed,
    });

    const personalityPrompt =
      this.personalities.getPersonalityPrompt(personality);

    const prompt = EnumeratePrompt({
      text: tasks.map((task, index) => task.value).join('\n'),
      personality: personalityPrompt,
    });

    const message = await this.ai.generateTextFromPrompt(prompt);

    this.bot.sendTextMessage(message);
  }
}

export type ListTasksCommand = {
  space: string;
  completed: boolean;
};
