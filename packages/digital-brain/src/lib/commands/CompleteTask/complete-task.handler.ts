import { Injectable, Logger } from '@nestjs/common';
import { Message } from 'node-telegram-bot-api';

import {
  Command,
  CommandHandler,
  OpenAIAdapter,
  PersonalityRegistry,
  TelegramBotAdapter,
} from '@the-artificial-agent/core';

import { ErrorPrompt, NotifyPrompt } from '@the-artificial-agent/chat';

import { ObsidianAdapter } from '../../adapters/obsidian/obsidian.adapter';

@Injectable()
export class CompleteTaskHandler
  implements CommandHandler<CompleteTaskCommand>
{
  private readonly logger = new Logger(CompleteTaskHandler.name);

  constructor(
    private readonly bot: TelegramBotAdapter,
    private readonly ai: OpenAIAdapter,
    private readonly brain: ObsidianAdapter,
    private readonly personalities: PersonalityRegistry
  ) {}

  async handle(
    { text }: CompleteTaskCommand,
    msg: Message,
    { personality }: Command
  ) {
    const tasks = await this.brain.getTasks();

    const prompt = `Answer only with the number of the task to be completed. There's only one correct answer:

${tasks.map((task, index) => `${index + 1}. ${task.value}`).join('\n')}

message: ${text}`;

    const taskToComplete = (
      await this.ai.generateTextFromPrompt(prompt, {
        temperature: 0.1,
      })
    ).trim();

    try {
      const taskIndex = parseInt(taskToComplete, 10) - 1;

      const task = tasks[taskIndex];

      if (!task) {
        throw new Error('Task not found');
      }

      if (task.value.startsWith('[x]')) {
        throw new Error('Task already completed');
      }

      await this.brain.completeTask(task);

      const prompt = NotifyPrompt({
        text: `Task "${task.value.replace('[ ]', '')}" completed`,
        personality: this.personalities.getPersonalityPrompt(personality),
      });

      const notification = await this.ai.generateTextFromPrompt(prompt);

      this.bot.sendTextMessage(notification);
    } catch (e) {
      this.logger.error(e);

      const prompt = ErrorPrompt({
        text: e.message,
        personality: this.personalities.getPersonalityPrompt(personality),
      });

      const notification = await this.ai.generateTextFromPrompt(prompt);

      this.bot.sendTextMessage(notification);
    }

    // const personalityPrompt =
    //   this.personalities.getPersonalityPrompt(personality);

    // const prompt = NotifyPrompt({
    //   text: `Task "${text}" added to daily notes`,
    //   personality: personalityPrompt,
    // });

    // const notification = await this.ai.generateTextFromPrompt(prompt);

    // this.bot.sendTextMessage(notification);
  }
}

export type CompleteTaskCommand = {
  text: string;
};
