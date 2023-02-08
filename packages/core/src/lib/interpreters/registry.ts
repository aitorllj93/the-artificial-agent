import { Injectable, Logger } from '@nestjs/common';
import { Interpreter, InterpreterRunner } from './types';
import { AIInterpreterRunner } from './ai/interpreter';

@Injectable()
export class InterpreterRegistry {
  private readonly logger = new Logger(InterpreterRegistry.name);

  private readonly interpreters: Map<string, Interpreter> = new Map([
    ['ai', { name: 'ai', runner: this.aiMode }],
  ]);

  constructor(private aiMode: AIInterpreterRunner) {}

  public registerInterpreters(interpreters: Interpreter[]): void {
    interpreters.forEach((interpreter) =>
      this.registerInterpreter(interpreter)
    );
  }

  public registerInterpreter(params: Interpreter): void {
    this.interpreters.set(params.name, params);

    this.logger.log(
      `registered interpreter: ${params.name} with runner ${params.runner.constructor.name}`
    );
  }

  public getInterpreterNames(): string[] {
    return Array.from(this.interpreters.keys());
  }

  public getInterpreter(name: string): Interpreter | undefined {
    return this.interpreters.get(name);
  }

  public getInterpreterRunner(name: string): InterpreterRunner | undefined {
    return this.interpreters.get(name)?.runner;
  }
}
