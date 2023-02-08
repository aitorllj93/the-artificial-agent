import { Message } from 'node-telegram-bot-api';

export interface InterpreterRunner {
  run(msg: Message): Promise<void>;
}

export type Interpreter = {
  name: string;
  description?: string;
  runner: InterpreterRunner;
};

export type JSONInterpreter = Omit<Interpreter, 'runner'> & {
  runner: string;
};
