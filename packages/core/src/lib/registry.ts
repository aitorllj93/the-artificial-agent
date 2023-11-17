import { Injectable, Logger } from '@nestjs/common';
import { Command, CommandHandler } from './handler';

@Injectable()
export class CommandRegistry {
  private readonly logger = new Logger(CommandRegistry.name);

  private readonly commands: Map<string, Command> = new Map();
  private fallbackCommand: string;

  public registerCommands(commands: Command[]): void {
    commands.forEach((command) => this.registerCommand(command));
  }

  public registerCommand(params: Command): void {
    this.commands.set(params.name, params);

    this.logger.log(
      `registered${params.internal ? ' internal' : ''} command: ${
        params.name
      } with handler ${params.handler.constructor.name}`
    );

    if (params.asFallback) {
      this.fallbackCommand = params.name;
      this.logger.log(`registered fallback command: ${params.name}`);
    }
  }

  public getCommandNames(): string[] {
    return Array.from(this.commands.keys());
  }

  /**
   * Gets a list of public command names interpretable by the machine, excluding the internal ones.
   * @returns {string[]} command names
   */
  public getPublicCommandNames(): string[] {
    return Array.from(this.commands.keys()).filter(
      (command) => !this.commands.get(command).internal
    );
  }

  public getCommand(command: string): Command {
    return (
      this.commands.get(command) || this.commands.get(this.fallbackCommand)
    );
  }

  public getCommandHandler(command: string): CommandHandler {
    return (
      this.commands.get(command)?.handler || this.getFallbackCommandHandler()
    );
  }

  public getFallbackCommandHandler(): CommandHandler {
    return this.commands.get(this.fallbackCommand).handler;
  }

  public getFallbackCommand(): string {
    return this.fallbackCommand;
  }
}
