""" domible/src/distarter/main.py 

this file serves as Python code to get started with domible
The datetime and webbrowser imports and openPage() funtion 
are not needed to use domible.
They're here only to be able to open the starter page in your default browser.
"""

from datetime import datetime as dt
import webbrowser as wb

from domible.elements import Html, Body, Title
from domible.elements import Heading, Anchor, Paragraph
from domible.starterDocuments import basicHeadEmptyBody


def openPage(htmlDoc: Html) -> None:
    """create temp html file to use webbrowser to open passed in Html doc"""
    thf = f"tmp_html_{dt.timestamp(dt.now())}.html"
    with open(thf, "w") as f:
        f.write(f"{htmlDoc}")
    wb.open(thf)


#######
def run() -> None:
    """
    generate, and show in browser,
    a very simple HTML document
    """
    title = "BareBones with a Minimal Body"
    bga = Anchor(
        href="https://blindgumption.com", contents="the Blind Gumption Website"
    )
    htmlDoc = basicHeadEmptyBody(title)
    body = htmlDoc.getBody()
    body.addContent(
        [
            Heading(1, title),
            Paragraph(f"You might find more interesting content at {bga}"),
        ]
    )
    openPage(htmlDoc)


if __name__ == "__main__":
    run()

## end of file
