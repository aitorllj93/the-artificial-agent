import { Injectable } from '@nestjs/common';

import { History, PersonalityRegistry } from '@the-artificial-agent/core';

import ChatMods from './chat.mods';
import ChatContext from './chat.context';
import ChatPrompt, { ChatProps } from './chat.prompt';

@Injectable()
export class ChatPromptBuilder {
  constructor(
    private readonly history: History,
    private readonly personalityRegistry: PersonalityRegistry
  ) {}

  build({ message, context, mods, personality }: ChatProps): string {
    return ChatPrompt({
      personality: this.personalityRegistry.getPersonalityPrompt(personality),
      mods:
        mods ||
        ChatMods({
          lastMessage: this.history.getLastMessage(),
        }),
      context:
        context ||
        ChatContext({
          previousMessages: this.history.getPreviousMessages(),
        }),
      message,
    });
  }
}
