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
from random import random 
from time import sleep 

from bs4 import BeautifulSoup as BSoup
from bs4.element import Tag
import requests
from typing import Dict, Tuple

from domible.elements import Anchor
from domible.builders.tableBuilder import TableBuilder, RowBuilder


MdnLocalPathPrefix = "" 
ElementsReferencePath = ""
MdnHostUrlBase = ""
ElementsReferenceUrl = f"{MdnHostUrlBase}{ElementsReferencePath}"
MdnAnchor = None 

DomibleIssuesPage = Anchor(href="https://github.com/joeldodson/domible/issues", contents="domible issue page on github")

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
    return True


def getElementSummary(soup: BSoup) -> Dict:
    """
    find and return the summary in the document,

    NOTE: this method hard codes knowledge of the format of the document.
    consider the first paragraph after the main element opening tag,
    and all its sibling paragraphs, to be the summary.
    """
    summary = ""
    try:
        p0 = soup.find("main").find("p")
        summary = p0.decode()
        for el in p0.next_siblings:
            if el.name and el.name == 'p': summary += el.decode()
            elif el.name: break
    except Exception:
        logger.exception("exception while getting summary")
        summary = f"no summary?  that's odd.  Please open an issue at the {DomibleIssuesPage}"
    return {"Summary": summary}


def getElementSpecificationReference(soup: BSoup) -> Dict:
    """
    The element specification is in a table with a single column and two rows.
    The first row is a <thead> with a <th> with the word "Specification"
    The second row is the specification link in a <td> in a <tbody>
    This is generally the second table on the page, but let's not assume that 
    """
    entry = dict()
    for table in soup.find_all('table'):
        if (thead := table.find('thead')) and thead.text.lower() == "specification":
            entry["Specification"] = table.find('tbody').find('td').decode_contents()
    return entry 


thToUseList = []
def findThToUse(th: Tag) -> Tag:
    """
    see notes on getElementTechnicalSummary for why this is here
    And the global hack is the easiest way to fake C like static variables 
    """
    global thToUseList
    for savedTh in thToUseList:
        if savedTh.text.lower() == th.text.lower():
            return savedTh
    thToUseList.append(th)
    return th


def getElementTechnicalSummary(soup: BSoup) -> Dict:
    """
    The page for each element has a two column table with summaries of various topics.
    The first column is the topic, the second is the summary.
    I want the topics to be columns in the table we're creating, the topic summary will be in the row for each element.
    Unfortunately, not all the tables topic columns are consistent.
    If I simply pull out the content of the th, and use that as a key in the dict for the row,
    we end up with multiple columns for what should be the same column.
    For example, "DOM Interface" and "DOM interface" turn into two different columns.
    To address this, the entries from the first element, <a> are saved to be used as keys for all the elements.
    Subsequent element table entries need to be compared against the saved keys. 
    """
    entries = dict() 
    detailstable = soup.find("table", {"class":"properties"})
    if detailstable:
        ths = detailstable.find_all('th')
        tds = detailstable.find_all('td')
        for th,td in zip(ths, tds):
            thToUse = findThToUse(th)
            entries[thToUse.decode_contents()] = td.decode_contents()
    return entries 


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
        return getElementDetails(elemSoup, elemUrl)
    except Exception:
        logger.exception(f"failed while getting info for element {elemName}")
        logger.fatal(f"failed while getting info for element {elemName}")
        exit(1)


def getElementsTables(mdnBaseUrl: str, lang: str) -> Tuple[TableBuilder, TableBuilder]:
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
        currentElementsTable = TableBuilder(
            caption="Current HTML Elements", rowHeadingName="Element"
        )
        deprecatedElementsTable = TableBuilder(
            caption="Deprecated HTML Elements", rowHeadingName="Element"
        )
        for elmPath in elems:
            sleep(random())  # don't get blocked by MDN...
            elemUrl = f"{MdnHostUrlBase}{elmPath}"
            elemName = path.split(elemUrl)[1]
            logger.info(f"getting element {elemName} from path {elemUrl}")
            rowEntries = getElementInformation(elemName, elemUrl)
            row = RowBuilder(Anchor(elemUrl, elemName), rowEntries)
            if "Deprecated" in rowEntries.get("Summary"):
                deprecatedElementsTable.addRow(row)
            else:
                currentElementsTable.addRow(row)
    except Exception:
        logger.exception("something bad happened while scraping MDN")
        return (None, None)
    return (currentElementsTable, deprecatedElementsTable)


## end of file
