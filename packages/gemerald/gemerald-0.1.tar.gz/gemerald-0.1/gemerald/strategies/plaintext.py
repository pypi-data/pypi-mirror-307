from typing import override, Type
from textwrap import wrap
from gemerald.elements import InlineElement
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import LineElement, MarkdownElement, InlineElement
from gemerald.line_elements import AbstractHeading, Heading1, Heading2

def get_element_text(element: MarkdownElement) -> str:
        if isinstance(element, LineElement) or element.is_complex:
            strategy = PlaintextStrategy()
            strs = []
            for e in element.content:
                formatter = strategy.find_formatter(e)()
                strs += formatter.format(e)
            return " ".join(strs)
        else:
            assert isinstance(element, InlineElement)
            return " ".join(element.text_content)

class TextFormatter(ElementFormatter):

    def wrap_lines_to_80(self, lines: list[str]) -> list[str]:
        wrapped = []
        for line in lines:
            wrapped += wrap(line, 80)
        wrapped += [""]
        return wrapped

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return self.wrap_lines_to_80([get_element_text(element)])


class HeadingTextFormatter(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, AbstractHeading)
        heading: AbstractHeading = element
        text = " ".join(heading.content[0].text_content)

        if not isinstance(element, Heading1) and not isinstance(element, Heading2):
            return ["", text, ""]

        underline = "=" if isinstance(element, Heading1) else "-"

        return ["", text, underline*len(text), ""]

class PlaintextStrategy(FormattingStrategy):

    format_extension = "txt"
    skip_index_in_path = None

    @classmethod
    def find_formatter(cls, element) -> Type[ElementFormatter]:
        if isinstance(element, AbstractHeading):
            return HeadingTextFormatter
        else:
            return TextFormatter
