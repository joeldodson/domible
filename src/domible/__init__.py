""" domible/__init__.py 

domible is a package used to generate accessible HTML documents of arbitrary complexity.
Python classes represent HTML elements.
Each class has a dict for element attributes and a contents member for the contents of the element.
Contents can be anything including other objects of HTML elements.
Evaluating a domible object results in the text of the HTML element it represents.
Starting from the root Html class, an HTML document is built using composition.
Evaluating the root Html object recursively evaluates all contents resulting in the text of an HTML document.

domible provides a set of builder abstractions to encapsulate some of the more complicated HTML structures.
TableBuilder is the first example.
Builders attempt to enforce accessibility standards by default.

Domible also provides starter documents with the basic structure of a simple HTML doc.
For example, the most basic starter document includes, within the Html element,
a Head element with a Title and a few Meta elements,
and an empty Body element.

I turned the scripts subdirectory into a package to use it as a source of sample code.
it is not imported anywhere in domible.
The dibrowse main module directly imports the dicli main module so both their source code will be added to dibrowse output.
you should never import anything from scripts.
"""

# read version from installed package
from importlib.metadata import version
__version__ = version("domible")

# use relative references to keep the namespaces cleaner.
from . import builders, elements, starterDocuments
from .tools import open_object_in_browser, open_html_document_in_browser, open_html_fragment_in_browser, save_to_file 

## end of file 