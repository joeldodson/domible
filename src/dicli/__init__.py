""" domible/src/dicli/__init__.py 
"""

import typer

app = typer.Typer()
app_name = "dicli"

# the main @app.command function needs to be inmported here
# I think it's so app can run it
from .dicli import main


def run():
    app(prog_name=app_name)


## end of file
