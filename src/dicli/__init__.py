""" domible/src/dicli/__init__.py 
"""

# read version from installed package
# using same version as domible as it's the main package 
from importlib.metadata import version
__version__ = version("domible")


from dicli import main 

def run():
    main.run()


## end of file
if __name__ == "__main__":
    run()

## end of file 