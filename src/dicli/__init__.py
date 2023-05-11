""" domible/src/dicli/__init__.py 
"""

# read version from installed package
# using same version as domible as it's the main package 
from importlib.metadata import version
__version__ = version("domible")


from dicli.main import app

app_name = "dicli"


def run():
    app(prog_name=app_name)


## end of file
