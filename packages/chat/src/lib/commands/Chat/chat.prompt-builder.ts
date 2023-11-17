import { History } from '@the-artificial-agent/core';
import ChatMods from './chat.mods';
import ChatContext from './chat.context';
import ChatPrompt, { ChatProps } from './chat.prompt';
import { Injectable } from '@nestjs/common';

@Injectable()
export class ChatPromptBuilder {
  constructor(private readonly history: History) {}

  build({ message, context, mods, personality }: ChatProps): string {
    return ChatPrompt({
      personality,
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
