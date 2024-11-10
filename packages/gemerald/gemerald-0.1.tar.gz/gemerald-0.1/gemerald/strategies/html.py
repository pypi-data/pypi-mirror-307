from typing import override
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import LineElement, MarkdownElement, InlineElement
import gemerald.line_elements as le
import gemerald.inline_elements as ie

def get_element_text(element) -> str:
        if isinstance(element, LineElement) or element.is_complex:
            strategy = HTMLFormattingStrategy()
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
        return [f"<h1>{get_element_text(element)}</h1>"]


class Heading2(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h2>{get_element_text(element)}</h2>"]


class Heading3(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h3>{get_element_text(element)}</h3>"]


class Heading4(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h4>{get_element_text(element)}</h4>"]


class Heading5(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h5>{get_element_text(element)}</h5>"]


class Heading6(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h6>{get_element_text(element)}</h6>"]


class Paragraph(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<p>{get_element_text(element)}</p>"]


class Quote(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = [
            "<figure>",
            f"<cite>{get_element_text(element)}</cite>",
        ]
        assert isinstance(element, le.Quote)
        if element.author is not None:
            strs.append(f"<figcaption>{element.author}</figcaption>")
        strs.append("</figure>")
        return strs


class Link(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.Link)
        return [f"<a href={element.address}>{get_element_text(element)}</a><br/>"]

class Codeblock(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<pre><code>{get_element_text(element)}</code></pre>"]

class Bold(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<b>{get_element_text(element)}</b>"]

class Italics(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<i>{get_element_text(element)}</i>"]


def format_list_elements(points):
    strs = []
    for point in points:
        assert isinstance(point, le.OrderedPoint) or isinstance(point, le.UnorderedPoint)
        strs.append(f"<li>{get_element_text(point)}</li>")
    return strs


class UnorderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = ["<ul>"]
        assert isinstance(element, le.UnorderedList)
        strs += format_list_elements(element.content)
        strs.append("</ul>")
        return strs


class OrderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = ["<ol>"]
        assert isinstance(element, le.OrderedList)
        strs += format_list_elements(element.content)
        strs.append("</ol>")
        return strs


class HorizontalRule(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        _ = element
        return ["<hr>"]

class Text(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, ie.Text)
        return element.text_content

class PreformattedText(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, ie.PreformattedText)
        return element.text_content


class HTMLFormattingStrategy(FormattingStrategy):

    format_extension = "html"
    skip_index_in_path = "index.html"

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
        "Bold": Bold,
        "Italics": Italics,
        "Paragraph": Paragraph,
        "UnorderedList": UnorderedList,
        "OrderedList": OrderedList,
        "HorizontalRule": HorizontalRule,
        "Text": Text,
        "PreformattedText": PreformattedText,
    }
