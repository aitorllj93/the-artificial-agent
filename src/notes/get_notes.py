
from datetime import datetime
from typing import List
from core.config import get_value
from notes.note import Note

vaultFolder = get_value('providers.obsidian.vault', None)
dailyNotesFolder = get_value('providers.obsidian.dailyNotes.folder', 'Journal')
dailyNotesFormat = get_value(
    'providers.obsidian.dailyNotes.format', '%Y-%m-%d')
bibliographyNotesFolder = get_value(
    'providers.obsidian.bibliography.folder', 'Bibliography')


async def get_notes_recursive(folder: str, notes: List[Note]) -> List[Note]:
    for f in folder.iterdir():
        if f.is_dir():
            await get_notes_recursive(f, notes)
        elif f.is_file():
            notes.append(Note(f))
    return notes


async def get_notes(path: str = None) -> List[Note]:
    notes = []
    if path is None:
        path = vaultFolder
    else:
        path = f'{vaultFolder}/{path}'
    await get_notes_recursive(path, notes)
    return notes


async def get_daily_notes() -> List[Note]:
    return await get_notes(dailyNotesFolder)


async def get_bibliography_notes() -> List[Note]:
    return await get_notes(bibliographyNotesFolder)


async def get_today_daily_note() -> Note:
    todayDailyNoteFile = datetime.now().strftime(dailyNotesFormat) + '.md'
    todayNote = Note(f'{vaultFolder}/{dailyNotesFolder}/{todayDailyNoteFile}')
    return todayNote


async def get_today_daily_note_content() -> str:
    todayNote = await get_today_daily_note()
    return todayNote.content


async def get_note_section(note: Note, section: str) -> str:
    noteContent = note.content
    noteSections = noteContent.split('## ')
    for noteSection in noteSections:
        if noteSection.startswith(section):
            return noteSection

    with open(note, 'a') as f:
        note.append(f'## {section}\n')

    return f'## {section}\n'


async def get_note_section_end_line(note: Note, section: str) -> int:
    """Get the line number of the end of a section in a note."""
    noteContent = note.content
    noteSections = noteContent.split('## ')
    for noteSection in noteSections:
        if noteSection.startswith(section):
            return noteSections.index(noteSection) + 1

    with open(note, 'a') as f:
        note.append(f'## {section}\n')

    return noteSections.index(f'## {section}\n') + 1
