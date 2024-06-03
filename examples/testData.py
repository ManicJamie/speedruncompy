from speedruncompy.datatypes import *
from speedruncompy.datatypes.enums import *
from speedruncompy import *

import json

time = RuntimeTuple({"hour":0, "minute":1, "second": 0, "millisecond": 50})

print(time)
print(repr(time))

print(json.dumps({"help": EventType.CATEGORY_CREATED}))