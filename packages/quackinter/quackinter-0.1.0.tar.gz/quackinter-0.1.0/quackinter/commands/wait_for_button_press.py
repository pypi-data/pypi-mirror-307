from quackinter.commands.command import Command
from quackinter.stack import Stack

from pymsgbox import alert


class WaitForButtonPressCommand(Command):
    names = ["WAITFORBUTTONPRESS", "WAIT_FOR_BUTTON_PRESS"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        alert(data.strip(), button="CONTINUE")
