""" domible/src/dicli/main.py 
"""

import logging
import jsonloggeriso8601datetime as jlidt

jlidt.setConfig()
logger = logging.getLogger(__name__)


import typer
app = typer.Typer()

import dicli.mdnElements as mdnElements  

from domible.elements import Html, Head, Body, Title, Base
from domible.elements import (
    UnorderedList,
    OrderedList,
    DescriptionList,
    ListItem,
    DListItem,
    DescriptionTerm,
    DescriptionDef,
)
from domible.elements import Heading, Anchor, Paragraph
from domible.builders.tableBuilder import TableBuilder, build_table_from_dicts
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_in_browser 


#######
@app.command()
def simple() -> None:
    """
    generate, and show in browser,
    a very simple HTML document
    """
    title = "BareBones with a Minimal Body"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(
        [
            Heading(1, title),
            Paragraph("Really, this is all you're going to get."),
            Paragraph(
                f'You might find more interesting content at {Anchor(href="https://blindgumption.com", contents="the Blind Gumption Website")}'
            ),
        ]
    )
    open_html_in_browser(htmlDoc)


#######
@app.command()
def elements(
    mdn_base_url: str = typer.Option("https://developer.mozilla.org", "-u", "--url_mdn"),
    lang: str = typer.Option("en-US", "-l", "--lang"),
    outputfile: str = typer.Option(None, "-o", "--outputfile")
) -> None:
    """
    elements is used to test, and provide an example of, Table and the tableBuilder
    it will scrape HTML element reference info from MDN and present it in a table in your default browser
    The HTML is also saved to a passed in file, not saved if no file specified.
    """
    if outputfile:
        typer.echo(f"saving html output to file: {outputfile}")
    title = "Tables of HTML Elements Scraped from MDN "
    htmlDoc = basic_head_empty_body(title, lang)
    head = htmlDoc.get_head_element()
    head.add_content(Base(href=mdn_base_url))
    body = htmlDoc.get_body_element()
    (currentElementsTable, deprecatedElementsTable) = mdnElements.getElementsTables(mdn_base_url, lang)
    if not currentElementsTable or not deprecatedElementsTable:
        body.add_content(Heading(1, f"failed to scrape elements from {mdnElements.MdnAnchor}"))
    else:
        # building up the body of the html document
        currentTable, _, _ = currentElementsTable.get_table()
        deprecatedTable, _, _ = deprecatedElementsTable.get_table()
        body.add_content(
            [
                Heading(1, title),
                Paragraph(
                    f"Information in the below tables was scraped from {mdnElements.MdnAnchor}."
                ),
                Heading(2, "Currently Supported HTML Elements"),
                currentTable,
                Heading(2, "Deprecated HTML Elements"),
                deprecatedTable,
            ]
        )
    open_html_in_browser(htmlDoc)


#######
@app.command()
def ctfd(
    lower: int = typer.Option(1, "-l", "--lower"),
    upper: int = typer.Option(10, "-u", "--upper"),
):
    """
    to test the buildTableFromDicts function from tableBuilder
    """
    rows = []
    for x in range(lower, upper + 1):
        row = {"base": x}
        row.update(dict([(y, x**y) for y in range(lower, upper + 1)]))
        rows.append(row)
    ## we have a matrix, now display it in an HTML table
    table = build_table_from_dicts("base number raised to column heading number", rows)
    title = f"Testing createTableFromDicts function in tableBuilder, lower is {lower}, upper is {upper}"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(
        [
            Heading(1, title),
            Heading(2, "Raise base to power (column heading number)"),
            table,
        ]
    )
    open_html_in_browser(htmlDoc)


