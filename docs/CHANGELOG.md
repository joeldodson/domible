# Changelog

## v0.1.18 (2025-05-21)

- changes to packaging and docs, nothing API related though
- upgraded to poetry 2.x

  - no longer able to specify dicli script as an extra
    without using deprecated functionality from poetry
  - so now it is always installed 

- moved dicli to be in domible package and  moved elements command out of dicli

  - see [docs for webdevaccess](https://joeldodson.github.io/webdevaccess) for why.
  - dicli is installed as a script (cli entry point to domible) and can be run via pipx out of PyPI

- switched to sphinx from mkdocs

  - better accessibility using the pydata-sphinx-theme
  - [domible docs on github pages](https://joeldodson.github.io/domible)

## v0.1.17 (2025-03-27) -- BREAKING BACKWARD COMPATIBILITY  

- fixed a few bugs in 0.1.16, no new functionality added 
- keeping the BREAKING note in case someone only looks at 0.1.17 and misses 0.1.16
- as though anyone is looking at any of this  ;)

## v0.1.16 (2025-03-27) -- BREAKING BACKWARD COMPATIBILITY  

- BREAKING: Changed domible.tools.open_html_in_browser to open_html_document_in_browser
- and added domible.tools.open_html_fragment_in_browser
- makes it easier to, for example, create an HTML table using a builder then have that table popped open in the browser 
- updated domible.tools.open_object_in_browser

  - this change is transparent but is good for testing open_html_fragment_in_browser

## v0.1.15 (2025-01-13) 

- this version is motivated by a desire to toggle visibility of all details elements 
- and now, forms... starting with the button  

  - this is a very basic ability to create a button element
  - any attributes (e.g., type) will be done manually or via a builders class
  - this is all TBD and might change in subsequent releases 

- a new builder to add a toggle button to a page to expand/collapse the content of a details element 

  - this is also the introduction of JavaScript into domible (sorry, it was inevitable) 
  - the JS is hard coded into the builder, which might be the long term solution, but I doubt it 
  - focus is on functionality, no CSS has been added 

- added toggle details button into efo.py in tests 
- added a toggle details button in open_object_in_browser() in domible tools 
- fixed bug in Script element where contents was not being passed to super().__init__ 

## v0.1.14 (2024-12-19) -- BREAKING BACKWARD COMPATIBILITY 

- removed typer from dicli, starts a little faster
  - going simple with argparse to avoid pip installing lots of stuff 
- major work on lists -- BREAKS COMPATIBILITY 
  - removed ListBuilder 
  - created new base class for HTML lists in domible/lists.py - HtmlListBase  
  - moved functionality from ListBuilder into HtmlListBase 
  - added ability to get list hidden in a Details element with a Summary 
  - updated tests in dicli and tests/efo.py to validate the changes 

## v0.1.13 (2024-11-28)

- missed ignore_Nones in tools.py 
- found a few more bugs in element_from_object 
- enhanced efo.py (element_from_object) in tests 

## v0.1.12 (2024-11-27)

- added Details and Summary elements to support collapsible regions 
- significant rewrite of element_from_object to hide lists in collapsible regions 
- removed bool to tell element_from_object to not include properties with value None, too hacky     

## v0.1.11 (2024-11-06)

- added bool to tell element_from_object to not include properties with value None      

## v0.1.10 (2024-09-14)

- fixed bug I created in v0.1.9 when using a temp file to open_html_in_browser
- would have been nice for the .10 release to be something cool, not just me screwing up 

## v0.1.9 (2024-09-14)

- added &lt;hr> (HorizontalRule) element to sectioning
- added ability to save html doc to a file in open_html_in_browser
- and now setting encoding correctly to utf-8 when writing to file (saved or temporary)

## v0.1.8 (2024-09-06)

- more tweaks to tools and updating other areas to use tools
- updated some dependencies 
- been focused on work and some volunteering stuff, hope to get back to this soon...

## v0.1.7 (2024-06-18)

- more tweaks to element_from_object
- added open_object_in_browser to tools.
  now, in the REPL, I don't have to call element_from_object then open_in_browser.

## v0.1.6 (2024-06-15)

- tweaks to element_from_object.
  I didn't like the way headings read out within list items.
  Also, treat empty objects like terminals, simple print statement.
  I think it's a bit cleaner this way.

## v0.1.5 (2024-06-14)

- WARNING - Breaking backward compatibility with this release 
- changed several methods and variable names to snake case (Hey, cool aid!!)
- added element_from_object to domible.builders, including simple test script (efo.py) in tests directory 
  (not tied in to pytest though)
- added add_sublist to ListBuilder to address HTML/CSS issue with extra "bullet point."
  (see comments in ListBuilder.py for more details)
- ran "poetry up" to update all version constraints in pyproject.toml 
- updates to docs available at [github pages for the domible repo](https://joeldodson.github.io/domible/).

## v0.1.4 (2024-06-06)

- kind of getting back to domible 
- to use with another project, added a 'tools' module under domible
- added open_in_browser and save_to_file in tools 

## v0.1.3 (2023-10-28)

- wait for 0.1.4 to complete NavBuilder, want to get ListBuilder into pypi
- changed documentation to mkdocs, so easy to automate deployment of docs to github pages
- created ListBuilder to support NavBuilder 
- added many, and moved some, elements to support a nav builder
- some modifications to dicli code and tablebuilder to support returning &lt;style> and &lt;script> elements 
- updated README to explain how CSS and JavaScript will be generated by builders

## v0.1.2 (2023-05-11)

- strange problem when installing domible[dicli].  pip appears to be installing dicli 0.1.0 and 0.1.1.
- adding versioning to dicli package using same version from 
pyproject.  let's see if that helps...

## v0.1.1 (2023-05-11)

- missed adding `requests` package to `dev` group and `dicli` extra
- element reference pages on MDN appear to have changed.  Updated parsing accordingly.  This is for `dicli elements`
- Along with upgrading the parsing, extended the summary to include all sibling paragraphs after the h1 heading in the element reference page.  Also for `dicli elements` 

## v0.1.0 (2023-05-08)

- First release of `domible`!
- This release completes the evolution of
[pymenable](https://github.com/joeldodson/pymenable) from using jinja for document structure to using only Python classes.
- Started some very basic 
pytest automated testing.
- Started basic examples.  Not sure if it will continue in notebooks.
