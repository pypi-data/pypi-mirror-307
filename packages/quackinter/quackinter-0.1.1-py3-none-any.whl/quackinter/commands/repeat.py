from quackinter.commands.command import Command
from quackinter.errors import InterpretationSyntaxError
from quackinter.line import Line
from quackinter.stack import Stack
from quackinter.stack_context import StackContext


class RepeatCommand(Command):
    names = ["REPEAT"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        line = stack.context.get_line_offset(1)
        if line is None:
            raise InterpretationSyntaxError("There must be a line before repeat to run")

        extra_context = self._add_context(stack.context)

        new_stack = stack.new_stack()
        new_stack.run([line.line for line in [*extra_context, line]])

    def _add_context(self, context: StackContext):
        count = 2
        extra_context: list[Line] = []
        while True:
            possible_line = context.get_line_offset(count)
            if (
                possible_line is None
                or possible_line.command is None
                or not possible_line.command.include_with_repeat
            ):
                break
            extra_context.append(possible_line)
            count += 1
        return extra_context[::-1]
