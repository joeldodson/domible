""" domible/builders/preformatted.py

supports blocks of pre formatted text.
Ideal for, and motivated by, displaying source code in the browser
"""

import html 

from domible.elements import Code, Pre, Style, Script

python_code_css = """
pre.python-source {
    overflow-x: auto;
    background-color: #f4f4f4;
    padding: 1em;
    border-radius: 4px;
}

pre.python-source code {
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}
"""

python_code_style = Style(f"{python_code_css}")

def python_code_block(source_code: str) -> Pre:
    src = Code(html.escape(source_code))
    return Pre(src, **{"class": "python-source"})

## end of file 