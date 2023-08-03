""" domible/src/domible/builders/listBuilder.py

Provide a more flexible interface to the various list elements.

This builder was motivated during implementation of the NavBuilder.
It might be necessary to update attributes in an <li> element,
to, for example, indicate that list item is the current page in a <nav> element.
It's better to have functionality like that in a builder,
not in the element class itself.
"""

import logging
logger = logging.getLogger(__name__)

from collections import namedtuple
from typing import Any

from domible.elements import DescriptionTerm, DescriptionDef, DListItem, ListItem 
from domible.elements import OrderedList, UnorderedList, MenuList, DescriptionList
from domible.elements import Script, Template


# see comments in ListBuilder class declaration for why ListEntry exists 
ListEntry = namedtuple("ListEntry", "contents attributes", defaults=[dict()])
class ListEntry:
    """
    ListEntry encapsulates information to eventually be rendered as an HTML element.
    HTML list entries can be anything allowed in an <li>, <script>, or <template> element, 
    a very broad set.
    A ListEntry object holds references to the contents of what will be eventually rendered in the list,
    what type of element it should be rendered as,
    and any attributes to be added to the opening tag.
    """
    def __init__(self, contents: Any, elemType: str = "li", **attributes):
        """
        """
        self.contents = contents
        self.elemType = elemType
        self.attributes = attributes


class ListBuilder:
    """ 
    used to create an HTML list element,
    e.g., <ul>, <ol>, <menu>.
    <dl> is a different builder due to its contents being structurally different.

    The type of list created is left unspecified until the HTML element is requested.
    This works because the allowed contents of each  type of list is the same, 
    the semantics of the list element are determined only by the tag string 
    (hopefully someone will correct me if I'm wrong about this).

    All that said, the builder encapsulates the ability to manipulate a list of items of arbitrary type.
    Hopefully the names and comments of the methods clarify what I mean.

    Note on a design decision.
    The list items (<li>) are not created until a list is requested.
    Thus there is no way to easily add attributes to a specific list item (the ListItem object does not exist yet).
    To enable attributes to be associated with a specific list item,
    I made the items tuples of what will be the contents of the <li> element,
    and a dict that will be attributes added to the <li> opening tag for the associated contents.
    See the ListEntry named tuple above.
    The interface for the ListBuilder should encapsulate this design detail 
    by still defining the list item as Any and attributes as effectively kwArgs
    in method signatures.
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

    def addItem(self, item: Any, **attributes):
        """
        """
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