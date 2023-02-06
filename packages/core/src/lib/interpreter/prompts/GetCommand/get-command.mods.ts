const GetCommandMods = ({ fallbackCommand }: GetCommandModsProps) => {
  return `If you don't know, answer with "${fallbackCommand}"`;
};

export type GetCommandModsProps = {
  fallbackCommand?: string;
};

export default GetCommandMods;
