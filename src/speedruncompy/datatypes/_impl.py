from enum import Enum
from types import NoneType, UnionType
from typing import Annotated, Any, TypeGuard, TypeVar, Union, get_type_hints, get_origin, get_args
from json import dumps

from ..exceptions import IncompleteDatatype
from .. import config
import logging


class _OptFieldMarker(): pass


T = TypeVar("T")
OptField = Annotated[T, _OptFieldMarker]
_log = logging.getLogger("speedruncompy.datatypes")

ALLOWED_SHADOWS = ["__module__", "__doc__"]

def de_annotate(test: type) -> tuple[type, bool]:
    """Removes annotation from a type, and returns if the annotation was OptField"""
    if get_origin(test) is not Annotated: return (test, False)
    subtype = get_args(test)[0]
    return (subtype, get_args(test)[1] == _OptFieldMarker)

def is_union(test: type) -> TypeGuard[UnionType]:
    return get_origin(test) is Union or get_origin(test) is UnionType

def is_compliant_type(hint: type):
    """Whether the type of the response should be coerced to the hint"""
    if get_origin(hint) == list: return False
    if is_union(hint): return False  # Can't get a union here! TODO: Maybe utilise annotations?
    return issubclass(hint, Datatype) or issubclass(hint, Enum) or hint is float or hint is bool

def de_parameterize(hint: type) -> type:
    return hint if (orig := get_origin(hint)) is None else orig

def get_type_tuple(hint: type) -> tuple[type, ...]:
    return tuple(de_parameterize(subhint) for subhint in get_args(hint)) if is_union(hint) else (de_parameterize(hint),)

def is_type(value, hint: type):
    if hint is Any: return True
    return isinstance(value, get_type_tuple(hint))

def degrade_union(union: type, *to_remove: type) -> type:
    """Removes types from a union type."""
    if get_origin(union) is Union:
        newargs: set = set(get_args(union)) - set(to_remove)
        return Union[tuple(newargs)]  # type: ignore
    return union

def in_enum(enum: type[Enum], value):
    return value in (v for v in enum.__members__.values())

class Datatype(dict):
    """A dictlike object with field accessors, type checking & initialisation helpers.
    
    Downstream datatypes may add helper properties & better initialisation helpers."""
    def __init__(self, template: Union[dict, tuple, "Datatype", None] = None, skipChecking: bool = False) -> None:
        self.__dict__ = self
        
        if isinstance(template, dict):
            self |= template
        elif isinstance(template, tuple):
            hints = get_type_hints(self.__class__)
            for pos, name in enumerate(hints):
                self[name] = template[pos]
        
        if not skipChecking and config.COERCION != config.CoercionLevel.DISABLED:
            self.enforce_types()
    
    @classmethod
    def get_type_hints(cls, de_annotate=True) -> dict[str, Any]:
        """Returns a dict of attributes and their specified type."""
        return get_type_hints(cls, include_extras=not de_annotate)

    def enforce_types(self):
        """Enforces this datatype's fields to conform to specified types."""
        hints = getattr(self, "__annotations__", {})  # TODO: abuse get_type_hints stripping Annotations for us :)
        missing_fields = []  # fields that are specified as non-optional that are missing from
        for fieldname, hint in hints.items():
            nullable_type, optField = de_annotate(hint)  # type that may be nullable but not optional
            true_type = degrade_union(nullable_type, NoneType)  # base type (no union)
            raw = self[fieldname]

            if fieldname not in self.__dict__:
                if optField: continue
                else: missing_fields.append(fieldname)  # Non-optional fields must be present, report if not
            elif is_compliant_type(true_type):
                if not isinstance(raw, true_type):
                    if true_type is bool and (raw != 1 or raw != 0):
                        _log.warning(f"{type(self)}.{fieldname} documented as bool but had value {raw}!")
                    elif issubclass(true_type, Enum) and not in_enum(true_type, raw):
                        _log.warning(f"{type(self)}.{fieldname} enum {true_type} does not contain value {raw}! Not coercing...")
                    else:
                        self[fieldname] = true_type(raw)
            elif get_origin(true_type) is list and type(raw) is list:
                list_type = get_args(true_type)[0]
                if is_compliant_type(list_type):  # Coerce list types
                    self[fieldname] = [list_type(r) if not isinstance(self[fieldname], list_type) else r for r in raw]

            if fieldname in self.__dict__:
                attr = self[fieldname]
                if true_type == Any: _log.debug(f"Undocumented attr {fieldname} has value {raw} of type {type(raw)}")
                elif not is_type(attr, nullable_type):
                    msg = f"Datatype {type(self).__name__}'s attribute {fieldname} expects {nullable_type} but received {type(attr).__name__} = {attr}"
                    if config.COERCION == config.CoercionLevel.STRICT: raise AttributeError(msg)
                    else: _log.warning(msg)

        if len(missing_fields) > 0:
            msg = f"Datatype {type(self).__name__} constructed missing mandatory fields {missing_fields}"
            if config.COERCION == 1: raise IncompleteDatatype(msg)
            else: _log.warning(msg)

    # Catch cases where an optional field is called but is missing
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            if key in get_type_hints(self.__class__).keys(): return None  # TODO: warn here?
            else: raise e
    
    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            if name in get_type_hints(self.__class__).keys(): return None  # TODO: warn here?
            else: raise e
    
    # Appended method in case a subclass shadows
    def values_(self): return super().values()
    
    def to_json(self, **params): return dumps(self, **params)

class LenientDatatype(Datatype):
    """A default Datatype that skips typechecking and enforcement."""
    def enforce_types(self):
        pass
