#!/usr/bin/env python
""" domible/scripts/dibrowse/main.py 

script to parse the domible package for all python modules, classes, and functions.
collect source code for each of those objects.
use domible to generate html page of its own source code.

This will work similarly to element_from_object in the builders.
For a given module (hard coded to the domible package for now),
get all the modules, functions, and classes directly in the modules namespace.
For each module in the namespace, recurse into it and do the same thing.

Build up a tree of details elements with the object name as the summary.
The contents will be the module's source code and list of any modules contained by that module.
Termination of a branch is when a module has only classes and functions.

This approach worked well enough.
There was a lot of duplicate entries due to imports in various modules.
Step 2 is now making the output more like the directory structure in the domible package.

First list the modules that are sub packages
next list modules that are files within a directory.
Last list all non module members in the module, e.g., functions, classes, others.
Nothing should be listed in more than one place.
"""

import inspect
from pathlib import Path
from typing import Self 

import domible 
from domible import open_html_document_in_browser
from domible.starterDocuments import basic_head_empty_body
from domible.elements import Html, Details, Summary, Heading, Paragraph, UnorderedList, ListItem, Pre, Style
from domible.builders import (
    default_expand_details_button,
    default_collapse_details_button,
    python_code_block,
    python_code_style,
)

##
# to get dicli in the source code output, need to import its main module.
# dibrowse main module is already imported due to this running script.
import domible.scripts.dicli.main

import argparse
import importlib

