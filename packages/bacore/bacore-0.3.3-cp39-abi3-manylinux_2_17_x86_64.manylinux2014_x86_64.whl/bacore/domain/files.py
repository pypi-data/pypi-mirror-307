"""Module domain files for handling of files and directories."""

import toml
from pathlib import Path


class MarkdownFile:
    """Markdown file."""

    def __init__(self, path: Path, skip_title: bool):
        if path.suffix not in [".md", ".markdown"]:
            raise ValueError("File should be in markdown format")
        self.path = path
        self.skip_title = skip_title

    def read(self) -> str:
        """Read file.

        Parameters:
            `file`: File path
            `skip_title`: Will skip the first line of the markdown file if it starts with the '#' character. Will also
                          try to remove any newline characters which remains after the title has been removed.

        Returns:
            String of complete text or the text without the title.
        """
        try:
            text = self.path.read_text()
        except OSError as e:
            raise OSError(f"Error reading file {self.path}: {e.strerror}") from e

        title, body = text.split("\n", 1)
        if self.skip_title and title.strip().startswith("#"):
            return body.lstrip()
        else:
            return text


class TOML:
    """TOML file class."""

    def __init__(self, path: Path):
        """Initialize."""
        self.path = path

    @property
    def path(self):
        """Get file path."""
        return self._path

    @path.setter
    def path(self, value):
        """Set file path as pathlib.Path object."""
        if not isinstance(value, Path):
            raise TypeError("Path must be a pathlib.Path object.")
        self._path = value

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        with open(self.path, mode="r") as file:
            content = toml.load(file)
        return content
