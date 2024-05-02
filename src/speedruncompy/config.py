import enum, typing

class CoercionLevel(enum.IntEnum):
    DISABLED = -1
    ENABLED = 0
    STRICT = 1


COERCION: typing.Union[CoercionLevel, int] = CoercionLevel.ENABLED
"""How aggressively to enforce type coercion.

-1: Disabled; types will not be coerced. WARN: field accessors will break!
0: Enabled; types will be coerced. Sends log warnings on incomplete types.
1: Strict; types will be coerced. Raises errors on incomplete types.
"""
