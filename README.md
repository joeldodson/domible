# domible

Domible is a set of Python classes used to generate HTML documents and elements of arbitrary complexity.

The basic idea behind domible is fairly simple, HTML elements are represented as Python objects.
When an element object is evaluated, it renders the text of the HTML element.
Objects can contain other element objects which will also evaluate to text when the containing object is evaluated.
See below for a basic example.

## Origin Story

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

## Installation

To install the domible package (which includes a simple starter script), run:

```bash
pip install domible
```

Along with the domible package is a script, `distarter` to serve as an example of how to use domible.  After you pip install domible, you should be able to run `distarter` from the command line.  Running it should result in a very simple web page shown in your default browser.  See below for how to find the code for `distarter`.

### Command Line Inerface (dicli)

Domible has an optional command line interface (`dicli`) to show some examples.  To install `dicli` along with domible, and be able to run `dicli` from the command line, install domible with:

``` bash
pip install domible[dicli] 
```

`dicli` is built using the Python package
[typer](https://typer.tiangolo.com).
Instead of documenting `dicli` here, I'll keep the internal typer supported help current.
For details on how to use `dicli`, run:

``` bash
dicli --help
```

## Usage

At some point there will be really cool examples here using Jupyter Notebooks.  Until then, the code from `distarter` will serve as a starting point.

To get the code for `distarter`, look in the site-packages, where you pip installed domible, for the distarter package.
And/or, you can clone the domible repo and look in `domible/src/distarter/main.py`.

## Interfaces

Domible has three areas of integration.  
They're not layers, as in one builds upon the other.
It's more of there is a foundational idea,
then interfaces using that foundational piece to provide higher level abstractions to encapsulate functionality.
It's within these abstractions I hope to include HTML/CSS/JS to generate more accessible, semantic HTML documents.

### typing (type hints)
First a note on my random use of python type hints.
Since each element is a class, in theory, I could, for example,
use type hints to indicate the contents of a &lt;ul> can contain only 
objects of type ListItem, Script, and Template (three classes defined in elements).

I should do that, someday.

We should be able to use typing to support using tools like mypy for checking 
the validity of a Python program generating HTML.

For now, I need to get more builders working to 
create more sophisticated proofs of concept.

### elements - Create basic HTML elements.

These are Python classes, one for each element, and are very low level.
Attributes and contents can be included at element object creation time, or added later.
Contents can be other element objects, or other Python objects (e.g. str).

### builders - classes to create more complicated HTML elements.

For example, a &lt;table> element is an HTML element but not very useful alone.
The tableBuilder module contains abstractions for rows and table.
These can be used in your python code to build tables using your data
without explicitly creating all the subsequent elements required in a &lt;table>.
Within the tableBuilder inerface, accessibility related code can be included,
thus resulting in more accessible, semantic HTML.

### starterDocuments - initial document structure to build upon

This module provides an intial HTML document on which to begin building your application.
It will range from the most basic, an &lt;html> element with a 
&lt;head>, with a few default &lt;meta> tags,
and an empty &lt;body> element ready to be added to with your own elements.

Other starter documents will increase in complexity with more initial boiler plate elements
like &lt;nav> components you can extend with your own navigation elements.

The starter documents will most likely be evolving as needs are better understood.

## What About CSS and JavaScript?

Ideally, there will be no JavaScript.
Unfortunately, we live in a broken world.
Some JavaScript might be needed to make an element more accessible.

Similar story regarding CSS.
Not the unfortunate part, the reality some CSS might be required for accessibility considerations.

As I write this, only the tablebuilder exists.
The navbuilder is in process, which forced me to think about CSS and JS.
Considering there is only one complete (as in usable) builder now,
and writing a nav builder is raising issues I need to think through,
it seems likely the builders will evolve for a while.
And probably not in a backward compatible way.
Here's how I'll address the CSS and JS issue for now.

Each builder will return not just the root element of the compoenent it encapsulates,
it will return a tubple with three elements:
1. the root element representing the component
1. a Style element containing any CSS required for accessibility
1. a Script element containing any necessary JavaScript.

If the component doesn't need any CSS, or JS,
None will be returned in place of that element.

Note: by "root" element, I mean the root of the element being built.
For example, tablebuilder creates a &lt;table> element
thus the "root" element is &lt;table>.
The "root" from the navbuilder will be a &lt;nav> element.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`domible` was created by Joel Dodson. It is licensed under the terms of the MIT license.

## Credits

`domible` was created with
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)
and the
[`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

