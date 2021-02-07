import os
import re

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), "nbt2yaml", "__init__.py"))
VERSION = (
    re.compile(r""".*__version__ = ["'](.*?)["']""", re.S)
    .match(v.read())
    .group(1)
)
v.close()

setup(version=VERSION)
