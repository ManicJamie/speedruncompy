from types import NoneType
from typing import get_origin, get_args, get_type_hints
from speedruncompy.datatypes import Datatype
from speedruncompy.datatypes._impl import _OptFieldMarker, degrade_union

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
        true = get_true_type(subtype)
        if issubclass(true, Datatype):
            if dt[attr] is not None:
                check_datatype_coverage(dt[attr])
        elif get_origin(true) is list:
            list_type = get_args(subtype)[0]
            if issubclass(list_type, Datatype):
                for item in dt[attr]:
                    check_datatype_coverage(item)

def check_pages(pages: dict[int, Datatype]):
    for p, page in pages.items():
        check_datatype_coverage(page)
