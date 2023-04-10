""" domible/tests/test_anchor.py 
testing the Anchor class from domible.elements 
"""

import logging 
logger = logging.getLogger(__name__)

from domible.elements import Anchor

from .testutils import validate_anchor


def test_basic_anchor():
    """ test an anchor with only an href and text contents """
    attrs = {"href": "https://blindgumption.com"}
    contents = "Blind Gumption Website"

    # HTML element text is genereated by evaluating the associated object
    # using str(Anchor()) should yield the same result 
    anchor_element = f"{Anchor(contents=contents, **attrs)}"
    logger.info(f"validating {anchor_element}")
    assert validate_anchor(attrs, contents,  anchor_element), \
        f"element: {anchor_element} is inconsistent with: {attrs, contents}"


def test_anchor_class_id():
    """ test an anchor with an href, class, and id attributes, and text contents """
    attrs = {
        "href": "https://blindgumption.com",
        "class": "a-class",
        "id": "uniqueId",
    }
    contents = "Blind Gumption Website"
    anchor_element = f"{Anchor(contents=contents, **attrs)}"
    logger.info(f"validating {anchor_element}")
    assert validate_anchor(attrs, contents, anchor_element), \
        f"element: {anchor_element} is inconsistent with: {attrs, contents}"


# end of file
