import { Injectable, Logger } from '@nestjs/common';

import { Interpreter } from './types';
import { InterpreterRegistry } from './registry';

@Injectable()
export class InterpreterManager {
  private readonly logger = new Logger(InterpreterManager.name);

  private interpreter: Interpreter;

  constructor(private readonly interpreterRegistry: InterpreterRegistry) {}

  public setInterpreter(interpreterName: string): Interpreter {
    const interpreter =
      this.interpreterRegistry.getInterpreter(interpreterName);

    if (!interpreter) {
      throw new Error(`Interpreter ${interpreterName} not found`);
    }

    this.interpreter = interpreter;

    this.logger.log(`Switched to ${interpreter} mode`);

    return interpreter;
  }

  public getInterpreter(): Interpreter {
    if (!this.interpreter) {
      this.setInterpreter('ai');
    }

    return this.interpreter;
  }
}
