""" domible/src/domible/builders/navBuilder.py

here we have a class to build a navigation element, <nav>.
It's based on an article from web.dev:
https://web.dev/website-navigation/

I'm starting this on 2023-05-25, with a focus on bare minimum functionality.
There is likely a lot of static stuff, especially CSS and JS.

Ugh.  Now it's 2023-07-12 and I've made almost no coding progress.
I'm hung up on feature creep.
I've been reading different articles on how to implement navigation and support collapsible sub navigation and support arrow keys and escape and whatnot...
I've decided to initially support the most basic navigation, list of anchors.
And whatever the API looks like intially is almost certainly going to change.
I'm embracing the ideals of get something out there and iterate 
(maybe, or maybe not known as Minimum Viable Product)

the following is from https://developer.mozilla.org/en-US/docs/web/html/element/nav
  The <nav> element represents a section of a page whose purpose is to provide navigation links,
  either within the current document or to other documents. 
  Common examples of navigation sections are 
  menus, tables of contents, and indexes.
""" 

from typing import Any

from domible.elements import Nav
from domible.elements import UnorderedList, OrderedList 

class NavBuilder:
    """
    This minimalist navigation element consists of a <nav> element and list of navigable items.
    For screen reader support, we'll require a string label for the nav element
    Though trying to not hard code any assumptions in the API for this class, 
    my expectation is the list of navigable items will be anchors.
    """

    def __init__(self, label: str, items: list[Any] = None, ordered: bool = False, currentPage:int = 0, **attributes):
        """
        label will be used in an aria-label attribute for the nav element.
        items is the list of navigable links in the ul or ol list
        the value of ordered dictates whether a ul or ol list is used.
        currentPage is the index of the item that is the page currently accessed from the nav.
        currentPage is used to set the aria-current="page" attribute on the list item 
        """
        self.label = label
        self.items = items if items else [] 
        if not ordered:
            self.itemsList = UnorderedList(self.items)
        else:
            self.itemsList = OrderedList(self.items)

## end of file 