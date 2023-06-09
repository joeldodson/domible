""" domible/src/utils.py 
little things I need to keep the code clean.
"""

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
    


## end of file 