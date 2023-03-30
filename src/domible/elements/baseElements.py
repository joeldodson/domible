"""  pymenable//elements/baseElements.py
classes in here are meant to be used to build HTML elements
most of the functionality of an element can be in the base class
The derived classes are mostly responsible for setting the appropriate tag string value 
"""

## from datetime import datetime as dt 
from random import random 
from typing import Dict, List, Any

from markupsafe import escape 

####### 
class ElementList(list):
    """
    this class only exists because __repr__ in BaseElement prints the square brackets 
    when it's generating the HTML for the list objects  
    """
    def __repr__(self):
        listString = ''
        for entry in self:
            listString += f'{entry}\n'
        return listString 


#######
class BaseElement:
    """
    BaseElement holds the tag value and a dict of attrivutes      
    and some methods likely needed by any element 
    """
    def __init__(self, tag: str, contents: Any = None, **kwArgs):
        self.tag = tag
        self.contents = contents
        self.attrs = dict(kwArgs)

    def attrValue(self, attr: str, value: str = None) -> str:
        """
        use this to set a value for a single attribute,
        or to get the value set for the given attribute.
        if value is None, returns the value of attr in attrs
        if value is set, adds attr to attrs with given value.
        if attr already existed in attrs, updates attr in attrs with new value and  returns old value 
        """ 
        originalValue = self.attrs.get(attr)
        if value:
            self.attrs[attr] = value
            # if attr did not exist already, need to return value it was just set to
            # if originalValue is not None, attr already existed thus need to return originalValue  
            originalValue = value if not originalValue else originalValue 
        return originalValue 

    def id(self, value:str = None) -> str:
        """
        id() is separate from attrValue as it's reasonable for the package to generate a unique id for the element.
        If there is no id in attrs, id() will generate one, add it to attrs and return the value.
        if the value argument is not None, id() will go through attrValue to set that value for the 'id' attribute and return that.
        """
        if value:
            return self.attrValue('id', value)
        elif (existing := self.attrs.get('id')):
            return existing
        else:
            idValue = f'{self.tag}-{random()}'
            self.attrValue('id', idValue)
            return idValue 

    def getAttributesString(self, inAttrs: Dict = None) -> str:
        """
        in general, this will return the string of the attributes currently set on the element
        alternatively, if a derived element has a dict of attributes not in the base attrs dict,
        that dict can be passed in and used instead.
        """
        lattrs = inAttrs if inAttrs else  self.attrs 
        attrString = ''
        if lattrs and len(lattrs) > 0: 
            for k,v in lattrs.items():
                attrString += f' {k}="{v}"'
        return attrString 


    def addAttributes(self, **kwArgs) -> None:
        self.attrs.update(kwArgs)


    def openingTag(self) -> str:
        """
        returns a string representing the opening tag  and any attributes 
        """
        return f'<{self.tag} {self.getAttributesString()}>'
        
    def closingTag(self) -> str:
        return f'</{self.tag}>'


    def __repr__(self):
        return f'{self.openingTag()} {self.contents} {self.closingTag()}'


#######
class BaseElementList(BaseElement):
    """
    when implementing the list elements (<ol>, <ul>, <dl>, <menu>), I created a BaseList in lists.py 
    Each of the list elements extended BaseList
    When implemeting tables, I realized there are many elements whose contents is a list of other elements
    Thus BaseList is now in baseElements.py as BaseElementList
    I'm not entirely happy with that name, maybe something better will come to me
    Regarding the type of objects contained in an ElementList,
    it really should be Baseelement as the idea is it's a list of Elements
    However, <dl> threw a wrench in the planning
    <dl> is a list but of two different types of elements
    In lists.py, there's DListItem used to make <dl> entries look like <li> elements
    But DListItem is not derived from BaseElement because it's not an element,
    and it doesn't have a tag, and I didn't want to make up one
    So ElementList can have Any type in it to initially accomodate ListItem and DListItem 
    And other elements like tr and label and input 
    and probably more objects like DListItem in the future 
    """
    def __init__(self, tag: str, elements: List[Any] = None, **kwArgs):
        self.elements = ElementList(elements) if elements else ElementList([])
        super().__init__(tag, self.elements, **kwArgs)

    def addElement(self, elem: Any, front: bool = False) -> None: 
        if front:
            self.elements.insert(0, elem)
        else:
            self.elements.append(elem)

    def addElements(self, elements: List[Any]) -> None:
        self.elements += ElementList(elements)

    def elementCount(self) -> int:
        return len(self.elements)


## end of file 