import { Message } from '@the-artificial-agent/core';

// Every 60 minutes, include a greeting.
const GREETING_TIME = 60 * 60 * 1000;

const TimeMod = () => {
  const date = new Date();
  const hours = date.getHours();
  const minutes = date.getMinutes();

  return `The time is ${hours}:${minutes}.`;
};

const GreetingMod = ({ lastMessage }: ChatModsProps) => {
  if (!lastMessage) {
    return '';
  }

  const timeAfterLastMessage = Date.now() - lastMessage.time;
  const shouldGreet = timeAfterLastMessage > GREETING_TIME;

  return shouldGreet ? 'Include a greeting.' : '';
};

const ChatMods = ({ lastMessage }: ChatModsProps) => {
  const mods = [TimeMod(), GreetingMod({ lastMessage })].filter(Boolean);

  return mods.join(' ');
};

export type ChatModsProps = {
  lastMessage?: Message;
};

export default ChatMods;
