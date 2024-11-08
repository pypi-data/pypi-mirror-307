"""
pyCFS
==========

Python library for automating and data handling tasks for openCFS.

pyCFS.data
----------
Data processing framework for openCFS. This submodule
contains Python libraries to easily create and manipulate data stored in
openCFS type HDF5 file format (``*.cfs``).

"""

__name__ = "pyCFS"
__author__ = ["IGTE", "Eniz Mušeljić", "Andreas Wurzinger"]
__version__ = "0.0.8"
__all__ = ["pyCFS", "data"]

from .pyCFS import pyCFS  # noqa
from . import data  # noqa
