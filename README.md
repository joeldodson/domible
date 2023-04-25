# domible

Domible is a set of Python classes used to generate HTML documents and elements of arbitrary complexity.
The basic idea behind domible is very simple, HTML elements are represented as Python objects.
When an element object is evaluated, it renders the text of the HTML element.
Objects can contain other element objects which will also evaluate to text when the containing object is evaluated.
See below for a simple example.

## Installation

To install only the domible package, the classes used to create HTML element objects, run:
```bash
$ pip install domible
```

Domible has an optional command line interface (`dicli`) to show some examples.  To install `dicli` along with domible, and be able to run `dicli` from the command line, install domible with:
``` bash
$ pip install domible[dicli] 
```

`dicli` is built using the Python package 
[typer](https://typer.tiangolo.com).
Instead of documenting `dicli` here, I'll keep the internal help current.
Run:
``` bash
$ dicli --help
```
for details on how to use `dicli`.

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`domible` was created by Joel Dodson. It is licensed under the terms of the MIT license.

## Credits

`domible` was created with 
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) 
and the 
[`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
