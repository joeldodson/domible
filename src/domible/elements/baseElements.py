"""  domible/src/domible/elements/baseElements.py
classes in here are used to build HTML elements
most of the functionality of an element is in the base class
The derived classes are mostly responsible for setting the appropriate tag string value 
And there are places where __repr__ needs to be overwritten 

*** note about contents ***

I'll elaborate on this more in the documentation as there's possibly quite a bit to say, here's the gist of it 

Initially, I assumed contents was a single item, e.g., a string, or another BaseElement.
I realized some elements had lists of other elements as their contents, so I made another class, BaseElementList 
in which the contents was specifically a list, though the list could hold anything.
As I learned more about HTML and was developing more complex documents, 
I realized I should only have BaseElement and let contents be anything, including a list.
I could handle it all within the BaseElement implementation. 
Thus BaseElementList is gone and BaseEllement dynamically adjust contents accordingly. 
"""

from __future__ import annotations

from random import random 
from typing import Any

from domible.utils import isSubDict 


class ContentsList(list):
    """
    this class only exists because list.__repr__ prints the square brackets 
    when it's generating the HTML for the list objects  
    """
    def __repr__(self):
        """ 
        return a string that does not include square brackets for the list 
        and has a newline between each element, instead of comma 
        This is used to generate HTML text for sibling elements 
        """
        #  I should change this to map(), except this way is so readable ... 
        listString = '\n'
        for entry in self:
            listString += f'{entry}\n'
        return listString 


class BaseElement:
    """
    BaseElement holds the tag value, the contents,  and a dict of attrivutes      
    and some methods likely needed by all elements 

    The text for the element is genereated by __repr__
    and almost all elements derived from BaseElement can let BaseElement.__repr__ generate the text

    Should we deep copy the contents and attributes?
    Probably not the attributes, they're all strings.
    The contents though can be very complicated structures 
    with many levels of nesting of other elements.
    If someone used elementX in the contents of elementB, 
    then changed elementX, that would change elementB if only references were copied.

    Should it then be an explicit callout that contents are references, not deep copied?
    Maybe ...    But isn't that just saying Python uses pass by reference?
    """
    def __init__(self, tag: str, contents: Any = None, **kwArgs):
        self.tag = tag
        if not contents:
            self.contents = ContentsList()
        elif not isinstance(contents, list):
            # need to call this out here so we don't end up with a list of a list 
            self.contents = ContentsList([contents])
        else:
            self.contents = ContentsList(contents)
        self.attributes = dict(kwArgs)

    def getElements(self, tag: str = None, **attrs) -> list[Any]:
        """
        look at this element and any elements in its contents and 
        return any elements with the given tag and list of attributes 
        Search is breadth first with returned elements in a list 
        with an ordering you'd expect from BFS 

        Think of self as the root of a generic tree.
        self has contents which could be empty, have one or more BaseElements, or something else (e.g., string).
        Only other BaseElements are considerred nodes needing to be searched.
        Nodes not derived from BaseElement are considered  leave nodes, and not searched. 
        """
        found = []
        if not (tag or attrs): return found
        searching = [self]
        while len(searching) > 0:
            current = searching.pop(0)
            if tag == current.tag and isSubDict(attrs, current.attributes):
                found.append(current)  
            searching += [elem for elem in current.contents if isinstance(elem, BaseElement)]    
        return found 

    def attrValue(self, attr: str, value: str = None) -> str:
        """
        use this to set a value for a single attribute,
        or to get the value set for the given attribute.
        if value is None, returns the value of attr in self.attrs
        if value is set, adds attr to attrs with given value.
        if attr already existed in attrs, updates attr in attrs with new value and  returns old value 
        """ 
        originalValue = self.attributes.get(attr)
        if value:
            self.attributes[attr] = value
            # if attr did not exist already, need to return value it was just set to
            # if originalValue is not None, attr already existed thus need to return originalValue  
            originalValue = value if not originalValue else originalValue 
        return originalValue 

    def id(self, value:str = None) -> str:
        """
        id() is separate from attrValue as it's reasonable for the package to generate a unique id for the element.
        If there is no id in self.attrs, id() will generate one, add it to attrs and return the value.
        if the value argument is provided, id() will go through attrValue to set that value for the 'id' attribute 
        and return whatever attrValue returned.
        """
        if value:
            return self.attrValue('id', value)
        elif (existing := self.attributes.get('id')):
            # no value was provided and 'id' already exists in self.attyrs, return the existing value 
            return existing
        else:
            # no value was provided and 'id' does not already exist in self.attrs
            # generate an id, set it in attrs and return that new value 
            idValue = f'{self.tag}-{random()}'
            self.attrValue('id', idValue)
            return idValue 

    def getAttributesString(self, inAttrs: dict = None) -> str:
        """
        in general, this will return the string of the attributes currently set on the element
        alternatively, if a derived element has a dict of attributes not in the base attrs dict,
        that dict can be passed in and used instead.
        """
        lattrs = inAttrs if inAttrs else  self.attributes 
        attrString = ''
        if lattrs and len(lattrs) > 0: 
            for k,v in lattrs.items():
                attrString += f' {k}="{v}"'
        return attrString 


    def addAttributes(self, **kwArgs) -> None:
        """ add all atttributes in kwArgs to self.attrs """
        self.attributes.update(kwArgs)


    def addContent(self, content: Any, front: bool = False) -> None: 
        """ 
        add content to any existing contents.  
        Adds to end of contents by default 
        We know from __init__, contents is at least an empty list 
        """
        if not isinstance(content, list):
            content = [content]
        if front:
            self.contents = ContentsList(content + self.contents)
        else:
            self.contents = ContentsList(self.contents + content)

    def setContent(self, content: Any) -> None: 
        """ 
        set the content of this element to the passed in content
        any existing content will be be lost 
        """
        if not isinstance(content, list):
            content = [content]
        self.contents = ContentsList(content)


    def openingTag(self) -> str:
        """ returns a string representing the opening tag  including any attributes """
        return f'<{self.tag}{self.getAttributesString()}>'
        
    def closingTag(self) -> str:
        """ returns closing tag """
        return f'</{self.tag}>'


    def __repr__(self):
        return f'{self.openingTag()}{self.contents}{self.closingTag()}'


class BaseVoidElement(BaseElement):
    """
    a void element cannot have contents and there is no closing tag
    This class enforces those two properties by overriding a few of BaseElements methods 
    """    
    def __init__(self, tag: str, **kwArgs):
        super().__init__(tag=tag, **kwArgs)

    def addContent(self, content: Any, front: bool = False) -> None: 
        """ 
        void elements do not contain content 
        as it is now, simply return from this method.
        Maybe we should raise an exception 
        or provide an override to say do it regardless.
        If an override is eventually added, __repr__ will need to be updated to include the contents 
        """
        return 

    def __repr__(self):
        """ a void element only has an opening tag, with attributes, if any  """
        return f'{self.openingTag()}'


## end of file 