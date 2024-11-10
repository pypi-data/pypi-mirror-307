from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quackinter.commands.command import Command


@dataclass
class Line:
    line: str
    line_index: int
    orig_line: str
    command: "Command | None" = None
