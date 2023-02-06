import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import TelegramBot, { Message } from 'node-telegram-bot-api';

@Injectable()
export class TelegramBotAdapter {
  private readonly logger = new Logger('TelegramBotAdapter');

  private chatId: number | null = this.config.get<number>(
    'providers.telegram.chatId'
  );

  private bot = new TelegramBot(this.config.get('providers.telegram.apiKey'), {
    polling: true,
  });

  constructor(private config: ConfigService) {}

  getChatId() {
    return this.chatId;
  }

  getBot() {
    return this.bot;
  }

  sendTextMessage(text: string) {
    if (!this.chatId) {
      this.logger.error('chatId is null');
      return;
    }

    this.bot.sendMessage(this.chatId, text);
    this.logger.log(`Sent message: ${text} to chatId: ${this.chatId}`);
  }

  onMessage(callback: (msg: Message, bot: TelegramBot) => void) {
    this.bot.on('message', async (msg) => {
      if (
        (this.chatId && this.chatId !== msg.chat.id) ||
        msg.text === '/start'
      ) {
        return;
      }

      this.chatId = msg.chat.id;

      this.logger.log(
        `Received message: ${msg.text} from chatId: ${this.chatId}`
      );

      callback(msg, this.bot);
    });
  }
}
