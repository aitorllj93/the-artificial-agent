import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
import { readFileSync } from 'node:fs';
import { format } from 'date-fns';

import { getHeadedSection, getNoteAST, insertIntoSection } from './ast';

@Injectable()
export class ObsidianAdapter {
  private readonly VAULT_DIR =
    this.config.get('providers.obsidian.vault') ||
    resolve(homedir(), 'Documents', 'My Knowledge Base');
  private readonly dailyNotesFormat =
    this.config.get('providers.obsidian.dailyNotes.format') || 'yyyy-MM-dd';

  private readonly dailyNoteAssistantSectionName =
    this.config.get('providers.obsidian.dailyNotes.headings.assistant') ||
    'Assistant';
  private readonly dailyNoteScheduleSectionName =
    this.config.get('providers.obsidian.dailyNotes.headings.schedule') ||
    'Schedule';

  private readonly dailyNotesSettings = JSON.parse(
    readFileSync(
      resolve(this.VAULT_DIR, '.obsidian', 'daily-notes.json'),
      'utf-8'
    )
  );

  constructor(private config: ConfigService) {}

  async getDailyNote() {
    const date = new Date();

    const dailyNoteName = `${format(date, this.dailyNotesFormat)}.md`;

    const dailyNotePath = resolve(
      this.VAULT_DIR,
      this.dailyNotesSettings.folder || '',
      dailyNoteName
    );

    const dailyNoteExists = readFileSync(dailyNotePath, 'utf-8');

    if (!dailyNoteExists) {
      throw new Error('Daily note does not exist');
    }

    const ast = await getNoteAST(dailyNotePath);

    return {
      ast,
      dailyNoteName,
      dailyNotePath,
    };
  }

  async getDailyNoteAssistantSection() {
    const dailyNote = await this.getDailyNote();

    const assistantSection = getHeadedSection(
      this.dailyNoteAssistantSectionName,
      dailyNote.ast
    );

    return assistantSection;
  }

  async getDailyNoteSchedule() {
    const dailyNote = await this.getDailyNote();

    const { sectionContent, sectionHeading } = getHeadedSection(
      this.dailyNoteScheduleSectionName,
      dailyNote.ast
    );

    const [morningRoutineCallout, eveningRoutineCallout, list, list2] =
      sectionContent;

    return sectionContent;
  }

  async insertAssistantContent(content: string) {
    const dailyNote = await this.getDailyNote();

    await insertIntoSection(
      dailyNote.dailyNotePath,
      this.dailyNoteAssistantSectionName,
      content
    );
  }
}
