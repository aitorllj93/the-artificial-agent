import { Module } from '@nestjs/common';
import { CoreModule } from '@the-artificial-agent/core';

import { NotFoundHandler } from './not-found.handler';

@Module({
  imports: [CoreModule],
  providers: [
    {
      provide: NotFoundHandler.name,
      useClass: NotFoundHandler,
    },
  ],
  exports: [NotFoundHandler.name],
})
export class NotFoundModule {}
