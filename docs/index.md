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

## Scripts

Two scripts, ```dicli```, and ```dibrowse```, are installed by default,
and added to your path, with the domible package installation.
They are very minimal, not resulting in any additional third party packages.

### dicli - domible Command Line Interface

```dicli``` is a simple script with examples of how to use domible.
Run ```dicli --help``` for more information.

### dibrowse - Browse domible's Source Code

```dibrowse``` uses python's inspect module to recursively iterate through the domible package
to collect the python code and enable viewing in your default browser.
Run ```dibrowse --help``` for more information.

```dibrowse``` is a good way to view examples of how domible can be used to build simple tools.
Look for the scripts sub package within domible details element (once your browser has been opened with the output from ```dibrowse```).
You can find the code for both dibrowse and dicli in the scripts package
which shows how domible was used in each of those scripts.
Best place to start is the "simple()" function in the dicli script.

### [webdevaccess](https://joeldodson.github.io/webdevaccess)

webdevaccess is not a script from the domible package,
it's a different github repo created to contain more complex scripts, with third party package requirements.
The link in the heading points to documentation for webdevaccess.

#### [htmlElements](https://joeldodson.github.io/webdevaccess/htmlElements.html)

```htmlElements``` is a python script using domible, requests, and beautifulsoup4 to scrape 
[HTML element references on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements) 
for information for each HTML element to create a table summarizing the elements.
It is very much tied to the structure of the pages on MDN thus breaks occasionally when MDN changes.

### Running Scripts with pipx

For a good intro to pipx, see this
[RealPython article on pipx](https://realpython.com/python-pipx/).

To run any of the domible scripts using pipx, use the following:

``` bash 
pipx --spec domible dicli --help
pipx --spec domible dibrowse --help
pipx --spec webdevaccess htmlElements --help
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
Within the tableBuilder interface, accessibility related code can be included,
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

For style considerations, if a developer is working with a designer,
the designer could provide the CSS file and list of classes to be applied to elements.
The developer could ensure those classes are part of the attributes in the elements' object,
then include a link element in the head of the HTML document to include the CSS file.
Depending on the depth of experience of the designer though, there might be additional CSS required for accessibility reasons.

As I write this, only the tablebuilder exists.
The navbuilder is in process, which forced me to think about CSS and JS.
Considering there is only one complete (as in usable) builder now,
and writing a nav builder is raising issues I need to think through,
it seems likely the builders will evolve for a while.
And probably not in a backward compatible way.

Since that previous paragraph, I've created the very basic formBuilder and preformatted builders.
The formBuilder has simple buttons to toggle, expand, and collapse details elements.
JavaScript is required for that functionality.
I decided to include the JavaScript in the python source code as a string then add it to a Script element.
The Script element is returned with the Button element, both wrapped in a Div.
For now this is sufficient for minimal JavaScript.

For preformatted, e.g., adding python source code to an HTML document,
I wanted specific formatting for the source code.
I included the CSS as a string in the python file and created a Style element.
The variable for the Style element is in file scope for the preformatted builder,
and is imported in the builders package.
It can be added to the head of the HTML doc once the starter document has been created.

The ```dibrowse``` script uses both the details buttons and preformatted builder (for python source code).
Run dibrowse and look in scripts.dibrowse.main.run for examples.

I'm not a huge fan of this approach for including CSS.
It's a two step process thus easy to forget.
Claude told me though it's not a good idea to include a style element within a div, like I'm doing with a script.
I guess this will be a convention/documentation issue for now.

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
