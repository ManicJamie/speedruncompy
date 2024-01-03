"""
Useful datatypes in both a dictlike and objectlike interface, to facilitate type hinting.

Note that the attribute hints may not be exhaustive; 
while I endeavour to keep these up to date, updates to the v2 API are unannounced and may be missed.

Missing attributes should remain available through both objectlike and dictlike interfaces,
so you can treat them as normal (albeit without type hinting).
"""

from numbers import Real
from typing import Any, Optional, Union, get_type_hints, get_origin, get_args
from json import JSONEncoder

from .exceptions import IncompleteDatatype
import logging

STRICT_TYPE_CONFORMANCE = False
"""Whether to raise an error or just warn when a type is incomplete.

Setting this to True might screw you over if SRC decide to remove parts of a type."""

DISABLE_TYPE_CONFORMANCE = False
"""Whether to automatically convert calls and nested datatypes from dictionaries to their typed equivalents.

Will probably improve performance on responses that retrieve a lot of data."""

#TODO: combine into single param, since Strict does nothing when Disabled

SUPPRESS_FIELD_WARNINGS = False
"""Suppress warnings that a type is """

class srcpyJSONEncoder(JSONEncoder):
    """Converts Datatypes to dicts when encountered"""
    def default(self, o: Any) -> Any:
        if isinstance(o, Datatype):
            return o.get_dict()
        return super().default(o)

_log = logging.getLogger("speedruncompy.datatypes")

def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)

def get_true_type(hint):
    return get_args(hint)[0] if (get_origin(hint) is Union) or (get_origin(hint) is Optional) else hint

class Datatype():
    def __init__(self, template: Union[dict, tuple, "Datatype"] = None) -> None:
        if isinstance(template, dict): 
            self.__dict__ |= template
        elif isinstance(template, tuple):
            hints = get_type_hints(self.__class__)
            for pos, name in enumerate(hints):
                self.__dict__[name] = template[pos]
        elif isinstance(template, Datatype):
            self.__dict__ |= template.get_dict()
        self.enforce_types()
    
    @classmethod
    def get_type_hints(cls) -> dict[str, Any]:
        """Returns a dict of attributes and their specified type"""
        return get_type_hints(cls)

    def enforce_types(self):
        if DISABLE_TYPE_CONFORMANCE: return
        hints = self.get_type_hints()
        missing_attrs = []
        for attr, hint in hints.items():
            base_hint = get_true_type(hint)

            if attr not in self.__dict__:
                if is_optional(hint): continue
                else: missing_attrs.append(attr)
            elif issubclass(base_hint, Datatype):
                if not isinstance(self[attr], hint):
                    self[attr] = base_hint(self[attr]) # Force contained types to comply
            elif get_origin(hint) is list:
                list_type = get_args(hint)[0]
                if issubclass(list_type, Datatype):
                    raw = self[attr]
                    self[attr] = []
                    for r in raw:
                        self[attr].append(list_type(r))

        if len(missing_attrs) > 0:
            if STRICT_TYPE_CONFORMANCE: raise IncompleteDatatype(missing_attrs)
            else: _log.warning(f"Datatype {type(self).__name__} constructed missing mandatory fields {missing_attrs}")
    
    # Allow interacting with these types as if they were dicts (in all reasonable ways)
    def __setitem__(self, key, value): self.__dict__[key] = value
    def get(self, key: str, _default: Any) -> Any: return self.__dict__.get(key, _default)
    def __eq__(self, __value: object) -> bool: return self.__dict__ == __value
    def keys(self): return self.__dict__.keys()
    def values(self): return self.__dict__.values()
    def items(self): return self.__dict__.items()
    def __contains__(self, item: object): return item in self.__dict__
    def __iter__(self): return iter(self.__dict__)

    # Catch cases where an optional field is called but is missing
    def __getitem__(self, key): 
        try: 
            return self.__dict__[key]
        except KeyError as e:
            if key in get_type_hints(self.__class__).keys(): return None #TODO: warn here?
            else: raise e
    # __getattr__ only called for missing attributes
    def __getattr__(self, __name: str) -> Any:
        if __name in get_type_hints(self.__class__).keys(): return None #TODO: warn here?
        else: raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{__name}'" ,name=__name, obj=self)

    # Quick conversion to basic dict for requests
    def get_dict(self): return self.__dict__

    # Default display is as a raw dict, subclasses should override appropriately
    def __str__(self) -> str: return str(self.__dict__)
    def __repr__(self) -> str: return self.__str__()

"""
Type definitions
"""

class StaticAsset(Datatype):

    assetType: str
    path: str

class VariableValue(Datatype):

    variableId: str
    valueId: str

    def __str__(self):
        return f"Var {self.variableId} = {self.valueId}"

