import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

import { Bootstrapper, CoreModule } from '@the-artificial-agent/core';

import { ChatModule } from '@the-artificial-agent/chat';
import { DigitalBrainModule } from '@the-artificial-agent/digital-brain';
import { EssentialsModule } from '@the-artificial-agent/essentials';

import load from './configuration';

@Module({
  imports: [
    ConfigModule.forRoot({
      load: [load],
    }),
    CoreModule,
    EssentialsModule,
    ChatModule,
    DigitalBrainModule,
  ],
  controllers: [],
})
export class AppModule {
  constructor(private readonly bootstrapper: Bootstrapper) {
    this.bootstrapper.bootstrap();
  }
}
