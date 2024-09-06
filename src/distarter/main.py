""" domible/src/distarter/main.py 

this file serves as Python code to get started with domible
"""

from domible.elements import Html, Body, Title
from domible.elements import Heading, Anchor, Paragraph
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_in_browser


#######
def run() -> None:
    """
    generate, and show in browser,
    a very simple HTML document
    """
    title = "BareBones with a Minimal Body"
    cib_anchor = Anchor(
        href="http://codinginblind.vip", contents="the Coding In Blind website"
    )
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(
        [
            Heading(1, title),
            Paragraph(f"You might find more interesting content at {cib_anchor}"),
        ]
    )
    open_html_in_browser(htmlDoc)


if __name__ == "__main__":
    run()

## end of file
