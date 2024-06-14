# domible

Domible is a set of Python classes used to generate HTML documents and elements of arbitrary complexity.

The basic idea behind domible is fairly simple, HTML elements are represented with Python classes.
When an element object is evaluated, it renders the text of the HTML element.
Objects can contain other element objects which will also evaluate to text when the containing object is evaluated.

Through this process of composition and recursive rendering,
domible can be used to programmatically create HTML elements
of arbitrary complexity directly from your Python code.

Go to the
[Domible Documentation](https://joeldodson.github.io/domible)
for details and examples.

