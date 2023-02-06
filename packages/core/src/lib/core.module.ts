import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

import { TelegramBotAdapter } from './adapters/telegram-bot.adapter';
import { History } from './history';
import type { Message } from './history';
import { OpenAIAdapter } from './adapters/openai.adapter';
import { Scheduler } from './scheduler';
import type { RecurrenceRuleAlike, JSONScheduleable } from './scheduler';
import { CommandRegistry } from './registry';
import { Interpreter } from './interpreter/interpreter';
import { GetCommandPromptBuilder } from './interpreter/prompts/GetCommand/get-command.prompt-builder';
import type { Command, CommandHandler, JSONCommand } from './handler';
import type { JSONPersonality } from './personality';
import { BotServer } from './server';

@Module({
  imports: [ConfigModule],
  providers: [
    TelegramBotAdapter,
    OpenAIAdapter,
    History,
    Scheduler,
    CommandRegistry,
    GetCommandPromptBuilder,
    Interpreter,
    BotServer,
  ],
  exports: [
    TelegramBotAdapter,
    OpenAIAdapter,
    History,
    Scheduler,
    CommandRegistry,
    Interpreter,
    BotServer,
    ConfigModule,
  ],
})
export class CoreModule {}

export {
  BotServer,
  TelegramBotAdapter,
  OpenAIAdapter,
  History,
  Message,
  Scheduler,
  CommandRegistry,
  Interpreter,
  Command,
  CommandHandler,
  JSONCommand,
  RecurrenceRuleAlike,
  JSONPersonality,
  JSONScheduleable,
};
