""" domible/src/domible/builders/elementFromObject.py 

Create fairly simple HTML from a Python object.

Okay, it's been many days since I wrote that opening comment.
I hadn't thought it through and now realize "simple" is not the right word.
But it's really not that bad, and I've written and deleted a lot of crap in this module comment.
So here it is at a high level.
anything not a list, tuple, set, or dict is considered a terminal.
lists, tuples, and sets are converted to simple unordered lists.
dicts are unordered lists with listitems as key: value pairs.
When a value in a dict, or an item in a list is a list, tuple, set, or dict, a sublist is created.
Sublists are presented as collapsible items.
See comments in the code for more details. 
"""

import logging 
logger = logging.getLogger(__name__)

import html 
import json 

from domible.elements import BaseElement, ListItem, UnorderedList, Paragraph, Anchor, Heading, Details, Summary  

import validators 

##
# using a global for depth to use depth to calculate heading levels
max_depth = None

def process_iter(obj: object, depth: int) -> UnorderedList:
    """
    create an HTML <ul> from the iterator  
    For each item in the iterator, 
    get the HTML for that item,
    wrap it in a ListItem,
    and add it to the list.

    if the item is another list/tuple/set, or a dict,
    a sublist is added to the list in a collapsible widget.
    meta-data is used as the summary for the sublist.
    """
    logger.debug(f"process_iter with object {obj}, depth {depth}")
    ul = UnorderedList(**{"aria-label":f"entering level  {depth}", "style": "list-style-type: none;"})
    for item in obj:
        list_contents = process_terminal(item)
        if depth < max_depth and isinstance(item, (list, tuple, set, dict)) and len(item) > 0:
            # if the itemis a non-empty iterable or dict, and we have not hit depth yet,
            # create a collapsible widget with the item meta-data as the Summary,
            # and the item as a list in the collapsible content.
            summary = Summary(list_contents)
            hidden_html = None 
            if isinstance(item, dict):
                hidden_html = process_dict(item, depth + 1)
            else:  # must be a list, tuple, or set 
                hidden_html = process_iter(item, depth + 1)
            list_contents = Details(summary, hidden_html)
        ul.add_item(ListItem(list_contents))
    return ul


def process_dict(obj: dict, depth: int) -> BaseElement:
    """
    See comments at the file level regarding why dicts are treated the way they are here.
    As you'll see below, keys in the dict are treated as terminals (as I've defined in this file)
    Yes, a tuple can be a key in a dict.
    I'm making a simplifying decision here (already spent way too much time on this module).
    If treating tuples as terminals here becomes a problem, maybe I'll change it.

    if the value results in a sublist,
    add a string after the key indicating the type and length of that value
    I think it adds clarity when using a screen reader 
    Added a disclosure widget to be able to collapse/expand sublist 
    """
    logger.debug(f"process_dict with object {obj}, depth {depth}")
    ul = UnorderedList(**{"aria-label": f"entering level {depth}", "style": "list-style-type: none;",})
    for key, value in obj.items():
        # key, value are handled based on the type of the value.
        # always treat the key as a "terminal" though.
        # and start by assuming the value is also a terminal and change if necessary
        list_contents = f"{process_terminal(key)}: {process_terminal(value)}"
        if depth < max_depth and isinstance(value, (list, tuple, set, dict)) and len(value) > 0:
            # if the value is a non-empty iterable or dict, and we have not hit depth yet,
            # create a collapsible widget with the key as the Summary,
            # and the value as a list in the collapsible content.
            summary = Summary(list_contents)
            hidden_html = None 
            if isinstance(value, dict):
                hidden_html = process_dict(value, depth + 1)
            else: # value is a list, set, or tuple
                hidden_html = process_iter(value, depth + 1)
            # now create the collapsible widget
            list_contents = Details(summary, hidden_html)
        ul.add_item(ListItem(list_contents))
    return ul


def process_terminal(obj) -> str:
    """
    process_terminal is called either when there is a terminal object 
    (not a dict, list, tuple, or set)
    or when depth has been reached and we don't want to go any deeper into the object 
    """
    if isinstance(obj, (dict, list, tuple, set) ): 
        if len(obj) == 0:
            return f"type empty  {type(obj).__name__}"
        else:
            return f"type {type(obj).__name__}"
    return html.escape(str(obj))


def element_from_object(obj: object, depth: int = 42) -> BaseElement: 
    """
    since, in theory, objects can have unlimited complexity, 
    depth can be specified to limit the amount of HTML returned.
    Once depth is reached, any non-terminal objects
    (e.g., dict, list, tuple, set) will be a string with some meta-data about the object.

    initially support a subset of Python objects:
    int, float, str, bool, list, tuple, set, and dict 
    anything else will have its str representation returned in a paragraph element
    For converting to HTML, list, tuple, and set can all be represented in an unordered list,
    and all three objects are iterators, thus can be processed the same way.
    int, float, str, and bool will be string representatives of themselves, 
    thus can be processed the same way as object types not supported here.

    read the file comments regarding how dicts are represented,
    it got more complicated than I had imagined.
    """
    global max_depth 
    max_depth = depth 
    if isinstance(obj, dict):
        return process_dict(obj, 0)
    elif isinstance(obj, (list, tuple, set)):
        return process_iter(obj, 0)
    return Paragraph(process_terminal(obj))


## end of file
