from types import NoneType
from typing import Mapping, get_origin, get_args, get_type_hints
from speedruncompy.datatypes import Datatype
from speedruncompy.datatypes._impl import _OptFieldMarker, degrade_union, get_type_tuple

def get_true_type(t: type):
    return degrade_union(t, NoneType, _OptFieldMarker)

def check_datatype_coverage(dt: Datatype):
    keys = set(dt.keys())
    try:
        hints = get_type_hints(dt)
    except TypeError: hints = dict()  # Errors on empty datatype
    hintNames = set(hints)
    unseenAttrs = keys.difference(hintNames)
    assert unseenAttrs == set(), f"{type(dt)} missing keys: {[a + ' = ' + str(dt[a]) for a in unseenAttrs]}"
    for attr, subtype in hints.items():
        types = get_type_tuple(subtype)
        for t in types:
            if issubclass(t, Datatype):
                if dt[attr] is not None:
                    check_datatype_coverage(dt[attr])  # type: ignore
            elif get_origin(t) is list:
                list_type = get_args(subtype)[0]
                if issubclass(list_type, Datatype):
                    for item in dt[attr]:  # type: ignore
                        check_datatype_coverage(item)

def check_pages(pages: Mapping[int, Datatype]):
    for p, page in pages.items():
        check_datatype_coverage(page)
