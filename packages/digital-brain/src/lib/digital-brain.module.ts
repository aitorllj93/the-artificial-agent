import { Module } from '@nestjs/common';
import { CoreModule } from '@the-artificial-agent/core';

import { AddNoteHandler } from './commands/AddNote/add-note.handler';
import { ObsidianAdapter } from './adapters/obsidian/obsidian.adapter';
import { FreeWritingInterpreterRunner } from './interpreters/free-writing.runner';
import { AddTaskHandler } from './commands/AddTask/add-task.handler';
import { CompleteTaskHandler } from './commands/CompleteTask/complete-task.handler';
import { ListTasksHandler } from './commands/ListTasks/list-tasks.handler';

@Module({
  imports: [CoreModule],
  providers: [
    ObsidianAdapter,
    {
      provide: FreeWritingInterpreterRunner.name,
      useClass: FreeWritingInterpreterRunner,
    },
    {
      provide: AddNoteHandler.name,
      useClass: AddNoteHandler,
    },
    {
      provide: AddTaskHandler.name,
      useClass: AddTaskHandler,
    },
    {
      provide: CompleteTaskHandler.name,
      useClass: CompleteTaskHandler,
    },
    {
      provide: ListTasksHandler.name,
      useClass: ListTasksHandler,
    },
  ],
  exports: [
    ObsidianAdapter,
    FreeWritingInterpreterRunner.name,
    AddNoteHandler.name,
    AddTaskHandler.name,
    CompleteTaskHandler.name,
    ListTasksHandler.name,
  ],
})
export class DigitalBrainModule {}
