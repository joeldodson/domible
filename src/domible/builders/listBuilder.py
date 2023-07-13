""" domible/src/domible/builders/listBuilder.py

Provide a more flexible interface to the various list elements.

This builder was motivated during implementation of the NavBuilder.
I want to create a legit HTML list element by passing in a list of anythinh, 
e.g., text string, Buttons, Anchors, Headings, whatever is allowed in <li> elements.
The list classes based on BaseElement require the contents to be a list of ListItem objects.
I think that's the right limitation, so this ListBuilder will be the higher level interface.

"""

import logging
logger = logging.getLogger(__name__)

from typing import Any

from domible.elements import DescriptionTerm, DescriptionDef, DListItem, ListItem 
from domible.elements import OrderedList, UnorderedList, MenuList, DescriptionList

class ListBuilder:
    """ 
    used to create an HTML list element,
    e.g., <ul>, <ol>, <menu>
    """
## end of file 