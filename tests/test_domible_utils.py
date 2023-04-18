""" domible/tests/test_domible_utils.py 
testing the various utilities I've created in domible 
"""

import logging 
logger = logging.getLogger(__name__)

from domible import utils as domutils 

def test_subdict_is_subdict():
    dSub = {"id": "uniqueId", "class": "fancy"}
    dSuper = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    assert domutils.isSubDict(dSub, dSuper),  f"{dSub} should be a sub dict of {dSuper}"

def test_subdict_is_NOT_subdict():
    dSub = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    dSuper = {"id": "uniqueId", "class": "fancy"}
    assert not domutils.isSubDict(dSub, dSuper),  f"{dSub} should be a sub dict of {dSuper}"

def test_subdict_equal_dicts():
    dSub = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    dSuper = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    assert dSub == dSuper, "sub and super are supposed to be equivalent"
    assert domutils.isSubDict(dSub, dSuper),  f"{dSub} should be equal to {dSuper}"

def test_subdict_same_attrs_different_values():
    dSub = {"id": "unique-id", "class": "fancy", "random-attribute": "random-value"}
    dSuper = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    assert not domutils.isSubDict(dSub, dSuper),  "dSub and dSuper have same attributes but a value is different"


def test_subdict_empty_sub():
    dSub = {}
    dSuper = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    assert len(dSub) == 0, "sub is supposed to be empty"
    assert domutils.isSubDict(dSub, dSuper), f"sub is empty, should be sub dict of super, {dSuper}"

def test_subdict_empty_super():
    dSub = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    dSuper = {}
    assert len(dSuper) == 0, "super is supposed to be empty"
    assert not domutils.isSubDict(dSub, dSuper), "super is empty, sub is not.  isSubDict should have been False"

def test_subdict_empty_both():
    dSub = {}
    dSuper = {}
    assert len(dSub) == 0 and len(dSuper) == 0, "both sub and super are supposed to be empty"
    assert domutils.isSubDict(dSub, dSuper), "sub and super are both empty"

##########################################

def test_subdict_None_sub():
    dSub = None
    dSuper = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    assert dSub == None, "sub is supposed to be None"
    assert domutils.isSubDict(dSub, dSuper), f"sub is None, should be sub dict of super, {dSuper}"

def test_subdict_None_super():
    dSub = {"id": "uniqueId", "class": "fancy", "random-attribute": "random-value"}
    dSuper = None
    assert dSuper == None, "super is supposed to be None"
    assert not domutils.isSubDict(dSub, dSuper), "super is None, sub is not.  isSubDict should have been False"

def test_subdict_None_both():
    dSub = None
    dSuper = None
    assert dSub == None and dSuper == None, "both sub and super are supposed to be None"
    assert domutils.isSubDict(dSub, dSuper), "sub and super are both None"


## end of file 