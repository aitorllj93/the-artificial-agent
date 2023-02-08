import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

import { TelegramBotAdapter } from './adapters/telegram-bot.adapter';
import { History } from './history';
import type { Message } from './history';
import { OpenAIAdapter } from './adapters/openai.adapter';
import { Scheduler } from './scheduler';
import type { RecurrenceRuleAlike, JSONScheduleable } from './scheduler';
import { CommandRegistry } from './commands/registry';
import { GetCommandPromptBuilder } from './interpreters/ai/prompts/GetCommand/get-command.prompt-builder';
import type { Command, CommandHandler, JSONCommand } from './commands/types';
import type { JSONPersonality } from './personalities/types';
import { BotServer } from './server';
import { SlashCommandRegistry } from './slash-commands/registry';
import type {
  SlashCommand,
  SlashCommandHandler,
  JSONSlashCommand,
} from './slash-commands/types';
import { InterpreterManager } from './interpreters/manager';
import { InterpreterRegistry } from './interpreters/registry';
import type {
  Interpreter,
  JSONInterpreter,
  InterpreterRunner,
} from './interpreters/types';
import { AIInterpreterRunner } from './interpreters/ai/interpreter';
import { Bootstrapper } from './bootstrapper';
import { PersonalityRegistry } from './personalities/registry';

@Module({
  imports: [ConfigModule],
  providers: [
    TelegramBotAdapter,
    OpenAIAdapter,
    PersonalityRegistry,
    History,
    Scheduler,
    SlashCommandRegistry,
    CommandRegistry,
    GetCommandPromptBuilder,
    AIInterpreterRunner,
    InterpreterRegistry,
    InterpreterManager,
    BotServer,
    Bootstrapper,
  ],
  exports: [
    TelegramBotAdapter,
    OpenAIAdapter,
    History,
    PersonalityRegistry,
    Scheduler,
    SlashCommandRegistry,
    CommandRegistry,
    InterpreterRegistry,
    InterpreterManager,
    BotServer,
    ConfigModule,
    Bootstrapper,
  ],
})
export class CoreModule {}

export {
  BotServer,
  TelegramBotAdapter,
  OpenAIAdapter,
  PersonalityRegistry,
  History,
  Message,
  Scheduler,
  SlashCommand,
  SlashCommandHandler,
  JSONSlashCommand,
  SlashCommandRegistry,
  CommandRegistry,
  Command,
  CommandHandler,
  JSONCommand,
  RecurrenceRuleAlike,
  JSONPersonality,
  JSONScheduleable,
  InterpreterManager,
  InterpreterRegistry,
  Bootstrapper,
  Interpreter,
  JSONInterpreter,
  InterpreterRunner,
};
