import { Message } from '@the-artificial-agent/core';

const getDateTimeForMessage = (message: Message) => {
  const date = new Date(message.time);
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const isYersterday = date.getDate() === new Date().getDate() - 1;

  return `${hours}:${minutes}${isYersterday ? ' (Yesterday) ' : ''}`;
};

const ChatContext = ({ previousMessages }: ChatContextProps) => {
  const previousMessagesText = previousMessages
    .map((m) => `${getDateTimeForMessage(m)} ${m.author}: ${m.text}`)
    .join('\n');

  if (!previousMessages) {
    return '';
  }

  return `Previous Messages:
${previousMessagesText}`;
};

export type ChatContextProps = {
  previousMessages?: Message[];
};

export default ChatContext;
