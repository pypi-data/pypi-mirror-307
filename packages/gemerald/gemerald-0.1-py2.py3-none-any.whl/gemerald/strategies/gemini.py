from typing import override
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import LineElement, MarkdownElement, InlineElement
import gemerald.line_elements as le
import gemerald.inline_elements as ie

def get_element_text(element) -> str:
        if isinstance(element, LineElement) or element.is_complex:
            strategy = GeminiStrategy()
            strs = []
            for e in element.content:
                formatter = strategy.find_formatter(e)()
                strs += formatter.format(e)
            return "".join(strs)
        else:
            assert isinstance(element, InlineElement)
            return "".join(element.text_content)


class Heading1(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"# {get_element_text(element)}"]

class Heading2(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"## {get_element_text(element)}"]

class Heading3(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"### {get_element_text(element)}"]

class Heading4(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"#### {get_element_text(element)}"]

class Heading5(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"##### {get_element_text(element)}"]

class Heading6(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"###### {get_element_text(element)}"]

class Quote(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"> {get_element_text(element)}", ""]

class PreformattedText(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [
            f"`{get_element_text(element)}`",
        ]

class Codeblock(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [
            "```",
            f"{get_element_text(element)}",
            "```",
            ""
        ]

class Text(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"{get_element_text(element)}"]

class Paragraph(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f" {get_element_text(element)}", ""]

class Link(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.Link)
        return [f"=> {element.address} {get_element_text(element)}"]

class UnorderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.UnorderedList)
        return [f"* {get_element_text(it)}" for it in element.content]

class OrderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.OrderedList)
        return [f"{k}) {get_element_text(it)}" for k,it in enumerate(element.content)]

class GeminiStrategy(FormattingStrategy):

    format_extension = "gmi"
    skip_index_in_path = "index.gmi"

    formatters = {
        "Heading1": Heading1,
        "Heading2": Heading2,
        "Heading3": Heading3,
        "Heading4": Heading4,
        "Heading5": Heading5,
        "Heading6": Heading6,
        "Quote": Quote,
        "Link": Link,
        "Codeblock": Codeblock,
        "Bold": Text,
        "Italics": Text,
        "Paragraph": Paragraph,
        "UnorderedList": UnorderedList,
        "OrderedList": OrderedList,
        "HorizontalRule": Text,
        "Text": Text,
        "PreformattedText": PreformattedText,
    }

