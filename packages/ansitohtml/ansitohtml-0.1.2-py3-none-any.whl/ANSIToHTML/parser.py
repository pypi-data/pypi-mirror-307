from re import compile, sub, finditer
from xml.etree.ElementTree import Element, SubElement, tostring
from logging import Logger
from typing import List, NamedTuple, Union, Literal
from dataclasses import dataclass
from ANSIToHTML.theme import DEFAULT


class MatchedChunk(NamedTuple):
    code: str
    start: int
    end: int


@dataclass
class Style:
    bold: bool = False
    italic: bool = False
    faint: bool = False
    underline: bool = False
    inverse: bool = False
    hidden: bool = False
    strikethrough: bool = False
    double_underline: bool = False
    foreground: Union[Literal[False], int] = False
    background: Union[Literal[False], int] = False


class Parser:
    color_8_to_16 = DEFAULT

    def __init__(self):
        self.consider = compile(
            r"(\033)\[(?P<code>\d+)"
        )
        self.logger = Logger("ansi-to-hml-parser")
        self.dom = Element("Article")
        self.style = Style()

    def clear_styles(self):
        del self.style
        self.style = Style()

    def update_styles(self, code: str):
        match code:
            # Code for Graphics Mode
            case "0":
                self.clear_styles()
            case "1":
                self.style.bold = True
            case "2":
                self.style.faint = True
            case "3":
                self.style.italic = True
            case "4":
                self.style.underline = True
            case "5":
                # blinking is not supported
                self.logger.warning("we are ignoring the command to blink")
            case "7":
                self.style.inverse = True
            case "8":
                self.style.hidden = True
            case "9":
                self.style.strikethrough = True
            case "21":
                self.style.double_underline = True
            # resetting graphics mode
            case "22":
                self.style.bold = False
                self.style.faint = False
            case "23":
                self.style.italic = False
            case "24":
                self.style.double_underline = False
                self.style.underline = False
            case "25":
                self.style.blinking = False
            case "27":
                self.style.inverse = False
            case "28":
                self.style.hidden = False
            case "29":
                self.style.strikethrough = False

            # resetting colors
            case "39":
                self.style.foreground = False
            case "49":
                self.style.background = False
            case _:
                if code.startswith("256f-"):
                    self.style.foreground = int(code.replace("256f-", ""))
                elif code.startswith("256b-"):
                    self.style.foreground = int(code.replace("256b-", ""))
                else:
                    possible_color = int(code)
                    if 37 >= possible_color >= 30 or 97 >= possible_color >= 90:
                        self.style.foreground = possible_color
                    elif 47 >= possible_color >= 40 or 107 >= possible_color >= 100:
                        self.style.background = possible_color

    def add_styles(self):
        style = []
        class_name = ["rem-ansi"]

        if self.style.bold:
            style.append('font-weight: bold')
            class_name.append("bold")
        if self.style.italic:
            style.append('font-style: italic')
            class_name.append("italic")
        if self.style.hidden:
            style.append('visibility: hidden')
            class_name.append("hidden")
        if self.style.underline:
            style.append('text-decoration: underline')
            class_name.append("underline")
        if self.style.strikethrough:
            style.append('text-decoration: line-through')
            class_name.append("strikethrough")
        if self.style.double_underline:
            style.append('text-decoration-line: underline; text-decoration-style: double')
            class_name.append("double_underline")
        if self.style.faint:
            style.append('opacity: 50%')
            class_name.append("faint")
        if self.style.foreground:
            color = self.color_8_to_16[self.style.foreground]
            style.append(f"color: {color}")
            class_name.append(f"foreground-{self.style.foreground}")
        if self.style.background:
            color = self.color_8_to_16[self.style.background]
            style.append(f"background-color: {color}")
            class_name.append(f"background-{self.style.background}")

        return "; ".join(style), "-".join(class_name)

    def add_to_dom(
            self, ansi_match: MatchedChunk,
            index: int, chunks: List[MatchedChunk],
            paragraph
    ):
        self.logger.info("Parsing %s", (ansi_match,))
        code = ansi_match.code

        if "38;5;" in code:
            code = sub(r"38;5;(\d+)", r"256f-\1", code)
        if "48;5;" in code:
            code = sub(r"48;5;(\d+)", r"256b-\1", code)

        for part in code.split(";"):
            self.update_styles(part)

        if len(chunks) > (index + 1) and ansi_match.end + 1 == chunks[index + 1].start:
            return

        styles, class_name = self.add_styles()
        sub_element = SubElement(
            self.dom, "span", style=styles, **{"class": class_name}
        )
        if index == (len(chunks) - 1):
            sub_element.text = paragraph[ansi_match.end + 1:]
        else:
            sub_element.text = paragraph[ansi_match.end + 1: chunks[index + 1].start]

    def parse(self, paragraph: str, append: bool = False):
        if not append:
            self.dom.clear()
            self.clear_styles()

        chunks: List[MatchedChunk] = []
        for found_match in finditer(self.consider, paragraph):
            chunks.append(
                MatchedChunk(found_match.group("code"), found_match.start(), found_match.end())
            )

        if not chunks:
            if not self.dom.text:
                self.dom.text = ""
            self.dom.text += paragraph

        for index, chunk in enumerate(chunks):
            self.add_to_dom(chunk, index, chunks, paragraph)

        return tostring(self.dom, encoding='unicode')


if __name__ == "__main__":
    message = "Hello there!"
    print(message)
    print(Parser().parse(
        message
    ))
