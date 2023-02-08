const Enumerate = ({ personality, text }: EnumerateProps) => `
${personality} Enumerate the following item(s) by keeping the order and adding a number in front of each item. You can add a message after the list if you want to:


${text}

`;

export type EnumerateProps = {
  personality?: string;
  text: string;
};

export default Enumerate;
