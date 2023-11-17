import { Injectable } from '@nestjs/common';

import { CommandHandler, TelegramBotAdapter } from '@the-artificial-agent/core';

@Injectable()
export class NotFoundHandler implements CommandHandler {
  constructor(private readonly botAdapter: TelegramBotAdapter) {}

  async handle() {
    this.botAdapter.sendTextMessage('Command not found');
  }
}
