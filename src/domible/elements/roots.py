""" domible/src/domible/elements/roots.py 

here is the <html> tag, considered the root of an HTML document.
I'm adding the <head> and <body> here as well, seems like a logical fit.
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Any 

from .baseElements import BaseElement

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


class Html(BaseElement):
    def __init__(self, contents: Any = None, lang: str = "en", **kwArgs):
        self.lang = lang
        super().__init__(tag="html", contents=contents, lang=lang, **kwArgs)


    def getBody(self) -> Body:
        """ 
        return the body element from the html doc
        Only return it if it's the only one and is an instance of Body.
        else log a warning and return None 
        """
        elms = self.getElements("body")
        if len(elms) == 0:
            logger.warning("html doc has no body!  By the Geeky Blues Band")
            return None
        elif len(elms) == 1 and isinstance(elms[0], Body):
            # make this the second check as it's almost certainly true 
            return elms[0]
        elif len(elms) > 1:
            logger.warning("html doc appears to have more than one body element, BAD Doc!!")
            return None 
        else:  
            #  not isinstance(elms[0], Body):
            logger.warning("html doc has an element with tag body, but element is not of type Body.  I blame the user!")
            return None


    def __repr__(self):
        return f"<!DOCTYPE html> \n{super().__repr__()}"


# end of file
