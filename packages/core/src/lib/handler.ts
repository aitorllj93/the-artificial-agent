import { Message } from 'node-telegram-bot-api';

export interface CommandHandler<T = unknown> {
  handle: (params: T, msg: Message | null, command: Command) => Promise<void>;
}

export type Command = {
  name: string;
  handler: CommandHandler;
  personality?: string;
  examples?: [
    {
      in: string;
      out: string;
    }
  ];
  parameters?: string[];
  asFallback?: boolean;
  internal?: boolean;
};

export type JSONCommand = Omit<Command, 'handler'> & {
  handler: string;
};
