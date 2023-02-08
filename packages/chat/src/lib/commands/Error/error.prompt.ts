const Error = ({ personality, text }: ErrorProps) => `
${personality} Tell me that you failed running the following command:

Example: Note "Hello World" added to daily notes
Failed to add "Hello World" into your daily notes!


Command: ${text}

`;

export type ErrorProps = {
  personality?: string;
  text: string;
};

export default Error;
