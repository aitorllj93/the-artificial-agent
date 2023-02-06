import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { readFile, appendFile, mkdir } from 'node:fs/promises';

@Injectable()
export class History {
  private readonly MESSAGES_FILE = `data/messages${
    this.config.get('source') ? `.${this.config.get('source')}` : ''
  }.txt`;
  private readonly ENCODING = 'utf8';
  private readonly MAX_MESSAGES_IN_CONTEXT = 4;

  private readonly previousMessages: Message[] = [];

  constructor(private readonly config: ConfigService) {}

  async initialize() {
    await mkdir('data', { recursive: true });
    await appendFile(this.MESSAGES_FILE, '', this.ENCODING);

    const content = await readFile(this.MESSAGES_FILE, this.ENCODING);

    if (content.length === 0) {
      return;
    }

    const messages = content
      .split('\n')
      .map((line) => {
        if (line.length === 0) {
          return null;
        }

        const [text, author, time] = line.split(' | ');

        return {
          text,
          author,
          time: Number(time),
        };
      })
      .filter(Boolean);

    const lastMessages = messages.slice(-this.MAX_MESSAGES_IN_CONTEXT);

    this.previousMessages.push(...lastMessages);
  }

  storeMessage(message: Message) {
    if (this.previousMessages.length > this.MAX_MESSAGES_IN_CONTEXT) {
      this.previousMessages.shift();
    }

    appendFile(
      this.MESSAGES_FILE,
      `${message.text} | ${message.author} | ${message.time} \n`,
      this.ENCODING
    );

    this.previousMessages.push(message);
  }

  getPreviousMessages() {
    return this.previousMessages;
  }

  getLastMessage() {
    return this.previousMessages[this.previousMessages.length - 1];
  }
}

export type Message = {
  text: string;
  author: string;
  time: number;
};
