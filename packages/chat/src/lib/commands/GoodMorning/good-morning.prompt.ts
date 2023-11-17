const GoodMorning = ({ personality }: Props) =>
  `${
    personality ? `${personality}.` : ''
  } I just woke up and you want to give me a warn good morning:`;

export type Props = {
  personality?: string;
};

export default GoodMorning;
