import { Message } from 'node-telegram-bot-api';
import {
  SlashCommand,
  SlashCommandHandler,
  InterpreterManager,
  TelegramBotAdapter,
  OpenAIAdapter,
  PersonalityRegistry,
} from '@the-artificial-agent/core';
import { NotifyPrompt } from '@the-artificial-agent/chat';
import { Injectable } from '@nestjs/common';

@Injectable()
export class SwitchInterpreterSHandler implements SlashCommandHandler {
  constructor(
    private readonly interpreterManager: InterpreterManager,
    private ai: OpenAIAdapter,
    private bot: TelegramBotAdapter,
    private readonly personalities: PersonalityRegistry
  ) {}

  public async handle(
    parameters: SwitchInterpreterSCommand,
    message: Message,
    { personality }: SlashCommand
  ): Promise<void> {
    const { interpreter } = parameters;

    this.interpreterManager.setInterpreter(interpreter);

    const personalityPrompt =
      this.personalities.getPersonalityPrompt(personality);

    const prompt = NotifyPrompt({
      personality: personalityPrompt,
      text: `Switched mode to "${interpreter}"`,
    });

    const notification = await this.ai.generateTextFromPrompt(prompt);

    await this.bot.sendTextMessage(notification);
  }
}

export type SwitchInterpreterSCommand = {
  interpreter: string;
  space?: string;
};
