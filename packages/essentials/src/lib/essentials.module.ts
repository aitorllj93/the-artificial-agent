import { Module } from '@nestjs/common';
import { SwitchInterpreterSHandler } from './commands/switch-interpreter.handler';
import { CoreModule } from '@the-artificial-agent/core';

@Module({
  imports: [CoreModule],
  providers: [
    {
      provide: SwitchInterpreterSHandler.name,
      useClass: SwitchInterpreterSHandler,
    },
  ],
  exports: [SwitchInterpreterSHandler.name],
})
export class EssentialsModule {}
