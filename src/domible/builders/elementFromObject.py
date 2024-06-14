""" domible/src/domible/builders/elementFromObject.py 

Create fairly simple HTML from a Python object.
This will start with very simple static HTML.
AT some point, there might be expandable/collapsable functionality.

Okay, it's been a few days since I wrote that opening comment.
I hadn't thought it through and now realize "simple" is not the right word.
Let's break this down.

The entry function to this module, element_from_object (efo), is passed in some arbitrary Python object.
I've made the simplifying decision only lists, tuples, sets, dicts will be expanded.
Anything not one of those, I'm calling a "terminal" will simply have its str() value added to the HTML.

I'm considering lists, tuples, and sets as iterators and map them all to an HTML unordered list <ul>
When any of them are encountered, they're processed identically.
each item in the iterator is added to the <ul> within an <li> element.
lists, which will be sublists, are added with the ListBuilder.add_sublist (see comments on that method for why).

What about adding a dict to a list though?
Maybe treat it like a sub list as well where each key, value is a list item.
I think that's okay as long as the value is a terminal type.

What about the case where the value is another dict, or an iterator (list, tuple, set)?
I'm going to treat the key as a heading for that value.
The key will be added to the current list within an hn, where n is TBD,
and the value will be a sublist.
"""

import logging 
logger = logging.getLogger(__name__)

import html 
import json 

from domible.elements import BaseElement, ListItem, UnorderedList, Paragraph, Anchor, Heading  
from domible.builders.listBuilder import ListBuilder 

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
    and add it to the ListBuilder.
    """
    logger.debug(f"process_iter with object {obj}, depth {depth}")
    lb = ListBuilder()
    for item in obj:
        if depth >= max_depth:
            # create a list of terminal objects, don't go any deeper 
            lb.add_item(ListItem(process_terminal(item)))
            continue
        if isinstance(item, dict):
            contents = process_dict(item, depth + 1)
            lb.add_sublist(contents)
        elif isinstance(item, (list, tuple, set)):
            contents = process_iter(item, depth + 1)
            lb.add_sublist(contents)
        else:
            contents = process_terminal(item)
            lb.add_item(ListItem(contents))
    return lb.get_list('ul')


def process_dict(obj: dict, depth: int) -> BaseElement:
    """
    See comments at the file level regarding why dicts are treated the way they are here.
    As you'll see below, keys in the dict are treated as terminals (as I've defined in this file)
    Yes, a tuple can be a key in a dict.
    I'm making a simplifying assumption here (already spent way too much time on this module).
    If treating tuples as terminals here becomes a problem, maybe I'll change it.
    """
    logger.debug(f"process_dict with object {obj}, depth {depth}")
    lb = ListBuilder()
    for key, value in obj.items():
        # k,v are handled based on the type of the value.
        # always treat the key as a "terminal" though.
        key_html = process_terminal(key)

        # if the value is an iterable or dict,
        # use a general ListItem with the key as a heading and value as a list
        if isinstance(value, (list, tuple, set, dict)):
            if depth >= max_depth:
                value_html = process_terminal(value)
                lb.add_item(ListItem(f"{key_html}: {value_html}"))            
                continue
            key_heading = Heading(min(depth, max_depth, 6), key_html)
            if isinstance(value, dict):
                valuelist = process_dict(value, depth + 1)
            else:
                valuelist = process_iter(value, depth + 1)
            lb.add_item(ListItem([key_heading, valuelist]))
        elif isinstance(value, str) and validators.url(value):
            # if the value is a valid HTTP(S) URL, add an anchor as a list item
            kv_anchor = Anchor(value, key_html)
            lb.add_item(ListItem(kv_anchor))
        else:
            # otherwise, add a list item in "key: value" format
            # (because I don't like how NVDA handles DL lists)
            value_html = process_terminal(value)
            lb.add_item(ListItem(f"{key_html}: {value_html}"))
    return lb.get_list('ul')


def process_terminal(obj) -> str:
    """
    process_terminal is called either when there is a terminal object 
    (not a dict, list, tuple, or set)
    or when depth has been reached and we don't want to go any deeper into the object 
    """
    if isinstance(obj, (dict, list, tuple, set) ): 
        return f"object is type {type(obj).__name__}, with length {len(obj)}"
    return html.escape(str(obj))


def element_from_object(obj: object, depth: int = 42) -> BaseElement: 
    """
    since, in theory, objects can have unlimited complexity, 
    depth can be specified to limit the amount of HTML returned.
    Once depth is reached, any non-terminal objects
    (e.g., dict, list, tuple, set) will be a string with some meta-data about the object.
    initially depth counted down with base case as 0.
    now depth is used to calculate which HTML heading tag to use
    (see file comments regarding headings)

    inistially support a subset of Python objects:
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
        return process_dict(obj, 1)
    elif isinstance(obj, (list, tuple, set)):
        return process_iter(obj, 1)
    return Paragraph(process_terminal(obj))


## end of file
