""" domible/src/dicli/__main__.py 
"""

import jsonloggeriso8601datetime as jlidt

from . import app, app_name
from . import run


def main():
    app(prog_name=app_name)


if __name__ == "__main__":
    jlidt.setConfig()
    run()
    ## main()

    ## end of file
