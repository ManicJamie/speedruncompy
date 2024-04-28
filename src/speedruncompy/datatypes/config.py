STRICT_TYPE_CONFORMANCE = False
"""Whether to raise an error or just warn when a type is incomplete.

Setting this to True might screw you over if SRC decide to remove parts of a type."""

DISABLE_TYPE_CONFORMANCE = False
"""Whether to automatically convert calls and nested datatypes from dictionaries to their typed equivalents.

Will probably improve performance on responses that retrieve a lot of data."""

#TODO: combine into single param, since Strict does nothing when Disabled

SUPPRESS_FIELD_WARNINGS = False
"""Suppress warnings that a type is """