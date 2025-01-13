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
from domible.elements import Html, Body, Heading 
from domible.builders import element_from_object, default_toggle_details_button  
from domible.starterDocuments import basic_head_empty_body 


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
        if not fp.is_file() or not force:
            raise FileExistsError(
                f"{filename} exists and is not a regular file, or force is False"
            )
    # if file does exists, force must be True
    with fp.open("w+t", encoding="utf-8") as f:
        f.write(f"{element}")


def open_html_in_browser(html_doc: Html, save_file: str = None, force: bool = False) -> None:
    """
    open the html_doc in the default browser.
    if a save_to_file is provided, also save the html_doc to that file,
    else use a temporary file 
    """
    if save_file:
        save_to_file(html_doc, save_file, force)
        # path must be absolute to match how temp file works 
        path = str(Path(save_file).absolute()) 
    else: 
        path =NamedTemporaryFile(delete=False, suffix='.html')
        f=open(path.name, 'w+t', encoding='utf-8')
        f.write(f"{html_doc}")
        f.close()
        path = path.name # consistent with path from saving file 
    wb.open('file://' + path)


def open_object_in_browser(obj: object, depth:int = 42, title: str = "opening an object in the browser", save_file: str = None, force: bool = False) -> None:
    """
    get HTML representation of the object then open it in the default browser.

    the passed in object is used to get HTML using element_from_object.
    That HTML is then put into a simple HtML document using the basicHeadEmptyBody starter document.
    that simple document is then opened in the browser. 
    """
    obj_html = element_from_object(obj, depth)
    html_doc: Html  = basic_head_empty_body(title)
    body: Body = html_doc.get_body_element() 
    body.add_content([Heading(1, f"showing object of type {type(obj).__name__}"), default_toggle_details_button()])
    body.add_content(obj_html)
    open_html_in_browser(html_doc, save_file, force)


## end of file
