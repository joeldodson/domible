# About

domible is an evolution of the
[pymenable package](https://pypi.org/project/pymenable/)
which is deprecated.

Instead of using jinja templates for the basic structure of the HTML document (as I did in pymenable),
domible uses only Python classes to create and modify the HTML document.
a root class, Html, generates the &lt;html> element.
Head and Body classes generate the &lt;head> and &lt;body> elements.
Elements can be added to the head and body to generate HTML documents of arbitrary complexity.

I decided pymenable was too complicated using jinja templates
(e.g., having to manage extra resources and learn to use jinja).

I'm not disparaging jinja, it's an awesome tool.
I think it's easier though to use Python classes to create the root element as well as all the other elements for the HTML document.

Plus I wanted to change the name.

## Contributing?

If you're interested in being part of this rambling experiment,
please open an issue in github to initiate a conversation.
Please first take a quick read through the 
[Code of Conduct](CONDUCT.md).
It's very short and casual.