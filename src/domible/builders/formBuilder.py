""" domible/builders/formBuilder.py """ 

from typing import Any

from domible.elements import Button, Div, Script 


js_toggle_all_code = """
function toggleDetails(expand) {
    const detailsElements = document.querySelectorAll('details');
    detailsElements.forEach(details => {
        details.open = expand;
    });
}

// Function to toggle between expanding and collapsing                                                          
function toggleAllDetails() {
    const detailsElements = document.querySelectorAll('details');
    const areAllOpen = Array.from(detailsElements).every(details => details.open);

    // Decide whether to expand or collapse based on current state                                              
    toggleDetails(!areAllOpen);
}                                                                                                               
"""


class ToggleDetailsBase:
    """
    using this base, create buttons with different behavior by 
    - passing in different onclick handlers via attributes from the derived classes 
    - note the onclick handlers are using the appropriate JS function with the appropriate argument based on the button's semantics
    - setting contents to an appropriate label 
    """

    def __init__(self, contents: Any, **attributes):
        self.toggle_button = Button(contents, ** attributes)

    def get_button(self):
        return Div([
            Script(js_toggle_all_code), 
            self.toggle_button,
        ])

    def __call__(self):
        return self.get_button()


class ToggleAllDetailsButton(ToggleDetailsBase):
    def __init__(self, contents: Any = "Toggle All Details", **kwArgs ):
        super().__init__(contents=contents, onclick="toggleAllDetails()", **kwArgs)


class ExpandAllDetailsButton(ToggleDetailsBase):
    def __init__(self, contents: Any = "Expand All Details", **kwArgs):
        super().__init__(contents=contents, onclick="toggleDetails(true)", **kwArgs)


class CollapseAllDetailsButton(ToggleDetailsBase):
    def __init__(self, contents: Any = "Collapse All Details", **kwArgs):
        super().__init__(contents=contents, onclick="toggleDetails(false)", **kwArgs)


##
# create these defaults to be easily used where the default label is acceptable
default_toggle_details_button = ToggleAllDetailsButton()
default_expand_details_button = ExpandAllDetailsButton()
default_collapse_details_button = CollapseAllDetailsButton()

## end of file
