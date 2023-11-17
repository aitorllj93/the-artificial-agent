import { Module } from '@nestjs/common';
import { CoreModule } from '@the-artificial-agent/core';

import { ChatHandler } from './commands/Chat/chat.handler';
import { ChatPromptBuilder } from './commands/Chat/chat.prompt-builder';
import { GoodMorningHandler } from './commands/GoodMorning/good-morning.handler';
import { NotFoundHandler } from './commands/NotFound/not-found.handler';
import NotifyPrompt from './commands/Notify/notify.prompt';

@Module({
  imports: [CoreModule],
  providers: [
    ChatPromptBuilder,
    {
      provide: ChatHandler.name,
      useClass: ChatHandler,
    },
    {
      provide: GoodMorningHandler.name,
      useClass: GoodMorningHandler,
    },
    {
      provide: NotFoundHandler.name,
      useClass: NotFoundHandler,
    },
  ],
  exports: [
    ChatPromptBuilder,
    ChatHandler.name,
    GoodMorningHandler.name,
    NotFoundHandler.name,
  ],
})
export class ChatModule {}

export { NotifyPrompt };
