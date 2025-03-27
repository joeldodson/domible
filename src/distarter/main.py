""" domible/src/distarter/main.py 

this file serves as Python code to get started with domible
"""

import domible
from domible.elements import Html, Body, Title
from domible.elements import Heading, Anchor, Paragraph, HorizontalRule 
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_document_in_browser


#######
def run() -> None:
    """
    generate, and show in browser,
    a very simple HTML document
    """
    title = "BareBones with a Minimal Body, though getting less minimal as I use this for testing..."
    cib_anchor = Anchor(
        href="http://codinginblind.vip", contents="the Coding In Blind website"
    )
    version = domible.__version__
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content([
        Heading(1, title),
        Paragraph(f"using domible version {version}"),
        Paragraph(f"check out: {cib_anchor}"),
        HorizontalRule(),
        Paragraph('Adding a non printable character, codepoint = 0xfeff, in the square brackets [\ufeff] to make sure encodings are set correctly.')
    ])
    open_html_document_in_browser(htmlDoc)


if __name__ == "__main__":
    run()

## end of file
