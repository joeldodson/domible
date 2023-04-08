""" domible/src/domible/elements/roots.py 

here is the <html> tag, considered the root of an HTML document.
I'm adding the <head> and <body> here as well, seems like a logical fit.
"""

from typing import Any 

from .baseElements import BaseElement


class Html(BaseElement):
    def __init__(self, contents: Any = None, lang: str = "en", **kwArgs):
        self.lang = lang
        super().__init__(tag="html", contents=contents, lang=lang, **kwArgs)

    def __repr__(self):
        return f"<!DOCTYPE html> \n{super().__repr__()}"


class Head(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        """ 
        tried having a constructor argument for a title with a default string.
        Turned in to a pain considering a Title object could be in the contents.
        Leaving it up to a document builder to handle a title string argument.  
        """
        super().__init__(tag="head", contents=contents, **kwArgs)


class Body(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="body", contents=contents, **kwArgs)


# end of file
