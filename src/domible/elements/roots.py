""" domible/src/domible/elements/roots.py 

here is the <html> tag, considered the root of an HTML document.
"""

import logging

logger = logging.getLogger(__name__)

from typing import Any

from domible.elements.baseElements import BaseElement
from domible.elements.meta import Head
from domible.elements  .sectioning import Body


class Html(BaseElement):
    """ 
    creates the root <html> element
    when rendered, also renders <!DOCTYPE html> 
    before the opening <html> tag 
    """
    def __init__(self, lang: str = "en", contents: Any = None, **kwArgs):
        self.lang = lang
        super().__init__(tag="html", contents=contents, lang=lang, **kwArgs)

    def get_head_element(self) -> Head:
        """
        return the Head element from the html doc
        Only return it if it's the only one and is an instance of Head.
        else log a warning and return None
        """
        elms = self.get_elements("head")
        if len(elms) == 1 and isinstance(elms[0], Head):
            # make this the first check as it's almost certainly true
            return elms[0]
        elif len(elms) == 0:
            logger.warning("html doc has no Head!  good pour!")
            return None
        elif len(elms) > 1:
            logger.warning(
                "html doc appears to have more than one Headelement, Cerberus?!?"
            )
            return None
        else:
            #  not isinstance(elms[0], Head):
            logger.warning(
                "html doc has an element with tag head, but element is not of type Head.  I blame the user!"
            )
            return None

    def add_elements_to_head(self, element: BaseElement | list[BaseElement]) -> None:
        """ add the passed in element to the end of list of elements in the head element of the HTML doc """
        head:Head = self.get_head_element()
        if head:
            head.add_content(element)

    def get_body_element(self) -> Body:
        """
        return the body element from the html doc
        Only return it if it's the only one and is an instance of Body.
        else log a warning and return None
        """
        elms = self.get_elements("body")
        if len(elms) == 1 and isinstance(elms[0], Body):
            # make this the first check as it's almost certainly true
            return elms[0]
        elif len(elms) == 0:
            logger.warning("html doc has no body!  By the Geeky Blues Band")
            return None
        elif len(elms) > 1:
            logger.warning(
                "html doc appears to have more than one body element, BAD Doc!!"
            )
            return None
        else:
            #  not isinstance(elms[0], Body):
            logger.warning(
                "html doc has an element with tag body, but element is not of type Body.  I blame the user!"
            )
            return None

    def add_contents_to_body(self, contents:Any) -> None:
        """ add contents to end of the body element """
        body: Body = self.get_body_element()
        if body:
            body.add_content(contents)

    def __repr__(self):
        return f"<!DOCTYPE html> \n{super().__repr__()}"


# end of file
