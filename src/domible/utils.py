""" domible/src/utils.py 
little things I need to keep the code clean.
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