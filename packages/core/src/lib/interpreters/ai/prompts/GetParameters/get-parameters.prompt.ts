import GetParametersContext from './get-parameters.context';

const GetParameters = ({
  mods,
  context = GetParametersContext({}),
  message,
}: GetParametersProps) => `
What's the JSON representation for the following message given this list of properties? ${mods}

${context}

Message: ${message}
`;

export type GetParametersProps = {
  message: string;
  personality?: string;
  mods?: string;
  context?: string;
};

export { GetParametersContext };

export default GetParameters;
