from enum import Enum
from types import NoneType, UnionType
from typing import Any, Optional, TypeVar, Union, get_type_hints, get_origin, get_args
from json import JSONEncoder, dumps
import typing

from ..exceptions import IncompleteDatatype
from .. import config
import logging


class _OptFieldMarker(): pass


T = TypeVar("T")
OptField = Union[T, _OptFieldMarker]

_log = logging.getLogger("speedruncompy.datatypes")


class srcpyJSONEncoder(JSONEncoder):
    """Converts Datatypes to dicts when encountered"""
    def default(self, o: Any) -> Any:
        if isinstance(o, Datatype):
            return o.get_dict()
        return super().default(o)


def is_optional_field(field):
    return get_origin(field) is Union and _OptFieldMarker in get_args(field)

def is_optional(test: type):
    return (get_origin(test) is Union and (NoneType in get_args(test))) or (get_origin(test) is Optional)

def is_union(test: type):
    return get_origin(test) is Union or get_origin(test) is UnionType

def is_compliant_type(hint: type):
    """Whether the type of the response should be coerced to the hint"""
    hint = degrade_union(hint, _OptFieldMarker, NoneType)
    if get_origin(hint) == list: return False
    if is_union(hint): return False  # Guard against unions
    return issubclass(hint, Datatype) or issubclass(hint, Enum) or hint == float or hint == bool

def is_type(value, hint: type):
    if value is None:
        return is_optional(hint)
    else:
        check = degrade_union(hint, _OptFieldMarker, NoneType)
        check = get_origin(check) if get_origin(check) is not None and not is_union(check) else check
        return isinstance(value, check)

def degrade_union(union: type, *to_remove: type):
    """Removes types from a union type."""
    if get_origin(union) is typing.Optional:
        union = get_args(union)[0]  # In case Optional does not become Union (hates me)
    if get_origin(union) is Union:
        newargs: set = set(get_args(union)) - set(to_remove)
        return Union[tuple(newargs)]
    return union

def in_enum(enum: type[Enum], value):
    return value in (v for v in enum.__members__.values())

class Datatype():
    """A dictlike object with field accessors, type checking & initialisation helpers.
    
    Downstream datatypes may add helper properties & better initialisation helpers."""
    def __init__(self, template: Union[dict, tuple, "Datatype", None] = None, skipChecking: bool = False) -> None:
        if isinstance(template, dict):
            self.__dict__ |= template
        elif isinstance(template, tuple):
            hints = get_type_hints(self.__class__)
            for pos, name in enumerate(hints):
                self.__dict__[name] = template[pos]
        elif isinstance(template, Datatype):
            self.__dict__ |= template.get_dict()
        if not skipChecking and config.COERCION != config.CoercionLevel.DISABLED:
            self.enforce_types()
    
    @classmethod
    def get_type_hints(cls) -> dict[str, Any]:
        """Returns a dict of attributes and their specified type"""
        return get_type_hints(cls)

    def enforce_types(self):
        """Enforces this datatype's fields to conform to specified types."""
        hints = self.get_type_hints()
        missing_fields = []  # fields that are specified as non-optional that are missing from
        for fieldname, hint in hints.items():
            nullable_type = degrade_union(hint, _OptFieldMarker)  # type that may be nullable but not optional
            true_type = degrade_union(nullable_type, NoneType)  # base type (no union)
            raw = self[fieldname]

            if fieldname not in self.__dict__:
                if is_optional_field(hint): continue
                else: missing_fields.append(fieldname)  # Non-optional fields must be present, report if not
            elif is_compliant_type(true_type):
                if not isinstance(raw, true_type):
                    if true_type is bool and (raw != 1 or raw != 0):
                        _log.warning(f"{type(self)}.{fieldname} documented as bool but had value {raw}!")
                    elif issubclass(true_type, Enum) and not in_enum(true_type, raw):
                        _log.warning(f"{type(self)}.{fieldname} enum {true_type} does not contain value {raw}!")
                    else:
                        self[fieldname] = true_type(raw)
            elif get_origin(true_type) is list and type(raw) is list:
                list_type = get_args(true_type)[0]
                if is_compliant_type(list_type):  # Coerce list types
                    self[fieldname] = [list_type(r) if not isinstance(self[fieldname], list_type) else r for r in raw]

            if fieldname in self.__dict__:
                attr = self[fieldname]
                if true_type == Any: _log.debug(f"Undocumented attr {fieldname} has value {raw} of type {type(raw)}")
                elif not is_type(attr, hint):
                    msg = f"Datatype {type(self).__name__}'s attribute {fieldname} expects {nullable_type} but received {type(attr).__name__} = {attr}"
                    if config.COERCION == config.CoercionLevel.STRICT: raise AttributeError(msg)
                    else: _log.warning(msg)

        if len(missing_fields) > 0:
            msg = f"Datatype {type(self).__name__} constructed missing mandatory fields {missing_fields}"
            if config.COERCION == 1: raise IncompleteDatatype(msg)
            else: _log.warning(msg)
    
    # Allow interacting with these types as if they were dicts (in all reasonable ways)
    def __setitem__(self, key, value): self.__dict__[key] = value
    def get(self, key: str, _default: Any) -> Any: return self.__dict__.get(key, _default)
    def pop(self, key: str): return self.__dict__.pop(key)
    def __eq__(self, __value: object) -> bool: return self.__dict__ == __value
    def keys(self): return self.__dict__.keys()
    def values(self): return self.__dict__.values()
    def items(self): return self.__dict__.items()
    def __contains__(self, item: object): return item in self.__dict__
    def __iter__(self): return iter(self.__dict__)
    def __copy__(self): return type(self)(self.__dict__.copy())

    def __or__(self, __value: Any):
        self.__dict__.update(__value)
        return self

    # Catch cases where an optional field is called but is missing
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            if key in get_type_hints(self.__class__).keys(): return None  # TODO: warn here?
            else: raise e
    
    # __getattr__ only called for missing attributes
    def __getattr__(self, __name: str) -> Any:
        if __name.startswith("__"): return None  # Special handling for python reserved calls
        if __name in get_type_hints(self.__class__).keys(): return None  # TODO: warn here?
        else: raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{__name}'", name=__name, obj=self)

    # Quick conversion to basic dict for requests
    def get_dict(self): return self.__dict__
    def to_json(self): return dumps(self, cls=srcpyJSONEncoder)

    # Default display is as a raw dict, subclasses should override appropriately
    def __str__(self) -> str: return str(self.__dict__)
    def __repr__(self) -> str: return self.__str__()

class LenientDatatype(Datatype):
    """A default Datatype that skips typechecking and enforcement."""
    def enforce_types(self):
        pass
