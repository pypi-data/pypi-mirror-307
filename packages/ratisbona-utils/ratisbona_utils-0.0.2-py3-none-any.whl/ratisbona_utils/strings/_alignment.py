from enum import Enum, auto


class Alignment(Enum):
    """
    Base class for enums.
    """
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()
    BLOCK = auto()


ALIGNMENT_FUNCTIONS={
    Alignment.LEFT: str.ljust,
    Alignment.RIGHT: str.rjust,
    Alignment.CENTER: str.center,
    Alignment.BLOCK: lambda text, width: text,
}


def align(text: str, width=80, alignment=Alignment.LEFT) -> str:
    """
    Align text in a given width.

    Args:
        text: The text to align.
        width: The width to align the text in.
        alignment: The alignment to use.

    Returns:
        str, the aligned text.
    """
    return ALIGNMENT_FUNCTIONS[alignment](text, width)


def longest_line(multiline_text: str) -> int:
    return max(len(line) for line in multiline_text.splitlines())