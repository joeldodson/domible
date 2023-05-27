""" domible/src/domible/elements/scripting.py
"""

from typing import Any

from domible.elements.baseElements import BaseElement


class Canvas(BaseElement):
    """
    create a <canvas> element
    All I know of the <canvas> element is it's a problem for accessibility.
    As I learn more, I might build out this class to enforce as much accessibility as possible in a <canvas>.
    """

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="canvas", **kwArgs)


class NoScript(BaseElement):
    """
    create a <noscript> element
    I guess this is like a <div> that can contain general HTML
    to be rendered if the rowser doesn't support the desired scripting.
    """

    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="noscript", **kwArgs)


class Script(BaseElement):
    """
    create a <script> element
    domible doesn't know anything about scripts.
    This class exists for the domible user to add scripts to their HTML.
    The content should be a string of valid text (probably JS) given the attributes of the element.
    """

    def __init__(self, contents: str, **kwArgs):
        super().__init__(tag="script", **kwArgs)


## end of file
