import { Module } from '@nestjs/common';
import { CoreModule } from '@the-artificial-agent/core';

import { AddNoteHandler } from './commands/AddNote/add-note.handler';
import { ObsidianAdapter } from './adapters/obsidian/obsidian.adapter';

@Module({
  imports: [CoreModule],
  providers: [
    ObsidianAdapter,
    {
      provide: AddNoteHandler.name,
      useClass: AddNoteHandler,
    },
  ],
  exports: [ObsidianAdapter, AddNoteHandler.name],
})
export class DigitalBrainModule {}
