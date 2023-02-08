import { Injectable, Logger } from '@nestjs/common';
import { Personality } from './types';

@Injectable()
export class PersonalityRegistry {
  private readonly logger = new Logger(PersonalityRegistry.name);

  private readonly personalities: Map<string, Personality> = new Map([]);
  private defaultPersonality: Personality | undefined;

  public registerPersonalities(personalities: Personality[]): void {
    personalities.forEach((personality) =>
      this.registerPersonality(personality)
    );
  }

  public registerPersonality(params: Personality): void {
    this.personalities.set(params.name, params);

    this.logger.log(`registered personality: ${params.name}`);

    if (params.isDefault || this.personalities.size === 1) {
      this.defaultPersonality = params;
      this.logger.log(`default personality: ${params.name}`);
    }
  }

  public getPersonalityNames(): string[] {
    return Array.from(this.personalities.keys());
  }

  public getPersonality(name?: string): Personality | undefined {
    if (!name) return this.getDefaultPersonality();

    return this.personalities.get(name) || this.getDefaultPersonality();
  }

  public getPersonalityPrompt(name?: string): string | undefined {
    if (!name) return this.getDefaultPersonalityPrompt();
    return (
      this.personalities.get(name)?.prompt || this.getDefaultPersonalityPrompt()
    );
  }

  public getDefaultPersonality(): Personality | undefined {
    return this.defaultPersonality;
  }

  public getDefaultPersonalityPrompt(): string | undefined {
    return this.defaultPersonality?.prompt;
  }
}
