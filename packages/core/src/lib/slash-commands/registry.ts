import { Injectable, Logger } from '@nestjs/common';
import { SlashCommand, SlashCommandHandler } from './types';

@Injectable()
export class SlashCommandRegistry {
  private readonly logger = new Logger(SlashCommandRegistry.name);

  private readonly commands: Map<string, SlashCommand> = new Map();

  public registerCommands(commands: SlashCommand[]): void {
    commands.forEach((command) => this.registerCommand(command));
  }

  public registerCommand(params: SlashCommand): void {
    this.commands.set(params.name, params);

    this.logger.log(
      `registered slash command: ${params.name} with handler ${params.handler.constructor.name}`
    );
  }

  public getCommandNames(): string[] {
    return Array.from(this.commands.keys());
  }

  public getCommand(command: string): SlashCommand | undefined {
    if (command.startsWith('/')) {
      command = command.substring(1);
    }
    return this.commands.get(command);
  }

  public getCommandHandler(command: string): SlashCommandHandler | undefined {
    return this.commands.get(command)?.handler;
  }
}
