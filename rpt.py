#!/usr/bin/env python
""" domible/rpt.py

rpt is for Run PyTest
I'm embedding running pytest into an app to manage logging and output.

pytest still gets its configuration from the table in pyproject.toml,
but it's using the handlers and formatters from jsonloggeriso8601datetime (jlidt).

when the pytest configuration parameter log_cli is true,
console logs from jlidt are seen in the console output from pytest.
For those logs, the log_cli_level is used, not the jlidt console log level.
At the very end of the pytest console output, you'll see the same set of console logs.
For those however, the log level from the jlidt console handler is used
(thus the logs streamed with the pytest output might be different than those at the end of the output).  

"""
import sys 

import jsonloggeriso8601datetime as jlidt 
jlidt.setConfig()
import logging
logger = logging.getLogger(__name__)

import pytest 

if __name__ == "__main__":
    args = sys.argv[1:]
    logger.info(f"running pytest with arguments: {args}, might be empty if nothing to add to or override from pyproject.")
    pytest.main(args)

    ## end of file 