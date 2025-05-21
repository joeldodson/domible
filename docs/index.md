# domible Documentation

Domible is a set of Python classes used to generate HTML documents and elements of arbitrary complexity.

The basic idea behind domible is fairly simple, HTML elements are represented using Python classes.
When an element object is evaluated, it renders the text of the HTML element.
Objects can contain other element objects which will also evaluate to text when the containing object is evaluated.
Through this process of composition and recursive rendering,
domible can be used to programmatically create HTML elements
of arbitrary complexity directly from your Python code.

## Installation

To install the domible package, run:

```bash
pip install domible
```

### Command Line Interface (dicli)

```dicli``` is a simple script with examples of how to use domible.
it is installed along with domible and should be in your path after installation.
For details on how to use `dicli`, run:

``` bash
dicli --help
```

## Interfaces

Domible has three areas of integration.  
They're not layers, as in one builds upon the other.
It's more of there is a foundational idea,
then interfaces using that foundational piece to provide higher level abstractions to encapsulate functionality.
It's within these abstractions I hope to include HTML/CSS/JS to generate more accessible, semantic HTML documents.

A developer using domible is likely to use all three points of integration in their code.
For example, an anchor should be created using the basic ```Anchor``` class.
There is no builder for an anchor, it's straight forward as is.

### elements - Create basic HTML elements.

These are Python classes, one for each element, and are very low level.
Attributes and contents can be included at element object creation time, or added later.
Contents can be other element objects, or other Python objects (e.g. str).

### builders - classes to create more complicated HTML elements.

For example, a &lt;table> element is an HTML element but not very useful alone.
The tableBuilder module contains abstractions for rows and table.
These can be used in your python code to build tables using your data
without explicitly creating all the subsequent elements required in a &lt;table>.
Within the tableBuilder 
interface, accessibility related code can be included,
thus resulting in more accessible, semantic HTML.

### starterDocuments - initial document structure to build upon

This module provides an initial HTML document on which to begin building your application.
It will range from the most basic, an &lt;html> element with a 
&lt;head>, with a few default &lt;meta> tags,
and an empty &lt;body> element ready to be added to with your own elements.

Other starter documents will increase in complexity with more initial boiler plate elements
like &lt;nav> components you can extend with your own navigation elements.

The starter documents will most likely be evolving as needs are better understood.

## What About CSS and JavaScript?

Ideally, there will be no JavaScript.
Unfortunately, we live in a broken world.
Some JavaScript might be needed to make an element more accessible or functional/usable.

Similar story regarding CSS.
Not the unfortunate part, the reality some CSS might be required for accessibility considerations.

As I write this, only the tablebuilder exists.
The navbuilder is in process, which forced me to think about CSS and JS.
Considering there is only one complete (as in usable) builder now,
and writing a nav builder is raising issues I need to think through,
it seems likely the builders will evolve for a while.
And probably not in a backward compatible way.

Here are my current thoughts regarding including CSS and JS.
Each builder will return not just the root element of the component it encapsulates,
it will return a tuple with three elements:

1. the root element representing the component
1. a Style element containing any CSS required for accessibility
1. a Script element containing any necessary JavaScript.

If the component doesn't need any CSS, or JS,
None will be returned in place of that element.

Note: by "root" element, I mean the root of the element being built.
For example, 

tablebuilder creates a &lt;table> element
thus the "root" element is &lt;table>.
The "root" from the 
navbuilder will be a &lt;nav> element.

## typing (type hints)
A note on my random use of python type hints.
Since each element is a class, in theory, I could, for example,
use type hints to indicate the contents of a &lt;ul> can contain only 
objects of type ListItem, Script, and Template (three classes defined in elements).

I should do that, someday.

For now though, I need to get more builders working to 
create more sophisticated proofs of concept.

``` {toctree}
:maxdepth: 2
:hidden: true
:caption: Table of Contents

about.md
CONDUCT.md
CHANGELOG.md
```
