import ChatContext from './chat.context';
import ChatMods from './chat.mods';

const ChatPrompt = ({
  personality,
  mods = ChatMods({}),
  context = ChatContext({}),
  message,
}: ChatProps) => `
${personality} ${mods}

${context}

Answer the following message: ${message}
`;

export type ChatProps = {
  message: string;
  personality?: string;
  mods?: string;
  context?: string;
};

export { ChatContext, ChatMods };

export default ChatPrompt;
