""" domible/src/domible/elements/meta.py 

the meta tags, e.g., meta  :)
and others, e.g., title, link, base, style, script  
"""

from typing import Any

from .baseElements import BaseElement, BaseVoidElement


class Base(BaseVoidElement):
    """ generates the base voide element """

    def __init__(self, **kwArgs):
        """ base is a void element, no contents are allowed """
        super().__init__(tag="base", **kwArgs)


class Head(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        """ 
        tried having a constructor argument for a title with a default string.
        Turned in to a pain considering a Title object could be in the contents.
        Leaving it up to a document builder to handle a title string argument.  
        """
        super().__init__(tag="head", contents=contents, **kwArgs)


class Meta(BaseVoidElement):
    """ generates the meta voide element """

    def __init__(self, **kwArgs):
        """ meta is a void element, no contents are allowed """
        super().__init__(tag="meta", **kwArgs)


class Style(BaseElement):
    """ 
    create a <style> element 
    As it stands, domible doesn't know anything about CSS.
    The user crating a <style> object is expected to create valid CSS 
    and create this element with the CSS content as a string.
    """
    def __init__(self, contents: str, **kwArgs):
        super().__init__(tag="style", **kwArgs)


class Title(BaseElement):
    """ Create a Title element
    Titles can only contain strings of text (per spec).
    This is enforced in this class.

    it's necessary to override setContent and addContent to ensure title is a string 
    and there is no other content in the element 
    """

    def __init__(self, contents: str, **kwArgs):
        if not isinstance(contents, str):
            raise TypeError("Title contents must be a string")
        self.titleStr = contents
        super().__init__(tag='title', contents=self.titleStr, **kwArgs)


    def set_title(self, title: str) -> None:
        """ set the value, must be a string, for the Title. """
        self.set_content(title)


    def set_content(self, content: Any) -> None:
        """ 
        <title> can only have a string that is the title  
        If the new content is a string, 
        overrite any existing title 
        else, raise an exception 
        """
        if not isinstance(content, str):
            raise TypeError("Title contents must be a string")
        self.titleStr = content
        super().set_content(content)


    def add_content(self, content: Any, front: bool = False) -> None:
        """ 
        let Title.setContent handle this 
        """
        self.set_content(content)


# end of file
