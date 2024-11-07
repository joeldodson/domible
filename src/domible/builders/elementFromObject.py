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
The key will be added to the current list within an hn, where n is based on depth within the object,
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

def process_iter(obj: object, depth: int, ignore_Nones: bool = True) -> UnorderedList:
    """
    create an HTML <ul> from the iterator  
    For each item in the iterator, 
    get the HTML for that item,
    wrap it in a ListItem,
    and add it to the ListBuilder.

    if the item is another list/tuple/set, or a dict,
    a sublist is added to the list.
    Initially there was no bullet point at the current level indicating a sublist was being added.
    I found that confusing and added the bullet point 
    about the type of sublist, and its length.
    """
    logger.debug(f"process_iter with object {obj}, depth {depth}")
    lb = ListBuilder()
    for item in obj:
        if (depth >= max_depth) or (hasattr(item, '__len__') and len(item) == 0):
            # if depth has been reached, create a list of terminal objects, don't go any deeper
            # or if an object is empty, treat it like a terminal
            lb.add_item(ListItem(process_terminal(item)))
            continue
        sublist = None
        if isinstance(item, dict):
            sublist = process_dict(item, depth + 1, ignore_Nones = ignore_Nones)
        elif isinstance(item, (list, tuple, set)):
            sublist = process_iter(item, depth + 1, ignore_Nones=ignore_Nones)
        bullet_str = process_terminal(item)
        contents = [bullet_str, sublist] if sublist else bullet_str
        lb.add_item(ListItem(contents))
    return lb.get_list('ul')


def process_dict(obj: dict, depth: int, ignore_Nones: bool = True) -> BaseElement:
    """
    See comments at the file level regarding why dicts are treated the way they are here.
    As you'll see below, keys in the dict are treated as terminals (as I've defined in this file)
    Yes, a tuple can be a key in a dict.
    I'm making a simplifying decision here (already spent way too much time on this module).
    If treating tuples as terminals here becomes a problem, maybe I'll change it.

    if the value results in a sublist,
    add a string after the key indicating the type and length of that value
    I think it adds clarity when using a screen reader 
    """
    logger.debug(f"process_dict with object {obj}, depth {depth}")
    lb = ListBuilder()
    for key, value in obj.items():
        # first, if we're not adding anything with a None value to output, simply skip this k,v pair.
        if value == None and ignore_Nones: 
            continue 

        # key, value are handled based on the type of the value.
        # always treat the key as a "terminal" though.
        key_html = process_terminal(key)
        value_html = "something has gone wrong if you see this string"
        if isinstance(value, str) and validators.url(value):
            # if the value is a valid HTTP(S) URL, add an anchor as a list item
            kv_anchor = Anchor(value, key_html)
            lb.add_item(ListItem(kv_anchor))
        else:
            if depth < max_depth and isinstance(value, (list, tuple, set, dict)):
                # if the value is an iterable or dict,
                # use a general ListItem with the key as a heading and value as a list
                # UPDATE: I didn't like the NVDA flow with key as a heading...
                # and changing that simplified this method
                if len(value) == 0:
                    # this reads a little cleaner in the screen reader
                    value_html = process_terminal(value).replace('object', 'value') 
                elif isinstance(value, dict):
                    key_html = f"{key_html} ({process_terminal(value).replace('object', 'value')})" 
                    value_html = process_dict(
                        value, depth + 1, ignore_Nones=ignore_Nones
                    )
                else:
                    key_html = f"{key_html} ({process_terminal(value).replace('object', 'value')})"
                    value_html = process_iter(value, depth + 1, ignore_Nones=ignore_Nones)
            else:
                # either we've hit depth,
                # or value is not a dict or iter
                # simply add a list item in "key: value" format
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


def element_from_object(obj: object, depth: int = 42, ignore_Nones: bool = True ) -> BaseElement: 
    """
    since, in theory, objects can have unlimited complexity, 
    depth can be specified to limit the amount of HTML returned.
    Once depth is reached, any non-terminal objects
    (e.g., dict, list, tuple, set) will be a string with some meta-data about the object.
    initially depth counted down with base case as 0.
    now depth is used to calculate which HTML heading tag to use
    (see file comments regarding headings)

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
        return process_dict(obj, 1, ignore_Nones = ignore_Nones)
    elif isinstance(obj, (list, tuple, set)):
        return process_iter(obj, 1, ignore_Nones = ignore_Nones)
    return Paragraph(process_terminal(obj))


## end of file
