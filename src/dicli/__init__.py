""" domible/src/dicli/__init__.py 
"""

from dicli.main import app

app_name = "dicli"


def run():
    app(prog_name=app_name)


## end of file
