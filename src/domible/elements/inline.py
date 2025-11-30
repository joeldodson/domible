"""  domible/src/domible/elements/inline.py 
"""
from typing import Dict, Any

from domible.elements.baseElements import BaseElement


class Anchor(BaseElement):
    def __init__(self, href: str, contents: Any = None, **kwArgs):
        self.href = href
        super().__init__(tag="a", contents=contents, href=self.href, **kwArgs)


class Code(BaseElement):
    """create a code element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="code", contents=contents, **kwArgs)


class Div(BaseElement):
    """create a div element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="div", contents=contents, **kwArgs)


class Paragraph(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="p", contents=contents, **kwArgs)


class Pre(BaseElement):
    """create a pre element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="pre", contents=contents, **kwArgs)


class Span(BaseElement):
    """create a span element
    use for wrapping a single content .
    For multiple elements, use a div.
    """

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="span", contents=contents, **kwArgs)


class Summary(BaseElement):
    """create a Summary element
    used within a details element to provide a label for a collapseable widget.
    For accessibility, requiring some content be provided
    """

    def __init__(self, contents: Any, **kwArgs):
        if not contents:
            raise ValueError("Summary element must have some contents")
        super().__init__(tag="summary", contents=contents, **kwArgs)


class Details(BaseElement):
    """create a details element
    used to create a collapseable widget.
    For accessibility, requiring a summary element be provided
    """

    def __init__(self, summary: Summary,  contents: Any = None, **kwArgs):
        if not summary or not isinstance(summary, Summary):
            raise ValueError("Details element must contain a Summary element")
        if isinstance(contents, list): 
            contents.insert(0, summary)
        else:
            contents  = [summary] + [contents] if contents else summary
        super().__init__(tag="details", contents=contents, **kwArgs)


## end of file
