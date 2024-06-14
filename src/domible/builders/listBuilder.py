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

from typing import Any

from domible.elements import BaseElement 
from domible.elements import DescriptionTerm, DescriptionDef, DListItem, ListItem 
from domible.elements import OrderedList, UnorderedList, MenuList, DescriptionList
from domible.elements import Script, Template
from domible.utils import indexMatchingAttributes 


class ListBuilder:
    """ 
    used to create an HTML list element,
    e.g., <ul>, <ol>, <menu>.
    <dl> is a different builder due to its contents being structurally different.

    The type of list created is left unspecified until the HTML element is requested.
    This works because the allowed contents of each  type of list is the same, 
    the semantics of the list element are determined only by the tag string 
    (hopefully someone will correct me if I'm wrong about this).
    Does this provide any real value (the delaying of the tag specification)?
    Perhaps ther's a need to generate a <ul> and <ol> from the same set of list entries?
    Doubtful.
    It's six of one, half dozen the other though, when to specify the type of list, 
    so let's go with the delayed style.

    I toyed with the idea of a class ListEntry builder.
    It was motivated by the fact a list can contain <li>, <script>, and <template> elements.
    The ListEntry was going to, sort of, encapsulate that, 
    ideally making it easyer to create ListEntries.
    Then users of ListBuilder would not have to explicitly create an <li>, <script>, or <template> element before adding it to the ListBuilder object.
    ListEntry would hold the contents of the eventual HTML element, it would also have to hold attributes to eventually create the element. 
    ListEntry started getting messy and duplicating BaseElement functionality.
    I experimented with ways to avoid that duplication.
    Short answer, it was all worse than simply requiring the ListBuilder user to
    use ListItem, Script, or Template objects when creating/useing ListBuilder objects.

    I was also going down a rabbit hole deciding how much functionality to add to ListBuilder.
    I thought about all the cool stuff to do, but realized quickly it would be just as easy 
    for a user to grab the items from the ListBuilder and operate directly on that Python list.
    OOP authorities might legitimately have me thrown in the stocks for the idea of allowing 
    users of ListBuilder to operate directly on its data.
    I'll rationalize this anti pattern by claiming pragmatism 
    and let's see first if anyone will use this before going deep on its interface.

    Another thought on the ListBuilder interface, and why this class exists.
    self.items is guaranteed to be a list based on __init__,
    and Python's list interface is already quite good.
    self.items contents though are guaranteed to be a type of BaseElement.
    Considering that, the ListBuilder interface should probably provide functionality to optimize dealing with a list of BaseElement objects.
    For example, I might want to add or update attributes to all elements in the list.
    Or maybe I want to update an attribute in the contents of a list item.
    And here we go down the rabbit hole... 
    """
    def __init__(self, items: list[Any] = None, **attributes):
        """
        as noted in the comments on the class declaration, 
        the type of list, the tag string, 
        is not needed until the builder generates an HTML element.
        We do however want to be able to set attributes for the list, thus **attributes
        """
        self.items: list[Any] = items if items else list()
        if not isinstance(self.items, list): self.items = [self.items]
        self.attributes: dict[str, str] = attributes if attributes else dict()
        for item in self.items:
            if not isinstance(item, (ListItem, Script, Template)):
                raise TypeError(f"{item} -- is not an li, script, or template element")


    def add_item(self, item: Any, index: int = None, attributes: dict[str, str] = None, before: bool = True) -> None:
        """
        add an item to the list, where is based on values of other parameters. 
        if index given, add item at that index 
        if index is not in range, raise IndexError
        if attributes, add item based on the attributes of another item
        if before is True, ad new item before existing item with matching attributes, else after
        before is ignored if attributes is None 
        if attributes is specified but no match is found, raise ValueError 
        if no index and attributes, add new item to end of list
        if index and attributes are both specified, attributes is ignored.
        """
        if not isinstance(item, (ListItem, Script, Template)):
            raise TypeError(f"{item} -- is not an li, script, or template element")
        if index:
            if index >= 0 and index < len(self.items):
                self.items.insert(index, item)
            else:
                raise IndexError(f"index {index} is outside range, len of items is {len(self.items)}")
        elif attributes:
            if (insert := indexMatchingAttributes(self.items, attributes)) != None:
                print(f"inserting at index {insert}, before is {before}")
                if before: self.items.insert(insert, item)
                else: self.items.insert(insert + 1, item)
            else:
                raise ValueError(f"no element found matching attributes {attributes}")
        else:
            self.items.append(item)


    def add_sublist(self, sublist: BaseElement, index: int = None, attributes: dict[str, str] = None, before: bool = True):
        """
        add_sublist exists to address the issue of an extra bullet point 
        when including an HTML list (e.g., <ul>, <ol>) within an <li>.
        This is required to comply with the content guidelines of what is allowed as a childe of a list element.
        check out the MDN docs for more details.

        The sublist must be one of the list elements from domible.elements.lists.
        add_sublist will wrap it in a <li> element and 
        add a style="list-style-type:none" attribute to the <li> wrapper.
        The <li> is then added to the list being built in this class/object. 
        See comments for ListBuilder::add_item for description of parameters after sublist.
        """
        li_wrapper = ListItem(sublist, style="list-style-type:none")
        self.add_item(li_wrapper, index, attributes, before)


    def get_list(self, tag: str, **attributes):
        """ 
        return the HTML element.
        More attributes can be added to the lists' opening tag if desired. 
        """
        if attributes: self.attributes.update(attributes)
        ## self.items = [ListItem(item) if not isinstance(item, (ListItem, Script, Template)) else item for item in self.items]
        if tag == "ul": return UnorderedList(self.items, **self.attributes)
        elif tag == "ol": return OrderedList(self.items, **self.attributes)
        elif tag == "menu": return MenuList(self.items, **self.attributes)
        else: raise ValueError(f"cannot build list with tag {tag}")


## end of file 
