""" domible/src/domible/__init__.py 
"""

# read version from installed package
from importlib.metadata import version
__version__ = version("domible")

import domible.elements
import domible.builders
import domible.starterDocuments 
from domible.tools import open_in_browser, save_to_file 
## end of file 