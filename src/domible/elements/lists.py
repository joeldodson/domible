"""  domible/src/domible/elements/lists.py
Here we have elements specific to creating lists.
the list items (including <dt> and <dd>) are defined in here as well.
"""

from typing import Any

from domible.elements.baseElements import BaseElement
from domible.elements.scripting import Script, Template 
from domible.elements.inline import Details, Summary
from domible.utils import index_matching_attributes


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


class HtmlListBase(BaseElement):
    """
    HtmlListBase is used to ensure any elements passed in at creation are either
    ListItem, Script, or Template elements 
    add_contents is overridden also to ensure valid content types 
    """
    @staticmethod
    def valid_list_element(element) -> bool:
        if element: return isinstance(element, (ListItem, DListItem, Script, Template, Details))
        return True 

    @staticmethod
    def valid_contents(contents) -> bool:
        if not isinstance(contents, list):
            return HtmlListBase.valid_list_element(contents)
        for elem in contents:
            if not HtmlListBase.valid_list_element(elem): return False 
        return True 

    def __init__(self, tag: str, entries: list[Any] = None, **kwArgs):
        if not HtmlListBase.valid_contents(entries):
            raise TypeError("list items must be either ListItem, DListItem, Script, or Template")
        super().__init__(tag, entries, **kwArgs)

    def add_content(self, content: Any, front: bool = False) -> None: 
        """
        overriding BaseElement to ensure content is appropriate for a list,
        then use BaseElement to add the contents.
        """
        if not HtmlListBase.valid_contents(content):
            raise TypeError(
                "list items must be either ListItem, DListItem, Script, or Template"
            )
        super().add_content(content, front)

    def add_item(
        self,
        item: Any,
        index: int = None,
        attributes: dict[str, str] = None,
        before: bool = True,
    ) -> None:
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
        if not HtmlListBase.valid_contents(item):
            raise TypeError(f"{item} -- is not valid list content")
        if index:
            if index >= 0 and index < len(self.contents):
                self.contents.insert(index, item)
            else:
                raise IndexError(
                    f"index {index} is outside range, len of contents is {len(self.contents)}"
                )
        elif attributes:
            if (insert := index_matching_attributes(self.contents, attributes)) != None:
                print(f"inserting at index {insert}, before is {before}")
                if before:
                    self.contents.insert(insert, item)
                else:
                    self.contents.insert(insert + 1, item)
            else:
                raise ValueError(f"no element found matching attributes {attributes}")
        else:
            self.contents.append(item)

    def add_sublist(
        self,
        sublist: BaseElement,
        index: int = None,
        attributes: dict[str, str] = None,
        before: bool = True,
    ):
        """
        add_sublist exists to address the issue of an extra bullet point
        when including an HTML list (e.g., <ul>, <ol>) within an <li>.
        This is required to comply with the content guidelines of what is allowed as a childe of a list element.
        check out the MDN docs for more details.

        The sublist must be one of the list elements from domible.elements.lists, or a details element for hidden lists.
        add_sublist will wrap it in a <li> element and
        add a style="list-style-type:none" attribute to the <li> wrapper.
        The <li> is then added to the list being built in this class/object.
        See comments for HtmlListBase.add_item for description of parameters after sublist.
        """
        li_wrapper = ListItem(sublist, style="list-style-type:none")
        self.add_item(li_wrapper, index, attributes, before)

    def get_collapsible(self, summary: any) -> Details:
        """
        I've been building up a list in self
        I want to use that list in a collapsible details/summary combination of elements 
        return the Details element with self as its hidden contents 
        """
        summary = Summary(summary)
        return Details(summary, self)


class UnorderedList(HtmlListBase):
    """creates a ul element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("ul", entries, **kwArgs)


class OrderedList(HtmlListBase):
    """creates an ol element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("ol", entries, **kwArgs)


class MenuList(HtmlListBase):
    """creates a menu element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("menu", entries, **kwArgs)


class DescriptionList(BaseElement):
    """creates a dl element."""

    def __init__(self, entries: list[Any] = None, **kwArgs):
        super().__init__("dl", entries, **kwArgs)


## end of file
