"""  domible/src/domible/elements/inline.py 
"""
from typing import Dict, Any

from domible.elements.baseElements import BaseElement


class Anchor(BaseElement):
    def __init__(self, href: str, contents: Any = None, **kwArgs):
        self.href = href
        super().__init__(tag="a", contents=contents, href=self.href, **kwArgs)


class Div(BaseElement):
    """create a div element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="div", contents=contents, **kwArgs)


#######
class Paragraph(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="p", contents=contents, **kwArgs)


#######
class Span(BaseElement):
    """create a span element
    use for wrapping a single content .
    For multiple elements, use a div.
    """

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="span", contents=contents, **kwArgs)


## end of file
