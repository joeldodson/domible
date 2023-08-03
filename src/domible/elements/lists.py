"""  domible/src/domible/elements/lists.py
Here we have elements specific to creating lists.
the list items (including <dt> and <dd>) are defined in here as well.
"""

from typing import Any

from domible.elements.baseElements import BaseElement

"""
<li>, <dt>, and <dd> are nearly the same element with different tags.
<dt> has more restrictions on its permitted content but I'm not sure this package needs to enforce that.
Maybe at some point I'll implement more types around content categories and build in more enforcement.
For now, I'm taking the C approach, so go ahead and corrupt memory.
Or in this case, implement nonsensical HTML documents.
"""


class DescriptionTerm(BaseElement):
    """creates a dt element."""

    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag="dt", contents=contents, **kwArgs)


class DescriptionDef(BaseElement):
    """creates a dd element."""

    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag="dd", contents=contents, **kwArgs)


class DListItem:
    """
    This is an attempt to make the dl list element behave similar to the other list elements.
    It is designed to be analogous to an li elment.
    It is created with a list of terms and their definition.
    It renders itself since it is not derived from BaseElement.
    Screen readers seem to have trouble with dl lists, they're a pain all around.
    """

    def __init__(self, terms: list[DescriptionTerm], definition: DescriptionDef):
        self.terms = terms
        self.definition = definition

    def __repr__(self):
        entryString = ""
        for term in self.terms:
            entryString += f"{term}"
        entryString += f"{self.definition}"
        return entryString


class ListItem(BaseElement):
    """creates an li element."""

    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag="li", contents=contents, **kwArgs)


class UnorderedList(BaseElement):
    """creates a ul element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("ul", entries, **kwArgs)


class OrderedList(BaseElement):
    """creates an ol element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("ol", entries, **kwArgs)


class MenuList(BaseElement):
    """creates a menu element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("menu", entries, **kwArgs)


class DescriptionList(BaseElement):
    """creates a dl element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("dl", entries, **kwArgs)


## end of file
