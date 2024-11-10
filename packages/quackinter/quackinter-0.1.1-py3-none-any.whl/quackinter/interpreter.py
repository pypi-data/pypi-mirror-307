from time import sleep

from quackinter.commands.command import Command
from quackinter.config import Config
from quackinter.commands import command_list as built_in_ducky_commands
from quackinter.environment import Environment
from quackinter.stack import Stack


class Interpreter:
    def __init__(
        self,
        extended_commands: list[type[Command]] | None = None,
        include_builtins: bool = True,
        config: Config | None = None,
    ) -> None:
        self.extended_commands = extended_commands or []
        self.commands = [*self.extended_commands]
        if include_builtins:
            self.commands.extend(built_in_ducky_commands)
        self.config = Config() if not config else config

    def interpret_text(self, text: str):
        new_ducky = text.split("\n")
        self._interpret(new_ducky)

    def _interpret(self, lines: list[str]):
        sleep(self.config.delay / 1000)
        with Environment.create_global(self.commands, self.config) as global_env:
            stack = Stack(global_env)
            stack.run(lines)
