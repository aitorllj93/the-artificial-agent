const Notification = ({ personality, text }: NotificationProps) => `
${personality} Tell me that you successfully ran the following command:

Example: Note "Hello World" added to daily notes
Added "Hello World" into your daily notes!


Command: ${text}

`;

export type NotificationProps = {
  personality?: string;
  text: string;
};

export default Notification;
