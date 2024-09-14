""" domible/src/domible/elements/sectioning.py 
"""

from typing import Any
from domible.elements.baseElements import BaseElement, BaseVoidElement


class Article(BaseElement):
    """create <article> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="article", contents=contents, **kwArgs)


class Body(BaseElement):
    """create <body> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="body", contents=contents, **kwArgs)


class Footer(BaseElement):
    """create <footer> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="footer", contents=contents, **kwArgs)


class Header(BaseElement):
    """create <header> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="header", contents=contents, **kwArgs)


class Heading(BaseElement):
    """create heading (<h1, ..., h6>) element."""

    def __init__(self, level: int, contents: Any = None, **kwArgs):
        self.level = level
        super().__init__(tag=f"h{level}", contents=contents, **kwArgs)


class HorizontalRule(BaseVoidElement):
    """generates the hr voide element"""

    def __init__(self, **kwArgs):
        """hris a void element, no contents are allowed"""
        super().__init__(tag="hr", **kwArgs)


class Main(BaseElement):
    """create <main> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="main", contents=contents, **kwArgs)


class Nav(BaseElement):
    """
    create a <nav> element
    For accessibility, require a label which will be used to set an aria-label attribute.
    This will result in a meaningful announcement when navigating by landmarks (and other scenarios). 
    """

    def __init__(self, label: str, contents: Any = None, **kwArgs):
        self.label = label
        super().__init__(tag="nav", contents=contents, **{"aria-label": self.label}, **kwArgs)


class Section(BaseElement):
    """create <section> element"""

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="section", contents=contents, **kwArgs)


## end of file
