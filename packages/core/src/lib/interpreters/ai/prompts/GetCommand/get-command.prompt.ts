import GetCommandContext from './get-command.context';
import GetCommandMods from './get-command.mods';

const GetCommand = ({
  mods = GetCommandMods({}),
  context = GetCommandContext({}),
  message,
}: GetCommandProps) => `
What's the command name for the following message given this list of commands? ${mods}

${context}

Message: ${message}
`;

export type GetCommandProps = {
  message: string;
  personality?: string;
  mods?: string;
  context?: string;
};

export { GetCommandContext };

export default GetCommand;
