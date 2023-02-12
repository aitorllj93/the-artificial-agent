"""Note objects."""

import re
from pathlib import Path
from typing import Callable, List, Union
from notes.task import Task

DEFAULT_SECTION_INDICATORS = '##'


class Note:

    def __init__(self, path: Union[Path, str], content: str = None):
        self.path: Path = Path(path)
        if self.path.is_file():
            with open(self.path, "r") as f:
                self.content: str = f.read()
        else:
            with open(self.path, 'w') as f:
                f.write(content)
                self.content: str = content

    def __repr__(self) -> str:
        return f'Note (path: "{self.path}")\n'

    def append(self, str_append: str, allow_repeat: bool = False):
        """Appends text to the note content.

        Args:
            str_append: string to append to the note content.
            allow_repeat: Add the string if it is already present in the note content.
        """
        if allow_repeat:
            self.content += f"\n{str_append}"
        else:
            if len(re.findall(re.escape(str_append), self.content)) == 0:
                self.content += f"\n{str_append}"
        self.write()

    def append_to_section(self, section: str, str_append: str, allow_repeat: bool = False, section_indicators: str = DEFAULT_SECTION_INDICATORS, end_indicators: str = None):
        """Appends text to a section of the note.

        Args:
            section: section to append to.
            str_append: string to append to the note content.
            allow_repeat: Add the string if it is already present in the note content.
        """
        # if allow_repeat is False:
        # avoid including line if there's alredy a line with exactly the same content

        section_start_line = self.get_section_start_line(
            section, section_indicators)

        if section_start_line is None:
            self.append(f'{section_indicators} {section}\n\n{str_append}')
            return

        section_end_line = self.get_section_end_line(
            section, section_indicators, end_indicators)

        if section_end_line is None:
            self.append(str_append)
            return

        with open(self.path, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i == section_end_line:
                    lines.insert(i, f"{str_append}\n")
            f.seek(0)
            for line in lines:
                f.write(line)
            self.content = f.read()

    def print(self):
        """Prints the note content to the screen."""
        print(self.content)

    def sub(self, pattern: str, replace: str, is_regex: bool = False):
        """Substitutes text within the note.

        Args:
            pattern:
                the pattern to replace (plain text or regular expression)
            replace:
                what to replace the pattern with
            is_regex:
                Whether the pattern is a regex pattern or plain text.
        """
        if not is_regex:
            pattern = re.escape(pattern)
        self.content = re.sub(pattern, replace, self.content)

    def update_content(
        self,
        inline_position: str = "bottom",
        inline_inplace: bool = True,
        inline_tml: Union[str, Callable] = "standard",  # type: ignore
        write: bool = False,
    ):
        """Updates the note's content.

        Args:
            inline_position:
                if "bottom" / "top", inline metadata is grouped at the bottom/top of the note.
                This is always the case for new inline metadata (that didn't exist in the
                previous note content).
            inline_inplace:
                By default it is True, which means the inline metadata position in the note
                is not modified. If False, the metadata is grouped according to `inline_how`
            inline_tml:
                Which template to use to update inline metadata content.
                Current possible values: ["standard", "callout"]
                Defaults to "standard": each metadata field is written on a newline.
                "callout": metadata fields are regrouped inside a callout:
                    > [!info]- metadata
                    > key1 :: values1
                    > key2 :: values2
                    ...
                NOTE: In later updates it will be possible to pass a function specifying how
                to display the metadata, for greater customization.
            write:
                Write changes to the file on disk after updating the content.
                If write = False, the user needs to call Note.write() subsequently to write
                changes to disk, otherwise only the self.content attribute is modified
                (in memory, but not on disk).
        """

        self.content = self.metadata._update_content(
            self.content,
            inline_position=inline_position,
            inline_inplace=inline_inplace,
            inline_tml=inline_tml,
        )
        if write:
            self.write()

    def write(self, path: Union[Path, None] = None):
        """Writes the note's content to disk.

        Args:
            path:
                path to the note. If None, overwrites the current note content.
        """
        p = self.path if path is None else path
        with open(p, "w") as f:
            f.write(self.content)

    def get_section(self, section: str, indicators: str = DEFAULT_SECTION_INDICATORS, end_indicators: str = None) -> str:
        """Returns a heading section of the note. If the section is not found, creates it.

        Args:
            section: section to return.
        """
        section_start_line = self.get_section_start_line(section, indicators)
        section_end_line = self.get_section_end_line(
            section, indicators, end_indicators)

        section_content = self.content.splitlines(
        )[section_start_line:section_end_line]

        return '\n'.join(section_content)

    def get_section_start_line(self, section: str, indicators: str = DEFAULT_SECTION_INDICATORS) -> int:
        """Returns the line number of the start of the section.

        Args:
            section: section to return.
        """
        for i, line in enumerate(self.content.splitlines()):
            if line.startswith(f"{indicators} {section}"):
                return i

    def get_section_end_line(self, section: str, indicators: str = DEFAULT_SECTION_INDICATORS, end_indicators: str = None) -> int:
        """Returns the line number of the end of the section.

        Args:
            section: section to return.
        """
        if (end_indicators is None):
            end_indicators = indicators
        end_indicators_list = end_indicators.split()
        inSection = False
        for i, line in enumerate(self.content.splitlines()):
            if line.startswith(f"{indicators} {section}"):
                inSection = True
            elif inSection and any(line.startswith(f"{end_indicator} ") for end_indicator in end_indicators_list):
                return i - 1

    def add_task_to_section(self, section: str, task: Task, indicators: str = DEFAULT_SECTION_INDICATORS):
        """Adds a task to the note.

        Args:
            task: task to add.
        """
        self.append_to_section(section, task, indicators)

    def complete_task(self, task: Task):
        """Completes a task in the note.

        Args:
            task: task to complete.
        """
        taskMd = task.to_markdown()
        completedTaskMd = taskMd.replace("- [ ]", "- [x]")
        self.sub(taskMd, completedTaskMd)
        self.write()

    def list_tasks(self, showCompletedTasks=False) -> List[Task]:
        """Lists all tasks in the note.

        Args:
            showCompletedTasks: whether to show completed tasks or not.
        """

        tasks = re.findall(r"^- \[.\] .*$", self.content, re.MULTILINE)

        if not showCompletedTasks:
            tasks = filter(lambda t: t.startswith("- [ ]"), tasks)

        return map(
            lambda t: self.line_to_task(t),
            tasks,
        )

    def list_tasks_from_section(self, section: str, showCompletedTasks=False) -> List[Task]:
        """Lists all tasks in a section.

        Args:
            section: section to list tasks from.
        """
        section_content = self.get_section(section)

        tasks = re.findall(r"^- \[.\] .*$", section_content, re.MULTILINE)

        if not showCompletedTasks:
            tasks = filter(lambda t: t.startswith("- [ ]"), tasks)

        return map(lambda t: self.line_to_task(t), tasks)

    def line_to_task(self, line: str) -> Task:
        """Converts a line to a task.

        Args:
            line: line to convert.
        """
        return Task().from_md(self.get_section(line[2:], indicators='-', end_indicators="## ### -") or line)

    def add_link_to_section(self, section: str, link: str):
        """Adds a link to the note.

        Args:
            link: link to add.
        """
        self.append_to_section(section, link)

    @staticmethod
    def _is_md_file(path: Path):
        exist = path.exists()
        is_md = path.suffix == ".md"
        return exist and is_md