#######
@app.command()
def lists():
    """
    Testing/example of using the lists related elements
    Note how elements are created using composition

    we're testing three types of lists, so let's make some coffee:
    unordered (ul) - stuff we need to make the coffee
    ordered (ol) - steps to make the coffee
    definition (dl) - some details regarding the supplies
    """
    typer.echo("testing lists")
    starbucks = Anchor(
        href="https://www.starbucks.com/menu/at-home-coffee/via-instant",
        contents="Starbucks Via instant coffee",
    )
    suppliesHeading = Heading(2, "Coffee Making Supplies")
    suppliesList = UnorderedList(
        [
            ListItem(f"coffee is from {starbucks}"),
            ListItem("knock-over resistant large coffee mug"),
            ListItem("Sugar"),
            ListItem("spoon to stir"),
            ListItem(
                "Liquid level detector, plays 'Small World' when fluid reaches the probes."
            ),
            ListItem("Hot/near boiling water, from dispenser on counter."),
            ListItem("milk, real or oat, whatever is in the fridge"),
        ]
    )
    suppliesList.attr_value("aria-labelledby", suppliesHeading.id())
    oooHeading = Heading(2, "Order Of Operations")
    oooList = OrderedList(
        [
            ListItem("Collect Supplies"),
            ListItem(UnorderedList(
                [
                    ListItem("coffee from pantry, 3 packets.  Oh, and the sugar too"),
                    ListItem("mug from drying rack"),
                    ListItem("scissors from 'junk drawer'"),
                ]
            )),
            ListItem("cut tops off coffee packets and empty contents into mug"),
            ListItem(
                "don't forget to throw empty packets in the trash, and put the scissors back where you found them"
            ),
            ListItem(
                "pour one scoop of sugar into mug, make sure no one is  watching how much sugar is used, no need to invite commentary from others"
            ),
            ListItem(
                "add hot water, amount based on listening to how full the mug sounds"
            ),
            ListItem("put level detector on rim of mug"),
            ListItem("add 'milk' until hearing high pitched 'Small World'"),
            ListItem("remove sensor from rim, wipe off probes, put back in drawer"),
            ListItem("stir"),
            ListItem(
                "microwave coffee for 1 minute, the 'milk' cooled it down too much"
            ),
            ListItem(
                "stir again after microwave.  make sure 'milk' is back in the fridge"
            ),
            ListItem("sit on stool at counter, start podcast, enjoy the coffee"),
        ]
    )
    oooList.attr_value("aria-labelledby", oooHeading.id())
    detailsHeading = Heading(2, "More Details (because I need to test the dl list)")
    detailsList = DescriptionList(
        [
            DListItem(
                [DescriptionTerm("The Coffee")],
                DescriptionDef(
                    f"I get the {starbucks} from Amazon as a subscription in the 50 count packet.  That's about as cheap as I can find it"
                ),
            ),
            DListItem(
                [DescriptionTerm("The Sugar")],
                DescriptionDef(
                    "It's, I think, the Tabago raw sugar from Trader Joe's.  it looks healthy and sounds exotic"
                ),
            ),
            DListItem(
                [DescriptionTerm("Real Milk"), DescriptionTerm("Oat Milk")],
                DescriptionDef(
                    "Why is cow's milk considered 'real'?  Or am I simply calling this out to have multiple <dt> elements for this entry?"
                ),
            ),
            DListItem(
                [DescriptionTerm("Why The list?")],
                DescriptionDef(
                    "I don't like having to use a list for dt elements, I should change that interface"
                ),
            ),
        ]
    )
    detailsList.attr_value("aria-labelledby", detailsHeading.id())
    title = "Testing Domible Lists"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(
        [
            Heading(1, "Makin' Coffee, the Coffeenator"),
            suppliesHeading,
            suppliesList,
            oooHeading,
            oooList,
            detailsHeading,
            detailsList,
        ]
    )
    open_html_in_browser(htmlDoc)


#######
@app.command()
def headings():
    """
    test the creation and display of HTML headings.
    this also shows how to add attributes to elements
    Note heading level 0 and 7 do not result in legit headings to the screen reader
    For now, to verify attributes, you'll need to view source in your browser
    """
    typer.echo("testing heading generation")
    title = "Domible testing Heading Element"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(Heading(1, title))
    for lvl in range(0, 8):
        body.add_content(Heading(level=str(lvl), contents=f"Heading with Level: {lvl}"))
    body.add_content(
        Heading(
            level=1,
            contents=Anchor(
                href="https://blindgumption.com",
                contents="Blind Gumption",
                **{"class": "classValue", "id": "uniqueId"},
            ),
        )
    )
    body.add_content(
        Heading(
            className="someClass",
            level=2,
            contents="heading level 2 with someClass classname",
        )
    )
    body.add_content(
        Heading(
            className="<someClass>",
            level=2,
            contents="heading level 2 with <someClass> classname",
        )
    )
    body.add_content(
        Heading(
            uniqueId="somethingUnique",
            level=3,
            contents="heading level 3 with somethingUnique for unique",
        )
    )
    body.add_content(
        Heading(
            uniqueId="'somethingUnique'",
            level=3,
            contents="heading level 3 with 'somethingUnique' for unique",
        )
    )
    open_html_in_browser(htmlDoc)


#######
@app.callback(invoke_without_command=True)
def main() -> None:
    typer.echo(
        "that's it for main"
    )


## end of file
