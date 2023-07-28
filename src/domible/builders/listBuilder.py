""" domible/src/domible/builders/listBuilder.py

Provide a more flexible interface to the various list elements.

This builder was motivated during implementation of the NavBuilder.
I want to create a legit HTML list element by passing in a list of anythinh, 
e.g., text string, Buttons, Anchors, Headings, whatever is allowed in <li> elements.
The list classes based on BaseElement require the contents to be a list of ListItem objects.
I think that's the right limitation at that layer, this ListBuilder will be the higher level interface.

"""

import logging
logger = logging.getLogger(__name__)

from typing import Any

from domible.elements import DescriptionTerm, DescriptionDef, DListItem, ListItem 
from domible.elements import OrderedList, UnorderedList, MenuList, DescriptionList
from domible.elements import Script, Template


class ListBuilder:
    """ 
    used to create an HTML list element,
    e.g., <ul>, <ol>, <menu>.
    <dl> is a different builder due to its contents being structurally different.

    The type of list created is left unspecified until the HTML element is requested.
    This works because the contents of each  type of list is the same, 
    the semantics are determined only by the tag string 
    (hopefully someone will correct me if I'm wrong about this).

    All that said, the builder encapsulates the ability to manipulate a list of items of arbitrary type.
    Hopefully the names and comments of the methods clarify what I mean.
    """
    def __init__(self, items: list[Any] = None, **attributes):
        """
        as noted in the comments on the class declaration, 
        the type of list, the tag string, 
        is not needed until the builder generates an HTML element.
        We do however want to be able to set attributes for the list, thus **attributes
        """
        self.items = items if items else list()
        self.attributes = attributes if attributes else dict()

    def getList(self, tag: str, **attributes):
        """ 
        return the HTML element.
        More attributes can be added to the lists' opening tag if desired. 
        """
        if attributes: self.attributes.update(attributes)
        listitems = [ListItem(item) if not isinstance(item, (ListItem, Script, Template)) else item for item in self.items]
        if tag == "ul": return UnorderedList(listitems, **self.attributes)
        elif tag == "ol": return OrderedList(listitems, **self.attributes)
        elif tag == "menu": return MenuList(listitems, **self.attributes)
        else: raise ValueError(f"cannot build list with tag {tag}")


## end of file 