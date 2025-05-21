# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Domible Documentation'
copyright = '2025-%Y, Joel Dodson'
author = 'Joel Dodson'
version = '0.1'
release = '0.1.0'
needs_sphinx = '8.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "pydata_sphinx_theme"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

# links for the sphinx_book_theme
# the 'book' theme is based on the 'pydata' theme thus options derive from there as well.
# pdata-sphinx-theme opsions: https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/layout.html#references
# sphinx-book-theme options: https://sphinx-book-theme.readthedocs.io/en/latest/reference.html

html_title = 'Domible Documentation' 
html_last_updated_fmt = ""
html_show_copyright = False
html_show_sphinx = True
html_show_sourcelink = False 
# remove all side bars, only have horizontal nav in header
html_sidebars = {"**": []}
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navbar_align": "left",
    "github_url": "https://github.com/joeldodson/webdevaccess",
    "content_footer_items": [],
    "footer_start": [],
    "footer_end": [],
    "footer_center": ["sphinx-version", "theme-version", "last-updated"],
    "show_version_warning_banner": False,
    # no secondary sidebars for any pages
    "secondary_sidebar_items": {"**": []},
    # trying to get rid of inaccessible color mode switcher
    "navbar_end": ["navbar-icon-links"],
    ###
    # folowing are options (I think) only used by sphinx-book-theme
    # leaving them here in case I try that theme again
    ## "use_download_button": False,
    ## "repository_branch": "main",
    ## "use_issues_button": True,
    ## "use_repository_button": True,
    ## "home_page_in_toc": True,
    ## "footer_content_items": [],
}

