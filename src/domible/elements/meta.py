""" domible/src/domible/elements/meta.py 

the meta tags, e.g., meta  :)
and others, e.g., title, link, base, style, script  
"""

from typing import Any

from .baseElements import BaseElement, BaseVoidElement


class Meta(BaseVoidElement):
    """ generates the meta voide element """

    def __init__(self, **kwArgs):
        """ meta is a void element, no contents are allowed """
        super().__init__(tag="meta", **kwArgs)


class Title(BaseElement):
    """ Create a Title element
    Titles can only contain strings of text (per spec).
    This is enforced in this class.
    """

    def __init__(self, contents: str, **kwArgs):
        if not isinstance(contents, str):
            raise TypeError("Title contents must be a string")
        self.titleStr = contents
        super().__init__(tag='title', contents=self.titleStr, **kwArgs)


    def setTitle(self, title: str) -> None:
        """ set the value, must be a string, for the Title. """
        self.addContent(title)


    def addContent(self, content: Any, front: bool = False) -> None:
        """ 
        <title> can only have a string that is the title  
        and it might have already been set at creation time.
        If the new content is a string, 
        overrite any existing title 
        """
        if not isinstance(content, str):
            raise TypeError("Title contents must be a string")
        self.titleStr = content
        self.contents = []
        super().addContent(content)


# end of file
