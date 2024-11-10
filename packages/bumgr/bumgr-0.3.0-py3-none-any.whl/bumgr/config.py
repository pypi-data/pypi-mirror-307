import os
from abc import ABC, abstractmethod
from collections import deque
from pathlib import Path

from rich.abc import RichRenderable
from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich.text import Text


class ConfigError(ValueError, RichRenderable):
    def __init__(self, message: tuple[str, str] | list[tuple[str, str]]):
        if not isinstance(message, list):
            message = [message]
        super().__init__(message)
        self.errors = message

    def __rich__(self):
        error_grid = Table.grid(
            padding=(0, 2), pad_edge=False, collapse_padding=True, expand=False
        )
        error_grid.add_column()
        error_grid.add_column()
        for field, error in self.errors:
            error_grid.add_row(Text(field, style="yellow"), error)
        return error_grid


class Configurable(ABC):
    """Configurable classes are classes that implement the method
    classmethod :meth:`.check_config`. It is used to check for errors
    in the configuration, like mutually exclusive attributes.
    """

    @classmethod
    @abstractmethod
    def check_config(cls, config: dict, **kwargs) -> None:
        """Check the configuration for errors.
        Raises :class:`ConfigError` if any errors are found.
        """
        raise NotImplementedError(
            "Configurable classes must implement the 'check_config' method"
        )


def handle_config_error(context: str, error: ConfigError, console: Console) -> None:
    console.print(f"[red]Config error in [underline]{context}[/underline]:[/red]")
    console.print(Padding(error, (1, 4)))


def get_config(config: str | None = None) -> Path:
    if config:
        path = Path(config)
        if path.is_file():
            return path
        else:
            raise FileNotFoundError(f"Config file '{config}' not found")
    checked_paths: list[str] = []
    testpaths = deque(["/etc/bumgr/config.toml", "./bumgr.toml"])
    if "XDG_CONFIG_HOME" in os.environ:
        testpaths.appendleft(os.path.expandvars("$XDG_CONFIG_HOME/bumgr/config.toml"))
    else:
        testpaths.appendleft(os.path.expanduser("~/.config/bumgr/config.toml"))
    while len(testpaths) > 0:
        path = Path(testpaths.popleft())
        if path.is_file():
            return path
        checked_paths.append(str(path))
    raise FileNotFoundError(f"No config file found in {', '.join(checked_paths)}")
