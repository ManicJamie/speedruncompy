"""Speedruncompy config

strict_mode: Enables pydantic strict mode; errors instead of coercing compatible types. Default False.

check_extras: NOT_IMPLEMENTED: Logs at runtime whether additional fields not known to speedruncompy are present. Intended to alert downstream users to update speedruncompy.
"""

strict_mode: bool = False

check_extras: bool = False
"""TODO: not implemented"""
