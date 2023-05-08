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

Instead of using jinja templates for the basic structure of the HTML document,
a root class, Html, generates the &lt;html> element
with Head and Body classes generating the &lt;head> and &lt;body> elements.
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

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`domible` was created by Joel Dodson. It is licensed under the terms of the MIT license.

## Credits

`domible` was created with
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)
and the
[`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

