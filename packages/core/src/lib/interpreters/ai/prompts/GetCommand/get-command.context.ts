const GetCommandContext = ({ commandNames = [] }: GetCommandContextProps) => {
  return `
Example: Email Susan with the subject "Today's review" and the message "Can we reschedule this meeting?"
"Send Email"

Commands: ${commandNames.map((c) => `"${c}"`).join(', ')}
`;
};

export type GetCommandContextProps = {
  commandNames?: string[];
};

export default GetCommandContext;
