# Import every Python file in the bowser directory

import pkgutil
import sys

def run():
    for module in pkgutil.iter_modules(['bowser']):
        if module.ispkg:
            sys.modules[module.name] = module.module
        else:
            __import__("bowser." + module.name)
