import { Injectable, Logger } from '@nestjs/common';

import { Interpreter } from './interpreter/interpreter';
import { History } from './history';
import { TelegramBotAdapter } from './adapters/telegram-bot.adapter';

@Injectable()
export class BotServer {
  private logger = new Logger('BotServer');

  constructor(
    private botAdapter: TelegramBotAdapter,
    private interpreter: Interpreter,
    private history: History
  ) {}

  start() {
    this.logger.log('Connecting to Telegram...');
    this.botAdapter.onMessage(async (msg) => {
      try {
        this.history.storeMessage({
          text: msg.text,
          author: 'Me',
          time: msg.date,
        });

        await this.interpreter.run(msg);
      } catch (e) {
        console.error(e);
      }
    });
  }
}
