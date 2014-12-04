"""
    `appengine_config.py` gets loaded when starting a new application instance.
"""
import sys
import os.path
# add `libs` subdirectory to `sys.path`, so our app can load third-party
# libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))
