#!/usr/bin/env python
""" domible/tests/efo.py 
 efo is from the function element_from_object 
 this is a simple file to test the function.
 It's not named according to pytest as I don't want it in the automated tests yet.
 I'll rename it eventually 
"""

import logging
import jsonloggeriso8601datetime as jlidt

jlidt.setConfig()
logger = logging.getLogger(__name__)

from sys import argv

from domible.builders import element_from_object 
from domible import open_html_in_browser, open_object_in_browser 
from domible.starterDocuments import basic_head_empty_body
from domible.elements import Html, Body, BaseElement, Heading

##
# following are some hard coded values to test
# 'me' comes from Atlassian with some data anonomized (sort of)

rd = {"key1": "value1", "key2": "value2", "bg_url": "https://blindgumption.com"}

bio = {
    "name":{"first": "Joel", "last": "Dodson"},
    "location": "SF Bay Area",
    "projects": [
        "list of projects as dicts",
        {"title": "domible", "repo_url": "https://github.com/joeldodson/domible"},
        {"title": "atlassible", "repo_url": "https://github.com/joeldodson/atlassible"},
        {},
    ],
    "redacted information": {
        "skeletons in closet": [],
        "arrest record": {},
    },
}


cases = {
    "bio": bio,
    ## random dict
    "rd": rd,
    ## list of lists
    "lol": [[1, 2, 3], [4, 5, 6]],
    ## list of lists of lists
    "lolol": [
        [1, 2, 3],
        [4, 5, 6],
        [[11, 22, 33], ["a", "b", "c", "d"]],
        {"sweet girls":["annie", "chelsea", "maple"]},
    ],
}

if __name__ == "__main__":

    if len(argv) < 2:
        print("usage: efo <obj name | 'cases' to run all> [depth]")
        print(f"names of objects in cases: {[c for c in cases.keys()]}")
        exit(0)

    depth = 42
    if len(argv) > 2:
        try:
            depth = d if (d := int(argv[2])) >= 0 else 42
        except:
            depth = 42

    obj, title = None, None
    arg = argv[1]
    if arg in cases:
        obj = cases[arg]
        title = f"running test {arg}, depth is {depth}"
        open_object_in_browser(obj, depth, title,)
    elif arg == 'cases':
        html = basic_head_empty_body(f"EFO: running all cases, depth {depth}")
        body = html.get_body_element()
        for name, obj in cases.items():
            elem = element_from_object(obj, depth)
            body.add_content([Heading(2, f"Object {name}"), elem])
        open_html_in_browser(html)
        # print the HTML in case I want to redirect output to a file.
        # it's easier than supporting writing to a file in this code.
        if len(argv) > 3 and argv[3] == "print":
            print(f"{html}")
    else:
        print(f"no object with name '{arg}' in cases.  run efo with no arguments to list cases.")


## end of file
