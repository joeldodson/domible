#!/usr/bin/env python
""" domible/src/dicli/main.py 
simple command line tool to test/experiment with domible 
"""

import logging
import jsonloggeriso8601datetime as jlidt

jlidt.setConfig()
logger = logging.getLogger(__name__)

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
from domible.tools import open_html_document_in_browser

import argparse

global_parser = argparse.ArgumentParser(
    prog="dicli",
    description="command line utility for domible testing",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Cheers!",
)


def simple(args) -> None:
    """create a very simple HTML document and open it in the default browser"""
    title = "BareBones with a Minimal Body"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content(
        [
            Heading(1, title),
            Paragraph("Really, this is all you're going to get."),
            Paragraph(
                f'You might find more interesting content at {Anchor(href="https://joeldodson.github.io/codinginblind", contents="Coding in Blind website")}'
            ),
        ]
    )
    open_html_document_in_browser(htmlDoc)


def elements(args) -> None:
    """
    elements is used to test, and provide an example of, Table and the tableBuilder
    it will scrape HTML element reference info from MDN and present it in a table in your default browser
    The HTML is also saved to a passed in file, not saved if no file specified.
    """
    mdn_base_url: str = args.url_mdn
    lang: str = args.lang
    outputfile: str = args.outfile

    if outputfile:
        print(f"saving html output to file: {outputfile}")
    title = "Tables of HTML Elements Scraped from MDN "
    htmlDoc = basic_head_empty_body(title, lang)
    head = htmlDoc.get_head_element()
    head.add_content(Base(href=mdn_base_url))
    body = htmlDoc.get_body_element()
    (currentElementsTable, deprecatedElementsTable) = mdnElements.getElementsTables(
        mdn_base_url, lang
    )
    if not currentElementsTable or not deprecatedElementsTable:
        body.add_content(
            Heading(1, f"failed to scrape elements from {mdnElements.MdnAnchor}")
        )
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
    open_html_document_in_browser(htmlDoc)


def ctfd(args) -> None:
    """
    to test the buildTableFromDicts function from tableBuilder
    """
    lower: int = args.lower
    upper: int = args.upper
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
    open_html_document_in_browser(htmlDoc)


def lists(args) -> None:
    """
    Testing/example of using the lists related elements
    Note how elements are created using composition

    we're testing three types of lists, so let's make some coffee:
    unordered (ul) - stuff we need to make the coffee
    ordered (ol) - steps to make the coffee
    definition (dl) - some details regarding the supplies
    """
    print("testing lists")
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
            ListItem("Liquid level detector"),
            ListItem("Hot/near boiling water, from dispenser on counter."),
            ListItem("milk, real or oat, whatever is in the fridge"),
        ]
    )
    suppliesList.add_content(ListItem("testing add_content"))
    suppliesList.attr_value("aria-labelledby", suppliesHeading.id())
    oooHeading = Heading(2, "Order Of Operations")
    oooList = OrderedList(
        [
            ListItem("Collect Supplies", **{"x-test": "collect-supplies"}),
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
    supplies_sublist = UnorderedList(
        [
            ListItem("coffee from pantry, 3 packets.  Oh, and the sugar too"),
            ListItem("mug from drying rack"),
            ListItem("scissors from 'junk drawer'"),
        ]
    )
    oooList.add_sublist(supplies_sublist, attributes={"x-test": "collect-supplies"}, before = False)
    hidden_sublist = UnorderedList([
        ListItem("what to do when you're trying to quietly drink your coffee, and someone wants to talk to you"),
        ListItem("take your coffee to a ruum in the house that is traditionally quiet and people leave you alone"),
        ListItem("It's okay to bring your toast/muffin/biscotti as well")
    ])
    oooList.add_sublist(hidden_sublist.get_collapsible("our little secret"))
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
    open_html_document_in_browser(htmlDoc)


def list_builder(args) -> None:
    """ """
    title = "Testing Domible List builder"
    htmlDoc = basic_head_empty_body(title)
    body = htmlDoc.get_body_element()
    body.add_content([])
    open_html_document_in_browser(htmlDoc)


def headings(args) -> None:
    """
    test the creation and display of HTML headings.
    this also shows how to add attributes to elements
    Note heading level 0 and 7 do not result in legit headings to the screen reader
    For now, to verify attributes, you'll need to view source in your browser
    """
    print("testing heading generation")
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
    open_html_document_in_browser(htmlDoc)


def run() -> None:
    subparsers = global_parser.add_subparsers(
        required=True, help="sub commands for dicli"
    )

    simple_parser = subparsers.add_parser("simple", help=simple.__doc__)
    simple_parser.set_defaults(func=simple)

    elements_parser = subparsers.add_parser("elements", help=elements.__doc__)
    elements_parser.add_argument(
        "-u", "--url_mdn", default="https://developer.mozilla.org"
    )
    elements_parser.add_argument("-l", "--lang", default="en-US")
    elements_parser.add_argument("-o", "--outfile")
    elements_parser.set_defaults(func=elements)

    ctfd_parser = subparsers.add_parser("ctfd", help=ctfd.__doc__)
    ctfd_parser.add_argument("-l", "--lower", default=1, type=int, help="lower bound")
    ctfd_parser.add_argument("-u", "--upper", default=10, type=int, help="upper bound")
    ctfd_parser.set_defaults(func=ctfd)

    lists_parser = subparsers.add_parser("lists", help=lists.__doc__)
    lists_parser.set_defaults(func=lists)

    headings_parser = subparsers.add_parser("headings", help=headings.__doc__)
    headings_parser.set_defaults(func=headings)

    args = global_parser.parse_args()
    args.func(args)


## end of file
