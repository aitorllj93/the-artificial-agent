import { Injectable } from '@nestjs/common';

import GetCommandMods from './get-command.mods';
import GetCommandContext from './get-command.context';
import GetCommandPrompt, { GetCommandProps } from './get-command.prompt';
import { CommandRegistry } from '../../../registry';

@Injectable()
export class GetCommandPromptBuilder {
  constructor(private readonly registry: CommandRegistry) {}

  build({ message, context, mods, personality }: GetCommandProps): string {
    return GetCommandPrompt({
      personality,
      mods:
        mods ||
        GetCommandMods({
          fallbackCommand: this.registry.getFallbackCommand(),
        }),
      context:
        context ||
        GetCommandContext({
          commandNames: this.registry.getPublicCommandNames(),
        }),
      message,
    });
  }
}
