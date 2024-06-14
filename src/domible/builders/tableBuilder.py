""" domible/src/domible/builders/tableBuilder.py

The tableBuilder module is the first attempt at providing some level of abstraction to creating a more complicated HTML element. 
dataclasses are used to represent HTML table related elements using any datatypes. 
RowInfo and TableInfo classes have properties with semantics indicating their use within the table.
The specific HTML elements used to construct the table are encapsulated within the classes.  

The user can create the rows however they like then add them to the TableInfo object.

There is a correlation between the dict defining a row and dict defining the column headings in the TableInfo.
That correlation is in the keys of the dicts.
The dict defining the column headings defines which values within a row are included in the table.
Thus a row can be a dict with an arbitrary list of key, value pairs.
Then what is included in a table is defined by the column headings dict.
When a table is being generated from TableInfo,
the keys from the column headings dict is sent to each RowInfo.
The RowInfo object uses that to get the value for the cell for that column.
If the RowInfo entries dict has a matching key, the associated value is used for that cell (a <td> element.)
If there is no matching key, the cell will be empty (or use None) for that row for that column .
The RowInfo entries dict can have entries that are not included in a specific table.
That will be the case when the table column IDs are a subset of the keys in the RowInfo entries dict. 

The values in the column headings dict can be used to have custom names for the column headings. 
The default name of the column heading is the key itself, e.g.:
columnHeadings = {'col1':'col1', 'col2':'col2', ... }
to use better names for the column headings, try something like:
customColumnHeadings = {'col1':'Column One', 'col2':'Column Two', ... }
"""


import logging

logger = logging.getLogger(__name__)

from dataclasses import dataclass, field
from typing import Any, Dict

from domible.elements import (
    Caption,
    Table,
    TableRow,
    TableData,
    TableColumnHeader,
    TableRowHeader,
    TableHead,
    TableBody,
    Style,
    Script,
)


#######
@dataclass
class RowBuilder:
    """
    RowBuilder has the values for the cells of the row stored as a dict (with the row heading called out separately)
    the key in the entries dict is the column id, the value is what will eventually be in the <th> or <td> elements
    the first item is called out as the heading for that row mainly as an API feature.
    """

    heading: Any = "you need to set the row heading"
    # this is how **kwArgs works in dataclasses
    # to ensure each instantiation gets its own object,
    # not a reference to a dict shared by all RowInfo objects
    entries: Dict = field(default_factory=dict)

    #####
    def add_entries(self, **kwArgs) -> None:
        """
        add entries to the row by passing in any number of named parameters (columnId = 'some value').
        the Ids represent the columns,
        the value is the entry in that column for this row
        """
        if self.entries:
            self.entries.update(kwArgs)
        else:
            self.entries = kwArgs

    #####
    def properties(self) -> list[Any]:
        """
        The properties are the keys from the entries in this row.
        The keys are used to identify which values from a row are used in a particular table.
        """
        if self.entries:
            return list(self.entries.keys())
        else:
            return []

    #####
    def get_row(self, columns: list[Any]) -> TableRow:
        """
        return the TableRow object that can generate the HTML for the row
        the columns parameter is needed to know which values from entries to include in the row
        """
        rowCells = [TableRowHeader(self.heading)]
        rowCells += [TableData(self.entries.get(col)) for col in columns]
        """
        rowCells is now a list of Elements (representing <th> and <td> elements)
        it can be used to create a TableRow (representing a <tr> element) object 
        """
        return TableRow(rowCells)


#######
@dataclass
class TableBuilder:
    """
    an object of TableBuilder holds all the information needed to generate an HTML table
    """

    caption: Any
    # the 0th column, i.e., the column of row headings
    # the upper left cell, 0,0.
    # Hopefully this is set to something meaningful by the user of this class.
    row_heading_name: Any = "Row Names"
    column_headings: Dict = field(default_factory=dict)
    rows: list[RowBuilder] = field(default_factory=list)

    #####
    def add_row(self, row: RowBuilder) -> None:
        self.rows.append(row)

    #####
    def generate_column_headings(self) -> None:
        """
        if you don't want to set the column headings directly, they can be inferred by the names of properties in the rows

        this method will iterate through the rows and keep track of the property name (key) of each item (key, value pair) in a row
        The columns can then be arranged based on the position of the propertys in the rows (the default),
        or another option can be specified (TODO)
        """
        counts = {}
        for row in self.rows:
            for prop in row.properties():
                if not counts.get(prop):
                    counts[prop] = 1
                else:
                    counts[prop] += 1
        # for now, column headings are all the properties found in the rows
        # TODO: allow the user to specify ordering of the columns based on counts
        #    or maybe columnHeadings.sort()
        # self.columnHeadings = list(counts.keys())
        self.column_headings = {key: key for key in counts.keys()}

    #####
    def get_table(self) -> tuple[Table, Style, Script]:
        """
        need to go through self (TableInfo) and convert all the info
        to corresponding elemensts (tr, th, td, caption...)
        """
        logger.debug(f"getting table with caption {self.caption}")
        table = Table(Caption(self.caption))
        # first add the column headings to the table
        # if column headings hve not been set yet, generate them based on the  rows
        if len(self.column_headings) == 0:
            self.generate_column_headings()
        columnNames = [self.row_heading_name] + list(self.column_headings.values())
        logger.debug(
            f"table with caption {self.caption}, has column heading names:\n {columnNames}"
        )
        """
        split this to multiple lines for readability 
        first add the table head <thead> element to the table.
        a <thead> is a list of rows though in this case it's a single row of the names of the columns
        a TableRow is a list of anything derived from TableData <td> or TableHeader <th> elements 
        """
        table.add_content(
            TableHead(
                [
                    TableRow(
                        # list comprehension to initiate the TableRow
                        [TableColumnHeader(colName) for colName in columnNames]
                    )  # close of TableRow construction
                ]
            )  # close TableHead construction including close list for list of TableRows to construct TableHead
        )  # close of addContent
        """
        now add all the rows in the tbody element 
        same idea as adding the TableHead above 
        """
        table.add_content(
            TableBody(
                [row.get_row(list(self.column_headings.keys())) for row in self.rows]
            )
        )
        return table, None, None


#######
def build_table_from_dicts(caption: Any, rows: list[Dict]) -> Table:
    """
    this is, so far, the easiest way to construct an HTML table from data the user has pulled from anywhere
    The rows are the dicts in the list, in order they appear in the list
    the column names are derived from the keys in the dicts
    the row heading is the value from the first item in the dict representing that row
    and the heading for the first column (column of row headings) in the table is the key from the first key, value  pair from the first dict in the list

    Using this a developer doesn't need to know anything about generating HTML tables, especially accessibility
    it's all about defaults...
    Caveat, I've only used this for lists of very consistent dicts,
    that is, they all have the same size and keys.
    It's likely this fails quickly for random dicts in a list
    That is, if the dicts represent, say a very sparsely populated table, dicts with different keys with little overlap
    this table might not be what you want.
    It's better to use the TableInfo and RowInfo dataclasses
    """
    if len(rows) == 0:
        raise ValueError("no rows sent to createTableFromDict")
    row_heading_name = list(rows[0].keys())[0]
    tbuilder = TableBuilder(caption, row_heading_name)
    for row in rows:
        items = list(row.items())
        heading = items[0][1]
        entries = dict(items[1:])
        ri = RowBuilder(heading, entries)
        tbuilder.add_row(ri)
    return tbuilder.get_table()


# end of file
