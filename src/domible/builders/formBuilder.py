""" domible/src/domible/builders/formBuilder.py 
""" 

from typing import Any

from domible.elements import Button, Div, Script 


js_code = """
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


class ToggleDetailsButton:
    def __init__(self, contents: Any = None, **attributes):
        """
        generates a single purpose button to set the details 'opn' property to True/False 
        attributes passed in are intended for the button element 
        """
        contents = "Toggle All Details" if not contents else contents 
        self.toggle_button = Button(
            contents, onclick="toggleAllDetails()", ** attributes
        )

    def get_button(self):
        return Div([Script(js_code), self.toggle_button])

    def __call__(self):
        return self.get_button()

##
# create this default to be easily used where the default label is acceptable 
default_toggle_details_button = ToggleDetailsButton()

## end of file
