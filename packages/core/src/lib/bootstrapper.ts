import { Injectable, Logger } from '@nestjs/common';
import { ModuleRef } from '@nestjs/core';
import { ConfigService } from '@nestjs/config';

import { History } from './history';
import { BotServer } from './server';

import { InterpreterRegistry } from './interpreters/registry';
import { Interpreter, JSONInterpreter } from './interpreters/types';

import { PersonalityRegistry } from './personalities/registry';
import type { JSONPersonality } from './personalities/types';

import { SlashCommandRegistry } from './slash-commands/registry';
import { SlashCommand, JSONSlashCommand } from './slash-commands/types';

import { CommandRegistry } from './commands/registry';
import type { Command, JSONCommand } from './commands/types';

import { Scheduler } from './scheduler';
import type { JSONScheduleable } from './scheduler';

const INTERPRETERS_PATH = 'interpreters';
const SLASH_COMMANDS_PATH = 'slashCommands';
const COMMANDS_PATH = 'commands';
const PERSONALITIES_PATH = 'personalities';
const SCHEDULES_PATH = 'schedules';

@Injectable()
export class Bootstrapper {
  private logger = new Logger(Bootstrapper.name);

  constructor(
    private readonly scheduler: Scheduler,
    private readonly history: History,
    private readonly interpreterRegistry: InterpreterRegistry,
    private readonly personalityRegistry: PersonalityRegistry,
    private readonly slashCommandRegistry: SlashCommandRegistry,
    private readonly commandRegistry: CommandRegistry,
    private readonly server: BotServer,
    private readonly config: ConfigService,
    private readonly moduleRef: ModuleRef
  ) {}

  bootstrap() {
    this.personalityRegistry.registerPersonalities(
      this.config.get<JSONPersonality[]>(PERSONALITIES_PATH)
    );

    this.interpreterRegistry.registerInterpreters(
      this.getInterpreters(
        this.config.get<JSONInterpreter[]>(INTERPRETERS_PATH)
      )
    );

    this.slashCommandRegistry.registerCommands(
      this.getSlashCommands(
        this.config.get<JSONSlashCommand[]>(SLASH_COMMANDS_PATH)
      )
    );

    this.commandRegistry.registerCommands(
      this.getCommands(this.config.get<JSONCommand[]>(COMMANDS_PATH))
    );

    this.scheduler.scheduleCommands(
      this.config.get<JSONScheduleable[]>(SCHEDULES_PATH)
    );

    this.history.initialize().then(() => {
      this.server.start();
    });
  }

  private getInterpreters(interpreters: JSONInterpreter[] = []): Interpreter[] {
    return interpreters
      .map((interpreter) => {
        try {
          const runner = this.moduleRef.get(interpreter.runner, {
            strict: false,
          });

          return {
            ...interpreter,
            runner,
          } as Interpreter;
        } catch (e) {
          this.logger.error(
            `Could not find runner for interpreter ${interpreter.name}!`
          );
          return null;
        }
      })
      .filter(Boolean);
  }

  private getCommands(commands: JSONCommand[] = []): Command[] {
    return commands
      .map((command) => {
        try {
          const handler = this.moduleRef.get(command.handler, {
            strict: false,
          });
          return {
            ...command,
            handler,
          } as Command;
        } catch (e) {
          this.logger.error(
            `Could not find handler for command ${command.name}!`
          );
          return null;
        }
      })
      .filter(Boolean);
  }

  private getSlashCommands(commands: JSONSlashCommand[] = []): SlashCommand[] {
    return commands
      .map((command) => {
        try {
          const handler = this.moduleRef.get(command.handler, {
            strict: false,
          });
          return {
            ...command,
            handler,
          } as SlashCommand;
        } catch (e) {
          this.logger.error(
            `Could not find handler for slash command ${command.name}!`
          );
          return null;
        }
      })
      .filter(Boolean);
  }
}
