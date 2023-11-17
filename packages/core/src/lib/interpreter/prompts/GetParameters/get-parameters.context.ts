const GetParametersContext = ({
  examples,
  propertyNames,
}: GetParametersContextProps) => {
  return `
Examples:
${examples.map(
  (c) => `${c.in}
${c.out}

`
)}

Properties: ${propertyNames.map((c) => `"${c}"`).join(', ')}
`;
};

export type GetParametersContextProps = {
  examples?: {
    in: string;
    out: string;
  }[];
  propertyNames?: string[];
};

export default GetParametersContext;
