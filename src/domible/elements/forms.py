"""  domible/src/domible/elements/forms.py 
Eventually will include all the HTML form elements.
Anythin fancy will probably be done in formsBuilder.
"""

from typing import Any

from domible.elements.baseElements import BaseElement


class Button(BaseElement):
    def __init__(self, contents: Any = None, **kwArgs):
        super().__init__(tag="button", contents=contents, **kwArgs)


## end of file
