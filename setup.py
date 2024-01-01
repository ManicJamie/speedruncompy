from setuptools import setup
import os

if "srcpy-version" in os.environ:
    __version__ = os.environ["srcpy-version"]

# __version__ = "v0.0.0-alpha" # For non-automated builds

setup(version=__version__)