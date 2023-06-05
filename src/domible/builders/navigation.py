""" domible/src/domible/builders/navigator.py

here we have a class to build a navigation element.
It's based on an article from web.dev:
https://web.dev/website-navigation/

I'm starting this on 2023-05-25, with a focus on bare minimum functionality.
There is likely a lot of static stuff, especially CSS and JS.
As of now, I haven't thought about how to dynamically include CSS and/or JS into these python elements.
Once/if I do, the hard coded stuff should go away.

the following is from https://developer.mozilla.org/en-US/docs/web/html/element/nav
  The <nav> element represents a section of a page whose purpose is to provide navigation links,
  either within the current document or to other documents. 
  Common examples of navigation sections are 
  menus, tables of contents, and indexes.
""" 

from domible.elements import UnorderedList, OrderedList 

class Navigation:
    """
    The basic navigation element consists of a <nav> element and list of navigable items.
    For screen reader support, we'll require a string label for the nav element
    """

    def __init__(self, label: str, items: list[Any] = None, ordered: bool = False, **attributes):
        self.label = label
        self.items = items if items else {} 
        if not ordered:
            self.itemsList = UnorderedList(self.items)
        else:
            self.itemsList = OrderedList(self.items)

## end of file 