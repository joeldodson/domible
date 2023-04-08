"""  domible/src/domible/elements/tables.py
it's all about HTML tables in here
And HTML tables are ONLY for presenting tabular data.
If you use any of these table related elements to format the layout of your document,
you should be hunted down and ... well, something unpleasant ought to happen to you 
considering the audible pain you've inflicted on screen reader users 
it's 2022, use  CSS for layout and formatting  
"""

from typing import List, Any

from .baseElements import BaseElement


#######
class TableData(BaseElement):
    """ create a td element """

    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag='td', contents=contents, **kwArgs)


#######
class TableHeader(BaseElement):
    """ create a th element """

    def __init__(self, contents: Any, **kwArgs):
        super().__init__('th', contents, **kwArgs)


#######
class TableColumnHeader(TableHeader):
    """ creates a th element with attribute scope="col" added by default.
    This is most likely used for th elements in the first row of the table.
    By setting the scope attribute to col, 
    a screen reader will read out the column names as the user explores a row. 
    """
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(contents, scope='col', **kwArgs)


#######
class TableRowHeader(TableHeader):
    """ creates a th element with attribute scope="row" added by default.
    This is most likely used for th elements in the first column of the table.
    By setting the scope attribute to row, 
    a screen reader will read out the row names as the user explores a column. 
    """
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(contents, scope='row', **kwArgs)


#######
class TableRow(BaseElement):
    """ creates a tr element.
    Note the tr element contains a list of th and/or td elements.
    The th/td elements can be provided at creation time,
    or added later via instance methods to add content.
    """
    def __init__(self, cells: List[Any] = None, **kwArgs):
        """
        cells should be a list of th or td elements 
        """
        super().__init__('tr', cells, **kwArgs)


"""
classes TableHead, TableBody, and TableFoot differ in only the four letters after the 't' for the tag string
hopefully there are no cut'n'paste errors here...
"""
#######


class TableHead(BaseElement):
    """ creates a thead element.
    Note the thead element contains a list of tr elements.
    The tr elements can be provided at creation time,
    or added later via instance methods to add content.
    """
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__(tag='thead', elements=rows, **kwArgs)


#######
class TableBody(BaseElement):
    """ creates a tbody element.
    Note the tbody element contains a list of tr elements.
    The tr elements can be provided at creation time,
    or added later via instance methods to add content.
    """
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__(tag='tbody', elements=rows, **kwArgs)


#######
class TableFoot(BaseElement):
    """ creates a tfoot element.
    Note the tfoot element contains a list of tr elements.
    The tr elements can be provided at creation time,
    or added later via instance methods to add content.
    """
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__(tag='tfoot', elements=rows, **kwArgs)


#######
class Caption(BaseElement):
    """ creates a caption element. """
    def __init__(self, contents: Any, **kwArgs):
        if not contents:
            raise ValueError("a Caption must have some contents")
        super().__init__(tag='caption', contents=contents, **kwArgs)


#######
class Table(BaseElement):
    """ creates the table element."""
    def __init__(self, caption: Caption, contents: List[Any] = None, **kwArgs):
        """
        a caption is not required in a table, here's where I start to get opinionated.
        And this opinion is toward accessibility.
        Tables with captions are nice when using single letter navigation.
        If I type 't' to go to the next table, I generally have to arrow up to understand what is in the table.
        A caption howerver will be read to me after typing 't' and landing on the next table.
        """
        if not caption:
            raise ValueError(
                "WTF, gives us a real caption for this Table my precious")
        self.caption = caption
        # make sure caption is first on the contents list so it gets rendered by the base __repr__
        contents = [caption] + contents if contents else [caption]
        super().__init__(tag='table', elements=contents, **kwArgs)


## end of file