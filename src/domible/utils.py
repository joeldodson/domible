""" domible/src/domible/utils.py 
little things I need to keep the code clean.

I'm writing the following note after creating the tools.py module at the same level as utils.py.
Hopefully this clarifies why there is a utils.py and tools.py, maybe it's just my bad planning...
utils.py is imported in many of the submodules in domible
thus should not import (depend on) anything within domible.
It shuld mainly be generic Python code to keep domible code cleaner.
Nothing in utils is intended to be used by users of the domible package.
See comments in tools.py for more clarification. 
"""

from typing import Any 


def isSubDict(dSub: dict[str,str], dSuper: dict[str,str]) -> bool:
    """
    if all attributes in dSub are also in dSuper,
    and all values match,
    return True
    else False

    NOTE: treat None as empty set 
    """
    dSub = dSub if dSub  else {}
    dSuper = dSuper if dSuper else {} 
    subKV = {(k,v) for k,v in dSub.items()}
    superKV = {(k,v) for k,v in dSuper.items()}
    return subKV.issubset(superKV)


def indexMatchingAttributes(items: list[Any], attributes: dict[str,str]) -> int:
    """
    given a list of elements and a dict of attributes,
    return the index of the first element in the list for which attributes is a subset of its attributes 
    return None if no element has matching attributes 
    """
    for index, item in enumerate(items):
        if isSubDict(attributes, item.attributes):
            print(f"indexMatchinAttributes returning index: {index}")
            return index
    return None 


## end of file
