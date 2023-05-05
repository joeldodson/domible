""" /domible/src/dicli/mdnElements.py
code to get HTML elements reference from MDN
used by getTableData 

this module is very specific to the layout of the MDN HTML reference pages

As the MDN site is scraped, TableInfo objects are constructed with a row for each element.
A table for current elements and one for deprecated is constructed.

Yes, this has devolved into much hackery.
I should turn this in to a class and use properties
and get rid of the globals.
The globals were initially hard coded "const" values.
When mdn_base_url and lang (language) became parameters, the conts became globals
Someday... I'll fix this??  
"""

import logging

logger = logging.getLogger(__name__)

from os import path

from bs4 import BeautifulSoup as BSoup
from bs4.element import Tag
import requests
from typing import Dict, Tuple

from domible.elements import Anchor
from domible.builders.tableBuilder import TableInfo, RowInfo


MdnLocalPathPrefix = "" 
ElementsReferencePath = ""
MdnHostUrlBase = ""
ElementsReferenceUrl = f"{MdnHostUrlBase}{ElementsReferencePath}"
MdnAnchor = None 


def updateInPageAnchorHref(soup: BSoup, elemUrl: str) -> None:
    """
    any anchors with href to local id, 
    e.g., href="#somewherein page"
    need to be updated to an absolute (because absolute is the url I have) href
    """ 
    anchors = soup.find_all("a")
    for a in anchors:
        href = a.get("href")
        if href and href.startswith("#"):
            a["href"] = f"{elemUrl}{href}"


def filterAnchor(anchor: Tag) -> bool:
    """
    for each element, there is a page with a url of the form
    ElementsReferenceUrl/<element_name>
    there are other anchors on the base MDN HTML reference page though with a similar base path
    there is also an anchor with href that looks like its fro an element called 'contributors.txt', filter that out too
    This filter is to ensure we get only the anchors referencing HTML elements
    """
    href = anchor.attrs.get("href")
    if not href or ElementsReferencePath not in href or "contributors.txt" in href:
        return False
    elif path.split(href)[0] != ElementsReferencePath:
        return False
    else:
        return True


def getElementSummary(soup: BSoup) -> Dict:
    """
    find the summary in the document,
    pull out the redundant html anchor,
    and return the rest

    NOTE: this method hard codes knowledge of the format of the document.
    e.g., the summary is the first paragraph after the only heading 1,
    and the html anchor is the first anchor in that paragraph,
    except for the canvas element, now I have to check the contents.
    """
    summary = soup.find("h1").next_sibling.find("p")
    anchor = summary.find('a')
    if anchor.text == "HTML":
        anchor.extract()
    return {"Summary": summary.decode()}


def getElementSpecificationReference(soup: BSoup) -> Dict:
    pass


def getElementTechnicalSummary(soup: BSoup) -> Dict:
    pass


def getElementDetails(soup: BSoup, elemUrl: str) -> Dict:
    """
    get all the information from the element's html page we want for the table
    A high level summary is in the first <p> element immediately after the only <h1> element in the doc
    A technical summary is in the first table.
    we'll use the first column as column headers for the table we're building.
    The second column is the values
    The second table in the doc has a link to the specification for the element.
    """
    result = dict()
    if d := getElementSummary(soup):
        result.update(d)
    if d := getElementSpecificationReference(soup):
        result.update(d)
    if d := getElementTechnicalSummary(soup):
        result.update(d)
    return result 


def getElementInformation(elemName: str, elemUrl: str) -> Dict:
    """
    request.get the page for the element
    then parse it to find what we're looking for
    """
    try:
        elemDoc = requests.get(elemUrl)
        elemSoup = BSoup(elemDoc.content, "html.parser")
        updateInPageAnchorHref(elemSoup, elemUrl)
        entries = getElementDetails(elemSoup, elemUrl)
        return entries
    except Exception:
        logger.exception(f"failed while getting info for element {elemName}")
        return dict()


def getElementsTables(mdnBaseUrl: str, lang: str) -> Tuple[TableInfo, TableInfo]:
    global MdnLocalPathPrefix, ElementsReferencePath, MdnHostUrlBase, ElementsReferenceUrl, MdnAnchor 
    MdnLocalPathPrefix = f"/{lang}/docs" ## was  "/en-US/docs/Web"
    ElementsReferencePath = f"{MdnLocalPathPrefix}/Web/HTML/Element"  ## was "/en-US/docs/Web/HTML/Element"
    MdnHostUrlBase = mdnBaseUrl  ## was "https://developer.mozilla.org"
    ElementsReferenceUrl = f"{MdnHostUrlBase}{ElementsReferencePath}"
    MdnAnchor = Anchor(
        ElementsReferenceUrl,
        "HTML elements reference page on Mozilla Developer Network (MDN)",
    )

    try:
        refPage = requests.get(ElementsReferenceUrl)
        soup = BSoup(refPage.content, "html.parser")
        anchors = soup.find_all("a")
        elems = list(
            set([a.attrs.get("href").lower() for a in anchors if filterAnchor(a)])
        )
        elems.sort()
        logger.info(f"number of element references is {len(elems)}")
        # we have links to each element,
        # time to scrape each page and create rows for each element
        currentElementsTable = TableInfo(
            caption="Current HTML Elements", rowHeadingName="Element"
        )
        deprecatedElementsTable = TableInfo(
            caption="Deprecated HTML Elements", rowHeadingName="Element"
        )
        for elmPath in elems:
            elmUrl = f"{MdnHostUrlBase}{elmPath}"
            elmName = path.split(elmUrl)[1]
            rowEntries = getElementInformation(elmName, elmUrl)
            row = RowInfo(Anchor(elmUrl, elmName), rowEntries)
            if "Deprecated" in rowEntries.get("Summary"):
                deprecatedElementsTable.addRow(row)
            else:
                currentElementsTable.addRow(row)
    except Exception:
        logger.exception("something bad happened while scraping MDN")
        return (None, None)
    return (currentElementsTable, deprecatedElementsTable)


## end of file
