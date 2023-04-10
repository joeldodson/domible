""" domible/tests/utils.py

some utilities to validate elements used by many of the test cases
"""

import json
import logging 
from typing import Any, TypeVar

from bs4 import BeautifulSoup as BSoup


logger = logging.getLogger(__name__)
StrOrList = TypeVar("StrOrList", str, list)


def validate_attributes(given: dict[str, str], parsed: dict[str, StrOrList]) -> bool:
    """ ensure the attributes used to create the element are correctly part of the element. 

    given: attributes used to create the element object, or added after construction 
    parsed: attributes parsed from the element by BeautifulSoup 

    This is complicated by multi-valued attributes, e.g., class.
    For details, see heading (at level 4) "Multi-valued attributes" 
    at https://www.crummy.com/software/BeautifulSoup/bs4/doc/

    TL;DR - attributes specified in the HTML spec as allowing multiple values 
    are parsed by BeautifulSoup into lists.
    Attributes having multiple values, but not specifically defined that way in the spec will be strings, 
    the same way you'd see them in the HTML document.
    """
    # first check that the attribute names are consistent between given and parsed
    if set(given.keys()) != set(parsed.keys()):
        logger.error("attrs check failed on keys comparison")
        return False
    # the attribute names are the same, now check their values 
    for k, v in parsed.items():
        if type(v) is str:
            if v != given[k]:
                logger.error(f"values {v, given[k]} do not match.")
                return False
        elif type(v) is list:
            if set(v) != set(given[k].split()):
                logger.error(f"values {set(v), set(given[k].split())} do not match.")
                return False
        else:
            assert False,  f"value {v}, for key {k}, is type {type(v)}"
    return True


def validate_anchor(attrs: dict[str:str], contents: Any, anchor_element: str) -> bool:
    """ check that the generated anchor_element is 
    consistent with the values passed in used to create the Anchor object. 
    """
    soup = BSoup(anchor_element, "html.parser")
    attrs_match = validate_attributes(attrs, soup.a.attrs)
    if not(contents_match := contents == soup.text.strip()):
        logger.error("contents do not match")
    logger.debug(f"validating anchor, attrs match is {attrs_match}, content match is {contents_match}")
    return attrs_match and contents_match


# end of file
