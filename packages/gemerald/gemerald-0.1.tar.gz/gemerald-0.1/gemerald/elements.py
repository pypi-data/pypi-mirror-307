from abc import abstractmethod, ABC
from typing import Callable, Optional, TYPE_CHECKING

class ParseException(BaseException): pass

# Class hierarchy for elements:
#
#           MarkdownElement
#           /             \ 
#       LineElement    InlineElement

class MarkdownElement(ABC):
    """
        Representation of a markdown-specific element
        like heading (##) or a preformatted text (`).
    """
    is_complex = False

    def format(self, strategy: "FormattingStrategy") -> list[str]:
        formatter = strategy.find_formatter(self)()
        return formatter.format(self)


class LineElement(MarkdownElement, ABC):
    """
        A Markdown element that takes at least one line in a markdown file.
        It is only capable of holding other MarkdownElements. It cannot hold raw data.
    """

    is_greedy: bool = False
    is_single_line: bool
    is_terminated_with_blank_line: bool
    termination_sequence: Optional[str]
    termination_func: Optional[Callable]

    @abstractmethod
    def __init__(self, content: list[str]):
        self.content: list[MarkdownElement] = []

    @staticmethod
    @abstractmethod
    def could_begin_with(line) -> bool: pass


class InlineElement(MarkdownElement, ABC):
    """
        A Markdown element that can hold raw text. For example bold text or a plain text.
        It is not a direct element of a markdown file. It can only exist as a child of another
        element.
    """
    beginning_symbol = Optional[str]

    def __init__(self, parent: MarkdownElement, content: str):
        self.content = content
        self.parent = parent
        self.elements: list[InlineElement] = []
        self.raw_len = 0

    @property
    def text_content(self) -> list[str]:
        return [self.content]


if TYPE_CHECKING:
    from gemerald.formatter import FormattingStrategy
