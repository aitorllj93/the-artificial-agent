import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as schedule from 'node-schedule';

import { TelegramBotAdapter } from './adapters/telegram-bot.adapter';
import { OpenAIAdapter } from './adapters/openai.adapter';

import { History } from './history';
import { CommandRegistry } from './registry';

@Injectable()
export class Scheduler {
  private readonly SCHEDULE_DEFAULT_TZ =
    this.config.get('common.timezone') || 'Europe/Madrid';

  private readonly logger = new Logger(Scheduler.name);

  constructor(
    private readonly config: ConfigService,
    private readonly botAdapter: TelegramBotAdapter,
    private readonly aiAdapter: OpenAIAdapter,
    private readonly history: History,
    private readonly registry: CommandRegistry
  ) {}

  generateRecurrenceRule({
    year,
    month,
    date,
    dayOfWeek,
    hour,
    minute,
    second,
    tz = this.SCHEDULE_DEFAULT_TZ,
  }: {
    year?: number;
    month?: number;
    date?: number;
    dayOfWeek?: number;
    hour?: number;
    minute?: number;
    second?: number;
    tz?: string;
  }) {
    return new schedule.RecurrenceRule(
      year,
      month,
      date,
      dayOfWeek,
      hour,
      minute,
      second,
      tz
    );
  }

  resolveRecurrenceRule(rule: RecurrenceRuleAlike): schedule.RecurrenceRule {
    return rule instanceof schedule.RecurrenceRule
      ? rule
      : this.generateRecurrenceRule(rule);
  }

  scheduleCommands(
    commands: {
      rule: RecurrenceRuleAlike;
      command: string;
      params?: any;
      onExecute?: () => void;
    }[]
  ): schedule.Job[] {
    return commands.map((command) => this.scheduleCommand(command));
  }

  scheduleCommand({
    rule,
    command,
    params,
    onExecute,
  }: {
    rule: RecurrenceRuleAlike;
    command: string;
    params?: any;
    onExecute?: () => void;
  }) {
    const commandDef = this.registry.getCommand(command);
    const recurrenceRule = this.resolveRecurrenceRule(rule);

    this.logger.log(`scheduled command ${command} for ${JSON.stringify(rule)}`);

    return schedule.scheduleJob(recurrenceRule, async () => {
      await commandDef.handler.handle(params, null, commandDef);

      if (onExecute) {
        onExecute();
      }
    });
  }

  schedulePrompts(
    prompts: {
      rule: RecurrenceRuleAlike;
      prompt: Promptable;
      onExecute?: (text: string) => void;
    }[]
  ): schedule.Job[] {
    return prompts.map((prompt) => this.schedulePrompt(prompt));
  }

  schedulePrompt({
    rule,
    prompt,
    onExecute,
  }: {
    rule: RecurrenceRuleAlike;
    prompt: Promptable;
    onExecute?: (text: string) => void;
  }): schedule.Job {
    return schedule.scheduleJob(this.resolveRecurrenceRule(rule), async () => {
      const promptText = typeof prompt === 'string' ? prompt : prompt();
      const text = await this.aiAdapter.generateTextFromPrompt(promptText);

      this.history.storeMessage({
        text,
        author: 'You',
        time: Date.now(),
      });

      this.botAdapter.sendTextMessage(text);

      if (onExecute) {
        onExecute(text);
      }
    });
  }
}

export type RecurrenceRuleProps = {
  year?: number;
  month?: number;
  date?: number;
  dayOfWeek?: number;
  hour?: number;
  minute?: number;
  second?: number;
  tz?: string;
};

export type RecurrenceRuleAlike = schedule.RecurrenceRule | RecurrenceRuleProps;
export type Promptable = string | (() => string);

export type JSONScheduleable = {
  rule: RecurrenceRuleAlike;
  command: string;
  params?: any;
};
