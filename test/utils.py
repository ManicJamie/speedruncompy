from typing import get_origin, get_args, Optional, Union, get_type_hints
from speedruncompy.datatypes import Datatype

def get_true_type(t: type):
    origin = get_origin(t)
    if origin is None: return t
    else:
        args = get_args(t)
        if origin is Union or origin is Optional:
            return args[0]
        else:
            return origin

def check_datatype_coverage(dt: Datatype):
    keys = set(dt.keys())
    hints = get_type_hints(dt)
    hintNames = set(hints)
    unseenAttrs = keys.difference(hintNames)
    assert unseenAttrs == set(), f"{type(dt)} missing keys: {[a + ' = ' + str(dt[a]) for a in unseenAttrs]}"
    for attr, subtype in hints.items():
        true = get_true_type(subtype)
        if issubclass(true, Datatype):
            if dt[attr] is not None:
                check_datatype_coverage(dt[attr])
        elif true is list:
            list_type = get_args(subtype)[0]
            if issubclass(list_type, Datatype):
                for item in dt[attr]:
                    check_datatype_coverage(item)

def check_pages(pages: dict[int, Datatype]):
    for p, page in pages.items():
        check_datatype_coverage(page)