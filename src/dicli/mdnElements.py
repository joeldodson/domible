""" /domible/src/dicli/mdnElements.py
code to get HTML elements reference from MDN
used by getTableData 

this module is very specific to the layout of the MDN HTML reference pages

As the MDN site is scraped, a TableInfo object is constructed with a row for each element.
The complete TableInfo is returned to the caller 
"""

import logging

logger = logging.getLogger(__name__)

from os import path

from bs4 import BeautifulSoup as BSoup
from bs4.element import Tag
from markupsafe import escape
import requests
from typing import Dict, Tuple

from domible.elements import Anchor
from domible.builders.tableBuilder import TableInfo, RowInfo


mdnLocalPathPrefix = "/en-US/docs/Web"
elementsReferencePath = "/en-US/docs/Web/HTML/Element"
mdnHostUrlBase = "https://developer.mozilla.org"
elementsReferenceUrl = f"{mdnHostUrlBase}{elementsReferencePath}"
mdnAnchor = Anchor(
    elementsReferenceUrl,
    "HTML elements reference page on Mozilla Developer Network (MDN)",
)


#######
def updateLocalAnchorHref(tag: Tag) -> BSoup:
    anchors = tag.find_all("a")
    for a in anchors:
        href = a.get("href")
        if href and href.startswith(mdnLocalPathPrefix):
            a["href"] = f"{mdnHostUrlBase}{href}"


#######
def filterAnchor(anchor: Tag) -> bool:
    """
    for each element, there is a page with a url of the form:
        elementsReferenceUrl/<element_name>
    there are other anchors on the base MDN HTML reference page though with a similar base path
    there is also an anchor with href that looks like its fro an element called 'contributors.txt', filter that out too
    This filter is to ensure we get only the anchors referencing HTML elements
    """
    href = anchor.attrs.get("href")
    if not href or elementsReferencePath not in href or "contributors.txt" in href:
        return False
    elif path.split(href)[0] != elementsReferencePath:
        return False
    else:
        return True


#######
def getElementSummary(soup: BSoup) -> Dict:
    """the summary is in the first <p> element immediately after the only <h1> element in the doc"""
    summary = soup.find("h1").next_sibling.find("p")
    updateLocalAnchorHref(summary)
    ## summary = str(escape(summary.encode()))
    return {"Summary": summary.decode()}


#######
def getElementInfo(name: str, url: str) -> Dict:
    """
    request.get the page for the element
    then parse it to find what we're looking for
    """
    logger.info(f"getting info for element {name}")
    elmDoc = requests.get(url)
    elmSoup = BSoup(elmDoc.content, "html.parser")
    entries = getElementSummary(elmSoup)
    return entries


#######
def getElementsTables(outfile: str) -> Tuple[TableInfo, TableInfo]:
    try:
        refPage = requests.get(elementsReferenceUrl)
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
            elmUrl = f"{mdnHostUrlBase}{elmPath}"
            elmName = path.split(elmUrl)[1]
            rowEntries = getElementInfo(elmName, elmUrl)
            row = RowInfo(Anchor(elmUrl, elmName), rowEntries)
            if "Deprecated" in rowEntries.get("Summary"):
                deprecatedElementsTable.addRow(row)
            else:
                currentElementsTable.addRow(row)
        with open(outfile, "w") as of:
            tsp = BSoup(str(currentElementsTable.getTable()), "html.parser")
            of.write(tsp.prettify())
            tsp = BSoup(str(deprecatedElementsTable.getTable()), "html.parser")
            of.write(tsp.prettify())
    except Exception as exc:
        logger.exception("something bad happened while scraping MDN")
        return (None, None)
    return (currentElementsTable, deprecatedElementsTable)


## end of file