class RuntimeTuple(Datatype):

    hour: int
    minute: int
    second: int
    millisecond: int

    def __init__(self, template: dict | tuple | Real = None) -> None:
        if isinstance(template, Real):
            self.hour = template // 3600
            self.minute = (template // 60) % 60
            self.second = template % 60
            self.millisecond = template % 1
            return self.enforce_types()
        super().__init__(template)
    
    def __str__(self):
        return f"{f'{self.hour}:' if self.hour != 0 else ''}{self.minute:02}:{self.second:02}{f'.{self.millisecond:03}' if self.millisecond != 0 else ''}" 
    
    def __repr__(self) -> str:
        return f"{self.hour}:{self.minute:02}:{self.second:02}.{self.millisecond:03}"

class RunSettings(Datatype):

    runId: str
    gameId: str
    categoryId: str
    playerNames: list[str]
    time: Optional[RuntimeTuple]  # Note: whichever timing method is primary to the game is required
    timeWithLoads: Optional[RuntimeTuple]
    igt: Optional[RuntimeTuple]
    platformId: int #TODO: change to enum?
    emulator: bool
    video: str
    comment: str
    date: int
    values: list[VariableValue]
    
    def _get_rta(self): return self.timeWithLoads if "timeWithLoads" in self else self.time
    #TODO: this only guarantees RTA if both time and timeWithLoads is present in the run, 
    # but if a LRT run is missing RTA then it will incorrectly return `time` rather than `None`
    # Correctly doing this would require knowledge of the Game data, so with cacheing or autoreqs.
    def _set_rta(self, _val):
        if "timeWithLoads" in self:
            self.timeWithLoads = _val
        else:
            self.time = _val
    rta = property(fget=_get_rta, fset=_set_rta)
    """Decorator property that points to RTA, as this may be either `time` or `timeWithLoads`."""

class Game(Datatype):

    id: str
    name: str
    url: str
    type: str # enum? is this true?
    loadtimes: bool
    milliseconds: bool
    igt: bool
    verification: bool
    autoVerify: Optional[bool] # Why is this optional????? I hate SRC
    requireVideo: bool
    emulator: int # enum
    defaultTimer: int # enum
    validTimers: list[int] # enum
    releaseDate: int
    addedDate: int
    touchDate: int
    baseGameId: Optional[str]
    coverPath: str
    trophy1stPath: Optional[str]
    trophy2ndPath: Optional[str]
    trophy3rdPath: Optional[str]
    runCommentsMode: int # enum
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    boostReceivedCount: int
    boostDistinctDonorsCount: int
    rules: Optional[str]
    viewPowerLevel: int # enum
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[int]
    websiteUrl: Optional[str]
    discordUrl: Optional[str]
    defaultView: int # enum
    guidePermissionType: int # enum
    resourcePermissionType: int # enum
    staticAssets: list

class Category(Datatype):

    id: str
    name: str
    url: str
    pos: int
    gameId: str
    isMisc: bool
    isPerLevel: bool
    numPlayers: int
    exactPlayers: bool
    playerMatchMode: int # enum
    timeDirection: int # technically an enum, 0 = fastest first
    enforceMs: bool
    rules: Optional[str]
    archived: Optional[bool]

class Level(Datatype):

    id: str
    gameId: str
    name: str
    url: str
    pos: int
    rules: Optional[str]
    archived: bool

class Platform(Datatype):

    id: str
    name: str
    url: str
    year: int

class Player(Datatype):
    # Actual optionals (always present in non-anon players) marked #OPT
    id: str
    name: str
    url: Optional[str] 
    powerLevel: Optional[int]
    color1Id: Optional[str]
    color2Id: Optional[str] #OPT
    colorAnimate: Optional[int]
    areaId: Optional[str]
    isSupporter: Optional[bool] #OPT

    def _is_user(self): return not self.id.startswith("u")
    _is_registered = property(fget=_is_user)
    """Checks if a player has an account or is a text label"""

class User(Datatype):
    id: str
    name: str
    url: str
    pronouns: list[str]
    powerLevel: int
    """Site-level, 1 is default, Meta is 4"""
    color1Id: str
    color2Id: Optional[str]
    colorAnimate: Optional[int]
    areaId: str
    isSupporter: Optional[bool] # ?
    avatarDecoration: Optional[Any] # Unknown type
    iconType: Any
    onlineDate: int
    signupDate: int
    touchDate: int
    staticAssets: list
    supporterIconType: Optional[Any]
    supporterIconPosition: Optional[Any]

class Region(Datatype):

    id: str
    name: str
    url: str
    flag: str

class Run(Datatype):

    id: str
    gameId: str
    categoryId: str
    levelId: Optional[str]
    time: Optional[float]
    timeWithLoads: Optional[float]
    igt: Optional[float]
    enforceMs: Optional[bool]
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: Optional[str]
    emulator: bool
    regionId: Optional[str]
    video: Optional[str]
    comment: Optional[str]
    submittedById: Optional[str]
    verified: int
    verifiedById: Optional[str]
    reason: Optional[str]
    date: int
    dateSubmitted: Optional[int]
    """Only omitted on some very old runs!"""
    dateVerified: Optional[int]
    hasSplits: bool
    obsolete: bool
    place: int
    issues: Optional[Any]
    playerIds: list[str]
    valueIds: list[str]

class ChallengeRun(Datatype):

    id: str
    gameId: str
    challengeId: str
    time: Optional[float]
    timeWithLoads: Optional[float]
    igt: Optional[float]
    enforceMs: Optional[bool]
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: Optional[str]
    emulator: bool
    regionId: Optional[str]
    video: Optional[str]
    comment: Optional[str]
    submittedById: Optional[str]
    screened: bool
    screenedById: Optional[str]
    verified: int
    verifiedById: Optional[str]
    reason: Optional[str]
    date: int
    dateSubmitted: int
    dateVerified: Optional[int]
    dateScreened: Optional[int]
    issues: Optional[Any] # Unknown type
    playerIds: list[str]
    commentsCount: int
    place: Optional[int]
    obsolete: Optional[bool]