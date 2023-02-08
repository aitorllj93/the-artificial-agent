import { Injectable, Logger } from '@nestjs/common';

import { History } from './history';
import { TelegramBotAdapter } from './adapters/telegram-bot.adapter';
import { InterpreterManager } from './interpreters/manager';

@Injectable()
export class BotServer {
  private logger = new Logger('BotServer');

  constructor(
    private botAdapter: TelegramBotAdapter,
    private readonly interpreterManager: InterpreterManager,
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

        const { runner } = this.interpreterManager.getInterpreter();

        await runner.run(msg);
      } catch (e) {
        console.error(e);
      }
    });
  }
}
