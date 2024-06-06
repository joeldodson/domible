""" domible/src/domible/tools.py

tools.py has functions for users of the domible package to do simple things
like open their HTML doc in the browser,
or save the HTML to a specified file.
tools.py imports other modules within domible thus should not be used by any of domible's submodules.
Any helper functions needed by domible should be put in utils.py 
See the top level comments in utils.py to understand why tools.py exists. 
"""

from pathlib import Path 
from tempfile import NamedTemporaryFile
import webbrowser as wb

from domible.elements import BaseElement 
from domible.elements import Html


def open_in_browser(htmlDoc: Html) -> None:
    """create temp file to use webbrowser to open passed in Html doc"""
    path =NamedTemporaryFile(delete=False, suffix='.html')
    f=open(path.name, 'w+t')
    f.write(f"{htmlDoc}")
    f.close()
    wb.open('file://' + path.name)


def save_to_file(element: BaseElement, filename: str, force: bool = False) -> None:
    """ 
    save the passed in element to passed in filename.
    If the file name exists and is a regular file, 
    save will fail unless force is Tru 
    """
    fp = Path(filename)
    if fp.exists():
        # if the file exists, is a regular file and force is true, carry on
        # otherwise, raise a FileExists error
        if not  fp.is_file() or not force:
            raise FileExistsError(f"{filename} exists and is not a regular file, or force is False")
    # if file does exists, force must be True
    with fp.open('w+t') as f:
        f.write(f"{element}")


## end of file
