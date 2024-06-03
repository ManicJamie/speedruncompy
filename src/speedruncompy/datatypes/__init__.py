"""Useful datatypes in both a dictlike and objectlike interface, to facilitate type hinting.

Note that the attribute hints may not be exhaustive;
while I endeavour to keep these up to date, updates to the v2 API are unannounced and may be missed.

Missing attributes remain available through both objectlike and dictlike interfaces,
so you can treat them as normal (albeit without type hinting)."""

from ._impl import LenientDatatype, Datatype  # noqa

from .defs import *  # noqa
from . import responses, enums, _impl  # noqa