def module_type(module_name):
    """
    Custom type function to import a module by name.
    defined here to use in parser.add_argument.
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        raise argparse.ArgumentTypeError(f"Cannot import module '{module_name}': {e}")

dibrowse_help = """ show source code for given python module.
defaults to domible package,
but, in theory, should work with any non builtin module.
Only shows native python code though.
"""
module_help = """ name of module to parse and display its python code """
parser = argparse.ArgumentParser(
    prog="dibrowse",
    description=dibrowse_help,
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Cheers!",
)

parser.add_argument("module", nargs="?", default="domible", type=module_type, help=module_help)
args = parser.parse_args()


def is_package(module) -> bool:
    """
    inspect.ispackage was added in python 3.14.
    rolling my own limited version for now.
    """
    return hasattr(module, '__path__')


def is_builtin(member) -> bool:
    """ 
    inspect.isbuiltin() does not check for buildin modules (e.g., sys).
    rolling my own.
    """
    if not inspect.ismodule(member):
        if inspect.isbuiltin(member): return True
    else:  #  check if it is a builtin module.
        try:
            inspect.getfile(member)
            return False
        except TypeError:
            return True


def get_name(obj):
    """Get the most descriptive name for any object."""
    # Try __name__ first (functions, classes, modules)
    if hasattr(obj, "__name__"):
        return obj.__name__

    # Try __class__.__name__ (instances)
    if hasattr(obj, "__class__"):
        return obj.__class__.__name__
    # Fallback to type name
    return type(obj).__name__


"""
get_leaf_html and get_module_html are the brute force, 
show all members returned by inspect.getmembers()
and display them in a details element.
There is some filtering to ensure we don't dig into modules not defined within domible.
There is a bit of creep though with non module imports (e.g., Any).
"""

def get_leaf_html(leaf: object, name: str = None) -> Details | str:
    """
    Leaf isn't really the right name, I'm abusing the tree metaphore.
    Leaf in this case simply means the object is not a module, thus do not recurse into it.
    A 'leaf' is a class, function, or other, and we simply want a Details element with its name and source code.
    There is no branch continuing from this object.

    passing in the "name" from inspect.getmembers.
    It might be different from what's found in get_name,
    specifically for instances of classes exposed at module level 
    (imported in __init__.py).
    """
    leaf_name = get_name(leaf)
    if inspect.isclass(leaf): leaf_type = "class"
    elif inspect.isfunction(leaf): leaf_type = "function"
    else: leaf_type = "other"
    try:
        source_code = python_code_block(inspect.getsource(leaf))
        return Details(Summary(f"{leaf_type}: {leaf_name}"),source_code)
    except Exception as ex:
        return f"{name} ({leaf_name}) - cannot find source, object is likely an instance variable"


def get_module_html(module: object) -> Details:
    """
    Parse a module into a details element.
    The summary is the name of the module.
    The hidden HTML is a list with the source code of the module and any modules contained.
    Source code is also collapsed in a details element.
    functions and classes will also be part of that list along with their source code.
    """
    mod_name = get_name(module)
    print(f"getting HTML for module {mod_name}")
    mod_file = f"File: {inspect.getfile(module)}"
    mod_src = Details(Summary("Source Code"), python_code_block(inspect.getsource(module)))
    ul = UnorderedList(**{"style": "list-style-type: none;"})
    ul.add_item(ListItem(mod_file))
    ul.add_item(ListItem(mod_src))
    mod_details = Details(Summary(f"Module: {mod_name}"), ul)

    # we have the details for the module setup with the module name, file, and source code,
    # now process any sub modules, functions, classes, or 'other'
    mod_path = Path(inspect.getfile(module)).parent
    for name, member in inspect.getmembers(module):
        if is_builtin(member) or  name.startswith("_"):
            # ignore dunder and private methods and variables
            continue

        if inspect.ismodule(member):
            member_file = inspect.getfile(member)
            # Only include modules defined in this package
            if member_file.startswith(str(mod_path)):
                ul.add_item(ListItem(get_module_html(member)))
        else: 
            ul.add_item(ListItem(get_leaf_html(member, name)))
    print(f"finished getting HTML for module {mod_name}")
    return mod_details

"""
Below is where we get much more organized as to what is included, and in what order.
And taking a different approach with classes.
"""

class ParsedMod:
    """
    ParsedMod has a reference to the mod itself, some meta data, then 
    - lists of sub modules (indicating the parsed module is likely a package),
    - non module objects defined within the module (e.g., classes and functions).
    - list of likely instance variables.
    Only .py files should have classes and functions and other non module definitions.
    All the conditionals comparing paths and files and attributes,
    are attempts to determine if the member being considered is actually defined in the module being parsed.
    This in large part is due to imported items show up in the inspect.getmembers(module) output.
    I could do this using asattr, looking for __path__ and __module__ attributes.
    I already did it using paths though which seems to work as well.
    """
    def __init__(self, module):
        if not inspect.ismodule(module):
            raise ValueError(f"argument, {get_name(module)}, to ParsedModule must be a module")
        self.module = module 
        self.mod_name = get_name(module)
        self.mod_file = Path(inspect.getfile(module))
        self.mod_path = Path(inspect.getfile(module)).parent
        self.sub_mods = []
        self.not_mods = [] # e.g., classes and functions 
        self.instances = [] # objects that except on inspect.getfile()

    def parse(self) -> Self:
        ## print(f"parsing {self.mod_name}")
        for name, member in inspect.getmembers(self.module):
            if is_builtin(member) or  name.startswith("_"):
                # ignore dunder and private methods and variables
                continue

            if inspect.ismodule(member):
                print(f"module {get_name(member)}")
                # if we're looking at a module, check that it is defined directly within the module being parsed.
                # if so, recursively parse the module and add it to the list of sub modules.
                # otherwise, it can be ignored.
                # inspect.getfile() ends with the __init__.py file for packages,
                # and the source file for code modules, thus the .parent.
                m_path = Path(inspect.getfile(member)).parent
                if (m_path == self.mod_path or # member is likely a py file within the package 
                m_path.parent == self.mod_path): # mod is a sub package 
                    self.sub_mods.append(ParsedMod(member).parse())
            else:  # it's a function, class, or something else.
                # check that it is defined within this module and save it for later if so.
                # getfile() will error if, for example, member is an instance variable.
                # save a string for each instance variable.
                try:
                    nm_file = Path(inspect.getfile(member))
                    if nm_file == self.mod_file :
                        ## print(f"saving {get_name(member)}")
                        self.not_mods.append(member)
                except:
                    self.instances.append(
                        f"{name}: {get_name(member)} - probably an instance variable"
                    )
        return self

    def get_html(self) -> Details:
        """
        create a Details element with the module name as summary,
        then list of module source code, other modules, non module defs and instance objects.
        """
        mod_src = Details(Summary("Source Code"), python_code_block(inspect.getsource(self.module)))
        ## ul = UnorderedList(**{"style": "list-style-type: none;"})
        ul = UnorderedList()
        ul.add_content([
            ListItem(mod_src)
        ])
        modtype = "package" if is_package(self.module) else "code file"
        details_mod = Details(Summary(f"{modtype}: {self.mod_name}"), ul)
        # We hve the Details element for the module,
        # now add any sub modules and other definitions to the list (ul).
        if len(self.sub_mods) > 0:
            ul.add_content([ListItem(m.get_html()) for m in self.sub_mods])
        # now look at objects that are not mods, but also do not error on inspect.getfile()
        # These are most likely class and function definitions.
        # Note we can use get_leaf_html here as it already does what I want.
        if len(self.not_mods) > 0:
            ul.add_content([ListItem(get_leaf_html(nm)) for nm in self.not_mods])
        # and finally get the strings of objects that error on inspect.getfile(), instance variables.
        if len(self.instances) > 0:
            ul.add_content([ListItem(inst) for inst in self.instances])
        return details_mod


def run():
    modname = args.module.__name__
    print(f"parsing module {modname}")
    module_html_focused = ParsedMod(args.module).parse().get_html()
    title: str = f"Source Code for the {modname} package"
    html_doc = basic_head_empty_body(title)
    html_doc.add_elements_to_head(python_code_style)
    html_doc.add_contents_to_body([
        default_expand_details_button(), 
        default_collapse_details_button(),
        Heading(1, title),
        Paragraph(f"Root path for {modname}: {Path(inspect.getfile(args.module)).parent}"),
        module_html_focused,
    ])
    open_html_document_in_browser(html_doc)

if __name__ == "__main__":
    run()

## end of file
