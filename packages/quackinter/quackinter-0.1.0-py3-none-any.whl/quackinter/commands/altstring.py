from typing import TypedDict
from quackinter.commands.command import Command
from quackinter.errors import InvalidArgError
from quackinter.key_injector import KeyInjector
from quackinter.stack import Stack


class Encoding(TypedDict):
    name: str
    zero_fill: bool


encodings: list[Encoding] = [
    {"name": "CP437", "zero_fill": False},
    {"name": "CP850", "zero_fill": False},
    {"name": "CP1252", "zero_fill": True},
]


class AltStringCommand(Command):
    names = ["ALTSTRING", "ALT_STRING", "ALTCODE", "ALT_CODE"]

    @classmethod
    def convert_char(cls, char: str) -> str:
        for enc in encodings:
            try:
                encoded = str(ord(char.encode(enc["name"])))
                if enc["zero_fill"]:
                    encoded = encoded.zfill(4)
                return encoded
            except UnicodeEncodeError:
                pass
        raise InvalidArgError(f"{char} cannot be converted to an alt code.")

    @classmethod
    def convert_text(cls, text: str) -> list[str]:
        return [cls.convert_char(char) for char in text]

    @classmethod
    def type_code(cls, code: str, injector: KeyInjector):
        with injector.hold("alt"):
            for num in code:
                injector.press(f"num{num}")

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        codes = self.convert_text(data)
        injector = KeyInjector(stack.environment)
        for code in codes:
            self.type_code(code, injector)
