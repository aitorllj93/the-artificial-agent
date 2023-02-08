import { Message } from 'node-telegram-bot-api';

export interface SlashCommandHandler<T = unknown> {
  handle: (
    params: T,
    msg: Message | null,
    command: SlashCommand
  ) => Promise<void>;
}

export type SlashCommand = {
  name: string;
  description?: string;
  handler: SlashCommandHandler;
  personality?: string;
  examples?: [
    {
      in: string;
      out: string;
    }
  ];
  parameters?: string[];
};

export type JSONSlashCommand = Omit<SlashCommand, 'handler'> & {
  handler: string;
};
