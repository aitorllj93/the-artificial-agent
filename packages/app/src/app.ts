import { Module } from '@nestjs/common';
import { ModuleRef } from '@nestjs/core';
import { ConfigModule, ConfigService } from '@nestjs/config';

import {
  BotServer,
  Command,
  CommandRegistry,
  CoreModule,
  History,
  JSONCommand,
  JSONPersonality,
  JSONScheduleable,
  Scheduler,
} from '@the-artificial-agent/core';

import { ChatModule } from '@the-artificial-agent/chat';
import { DigitalBrainModule } from '@the-artificial-agent/digital-brain';

import load from './configuration';

const COMMANDS_PATH = 'commands';
const PERSONALITIES_PATH = 'personalities';
const SCHEDULES_PATH = 'schedules';

@Module({
  imports: [
    ConfigModule.forRoot({
      load: [load],
    }),
    CoreModule,
    ChatModule,
    DigitalBrainModule,
  ],
  controllers: [],
})
export class AppModule {
  constructor(
    readonly scheduler: Scheduler,
    readonly history: History,
    readonly registry: CommandRegistry,
    readonly server: BotServer,
    readonly config: ConfigService,
    private moduleRef: ModuleRef
  ) {
    const defs = this.config.get<JSONCommand[]>(COMMANDS_PATH);
    const personalities =
      this.config.get<JSONPersonality[]>(PERSONALITIES_PATH);
    const schedules = this.config.get<JSONScheduleable[]>(SCHEDULES_PATH);
    const commands = this.getCommands({ defs, personalities });

    registry.registerCommands(commands);
    scheduler.scheduleCommands(schedules);

    history.initialize().then(() => {
      server.start();
    });
  }

  private getCommands({
    defs,
    personalities,
  }: {
    defs: JSONCommand[];
    personalities: JSONPersonality[];
  }): Command[] {
    return defs.map((command) => {
      const handler = this.moduleRef.get(command.handler, {
        strict: false,
      });

      return {
        ...command,
        personality: personalities.find((p) => p.name === command.personality)
          .prompt,
        handler,
      } as Command;
    });
  }
}
