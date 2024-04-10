"""
Useful datatypes in both a dictlike and objectlike interface, to facilitate type hinting.

Note that the attribute hints may not be exhaustive; 
while I endeavour to keep these up to date, updates to the v2 API are unannounced and may be missed.

Missing attributes should remain available through both objectlike and dictlike interfaces,
so you can treat them as normal (albeit without type hinting).
"""

from enum import Enum
from numbers import Real
from typing import Any, Optional, Union, get_type_hints, get_origin, get_args, _SpecialForm, _type_check
from json import JSONEncoder

from .enums import *
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

class _OptFieldMarker(): pass
@_SpecialForm
def OptField(self, parameters):
    """Field that may not be present. Will return `None` if not present."""
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, type(_OptFieldMarker)]

class srcpyJSONEncoder(JSONEncoder):
    """Converts Datatypes to dicts when encountered"""
    def default(self, o: Any) -> Any:
        if isinstance(o, Datatype):
            return o.get_dict()
        return super().default(o)

_log = logging.getLogger("speedruncompy.datatypes")

def is_optional(field):
    return get_origin(field) is Union and type(_OptFieldMarker) in get_args(field)

def get_true_type(hint):
    return get_args(hint)[0] if (get_origin(hint) is Union) or (get_origin(hint) is Optional) else hint

def get_optional_type(hint: type):
    if get_origin(hint) is Union and type(None) in get_args(hint): return Union[get_true_type(hint), None]

class Datatype():
    def __init__(self, template: Union[dict, tuple, "Datatype", None] = None, skipChecking: bool = False) -> None:
        if isinstance(template, dict): 
            self.__dict__ |= template
        elif isinstance(template, tuple):
            hints = get_type_hints(self.__class__)
            for pos, name in enumerate(hints):
                self.__dict__[name] = template[pos]
        elif isinstance(template, Datatype):
            self.__dict__ |= template.get_dict()
        if not skipChecking and not DISABLE_TYPE_CONFORMANCE: 
            self.enforce_types()
    
    @classmethod
    def get_type_hints(cls) -> dict[str, Any]:
        """Returns a dict of attributes and their specified type"""
        return get_type_hints(cls)

    def enforce_types(self):
        #TODO: This is the messiest function i've ever written. do better, me (to be fixed Soon(tm))
        hints = self.get_type_hints()
        missing_attrs = []
        for attr, hint in hints.items():
            base_hint = get_true_type(hint)
            if get_origin(hint) is list: 
                list_subhint = get_args(hint)[0]
            else:
                list_subhint = None
            if attr not in self.__dict__:
                if is_optional(hint): continue
                else: missing_attrs.append(attr)
            elif issubclass(base_hint, Datatype) or issubclass(base_hint, Enum) or base_hint == float:
                if not isinstance(self[attr], base_hint):
                    self[attr] = base_hint(self[attr]) # Force contained types to comply
            elif get_origin(hint) is list:
                list_subhint = get_args(hint)[0]
                if issubclass(list_subhint, Datatype) or issubclass(list_subhint, Enum):
                    raw = self[attr]
                    self[attr] = []
                    for r in raw:
                        self[attr].append(list_subhint(r))

            if len(missing_attrs) > 0:
                if STRICT_TYPE_CONFORMANCE: raise IncompleteDatatype(f"Datatype {type(self).__name__} constructed missing mandatory fields {missing_attrs}")
                else: _log.warning(f"Datatype {type(self).__name__} constructed missing mandatory fields {missing_attrs}")

            opt_hint = get_optional_type(hint)
            check = get_origin(base_hint) if get_origin(base_hint) is not None else base_hint
            if check == Any:
                _log.debug(f"Undocumented attr {attr} has value {self[attr]} of type {type(self[attr])}")
                continue # Can't do enforcement against Any
            if not isinstance(self[attr], check) and not isinstance(self[attr], opt_hint):
                if STRICT_TYPE_CONFORMANCE: 
                    raise AttributeError(f"Datatype {type(self).__name__}'s attribute {attr} expects {check} but received {type(self[attr]).__name__}")
                else: _log.warning(f"Datatype {type(self).__name__}'s attribute {attr} expects {check} but received {type(self[attr]).__name__}")
            if isinstance(self[attr], list) and len(self[attr]) > 0:
                instance = self[attr][0]
                subhints = get_args(hint)
                list_subhint = subhints[0]
                if not isinstance(instance, list_subhint):
                    if STRICT_TYPE_CONFORMANCE: 
                        raise AttributeError(f"Datatype {type(self).__name__}'s attribute {attr} expects list[{list_subhint}] but received {type(self[attr][0]).__name__}")
                    else: _log.warning(f"Datatype {type(self).__name__}'s attribute {attr} expects list[{list_subhint}] but received {type(self[attr][0]).__name__}")

        
    
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
    def __or__(self, __value: Any): 
        self.__dict__.update(__value)
        return self

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

class LenientDatatype(Datatype):
    """A default Datatype that skips typechecking and enforcement."""
    def enforce_types(self):
        pass
"""
Type definitions
"""

class StaticAsset(Datatype):

    assetType: str
    path: str

class VarValue(Datatype):

    variableId: str
    valueId: str

    def __str__(self):
        return f"Var {self.variableId} = {self.valueId}"

class VarValues(Datatype):

    variableId: str
    valueIds: list[str]

class RuntimeTuple(Datatype):

    hour: int
    minute: int
    second: int
    millisecond: int

    def __init__(self, template: dict | tuple | Real | None = None) -> None:
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

class CommentPermissions(Datatype):
    canManage: bool
    canViewComments: bool
    canPostComments: bool
    canEditComments: bool
    canDeleteComments: bool
    cannotViewReasons: list[str]
    cannotPostReasons: list[str]

class Commentable(Datatype):
    itemType: int # enum
    itemId: str
    properties: dict # disabled, locked
    permissions: CommentPermissions

class Comment(Datatype):
    id: str
    itemType: int # enum
    itemId: str
    date: int
    userId: str
    text: str
    parentId: str
    deleted: bool

class Like(Datatype):
    itemType: int # enum
    itemId: str
    userId: str
    date: int

class Forum(Datatype):
    id: str
    name: str
    url: str
    description: str
    type: int # Enum, 3=Game
    threadCount: int
    postCount: int
    lastPostId: str
    lastPostUserId: str
    lastPostDate: int
    touchDate: int

class Thread(Datatype):
    id: str
    name: str
    gameId: str
    forumId: str
    userId: str
    replies: int
    created: int # enum
    lastCommentId: str
    lastCommentUserId: str
    lastCommentDate: int
    sticky: bool
    locked: bool

class RunSettings(Datatype):

    runId: str
    gameId: str
    categoryId: str
    playerNames: list[str]
    time: OptField[RuntimeTuple]  # Note: whichever timing method is primary to the game is required
    timeWithLoads: OptField[RuntimeTuple]
    igt: OptField[RuntimeTuple]
    platformId: str
    emulator: bool
    video: str
    comment: str
    date: int
    values: list[VarValue]
    
    def _get_rta(self): return self.timeWithLoads if "timeWithLoads" in self else self.time
    #TODO: this only guarantees RTA if both time and timeWithLoads is present in the run, 
    # but if a LRT run is missing RTA then it will incorrectly return `time` rather than `None`
    # Correctly doing this would require knowledge of the Game data, so with cacheing or autoreqs.
    def _set_rta(self, _val):
        if "timeWithLoads" in self:
            self.timeWithLoads = _val
        else:
            self.time = _val
    _rta = property(fget=_get_rta, fset=_set_rta)
    """Decorator property that points to RTA, as this may be either `time` or `timeWithLoads`.
    
    WARN: only guaranteed RTA if RTA is not None, otherwise may falsely return LRT."""

class Series(Datatype):
    id: str
    name: str
    url: str
    addedDate: int
    touchDate: int
    websiteUrl: OptField[str]
    discordUrl: OptField[str]
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    officialGameCount: int
    staticAssets: list[StaticAsset]

class Game(Datatype):

    id: str
    name: str
    url: str
    type: str # enum? is this true?
    loadtimes: bool
    milliseconds: bool
    igt: bool
    verification: bool
    autoVerify: OptField[bool] # Why is this OptField????? I hate SRC
    requireVideo: bool
    emulator: int # enum
    defaultTimer: TimerName # int enum
    validTimers: list[TimerName] # int enum
    releaseDate: int
    addedDate: int
    touchDate: int
    baseGameId: OptField[str]
    coverPath: str
    trophy1stPath: OptField[str]
    trophy2ndPath: OptField[str]
    trophy3rdPath: OptField[str]
    trophy4thPath: OptField[str]
    runCommentsMode: int # enum
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    boostReceivedCount: int
    boostDistinctDonorsCount: int
    rules: OptField[str]
    viewPowerLevel: int # enum
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[gameType] 
    websiteUrl: OptField[str]
    discordUrl: OptField[str]
    defaultView: int # enum
    guidePermissionType: int # enum
    resourcePermissionType: int # enum
    staticAssets: list[StaticAsset]
    embargoDate: OptField[int]
    embargoText: OptField[str]

class GameStats(Datatype):
    gameId: str
    totalRuns: int
    totalRunsFG: int
    totalRunsIL: int
    totalRunTime: int
    recentRuns: int
    recentRunsFG: int
    recentRunsIL: int
    totalPlayers: int
    activePlayers: int
    followers: int
    guides: int
    resources: int

class RunCount(Datatype):

    gameId: str
    categoryId: str
    levelId: OptField[str]
    variableId: OptField[str]
    valueId: OptField[str]
    count: int

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
    rules: OptField[str]
    archived: OptField[bool]

class Variable(Datatype):

    id: str
    name: str
    url: str
    pos: int
    gameId: str
    description: OptField[str]
    categoryScope: int # enum
    categoryId: OptField[str]
    levelScope: int # enum
    levelId: OptField[str]
    isMandatory: bool
    isSubcategory: bool
    isUserDefined: bool
    isObsoleting: bool
    defaultValue: OptField[str]
    archived: bool
    displayMode: OptField[int] # enum

class Value(Datatype):
    """Value of a variable. `VariableValue` is a selector on this type (and the underlying variable)"""
    id: str
    name: str
    url: str
    pos: int
    variableId: str
    isMisc: OptField[bool]
    rules: OptField[str]
    archived: bool

class Level(Datatype):

    id: str
    gameId: str
    name: str
    url: str
    pos: int
    rules: OptField[str]
    archived: bool

class Platform(Datatype):

    id: str
    name: str
    url: str
    year: int

class Article(Datatype):

    id: str
    slug: str
    title: str
    summary: str
    body: str
    createDate: int
    updateDate: int
    publishDate: OptField[int]
    rejectDate: OptField[int]
    publishTarget: str # enum?
    publishTags: list[str] # enum? probably not
    coverImagePath: OptField[str]
    commentsCount: int
    community: OptField[bool]
    gameId: OptField[str]
    userId: OptField[str]
    editorId: OptField[str]
    stickyDate: OptField[int]

class News(Datatype):

    id: str
    gameId: str
    userId: str
    title: str
    body: str
    dateSubmitted: int

class Player(Datatype):
    """Fields from `User` present in `playerLists`. May also be an unregistered player, use property `_is_registered`"""
    # Actual OptFields (always present in non-anon players) marked #OPT
    id: str
    name: str
    url: OptField[str] 
    powerLevel: OptField[int]
    color1Id: OptField[str]
    color2Id: OptField[str] #OPT
    """OptField even on full `player`"""
    colorAnimate: OptField[int]
    areaId: OptField[str]
    isSupporter: OptField[bool] #OPT
    """OptField even on full `player`"""

    def _is_user(self): return not self.id.startswith("u")
    _is_registered = property(fget=_is_user)
    """Checks if a player has an account or is a text label"""

class User(Datatype):
    id: str
    name: str
    altname: OptField[str]
    url: str
    pronouns: list[str]
    powerLevel: SitePowerLevel
    """Site-level, 1 is default, Meta is 4"""
    color1Id: str
    color2Id: OptField[str]
    colorAnimate: OptField[int]
    areaId: str
    isSupporter: OptField[bool] # ?
    avatarDecoration: OptField[dict[str, bool]] # {enabled: bool}, add type for this later
    iconType: int # enum 0-2?
    onlineDate: int
    signupDate: int
    touchDate: int
    staticAssets: list[StaticAsset]
    supporterIconType: OptField[int] # enum 0-2?
    supporterIconPosition: OptField[int] # enum 0-1?
    titleId: OptField[str]
    """ID for a title given for completing a Challenge"""

class UserStats(Datatype):
    userId: str
    followers: int
    runs: int
    runsFg: int
    runsIl: int
    runsPending: int
    runTime: int
    minRunDate: int
    maxRunDate: int
    commentsPosted: int
    guidesCreated: int
    resourcesCreated: int
    threadsCreated: int
    gamesBoosted: int
    usersBoosted: int
    followingGames: int
    followingUsers: int
    challengeRuns: int
    challengeRunsPending: int

class UserSocialConnection(Datatype):
    userId: str
    networkId: int # enum
    value: str
    verified: bool

class GameOrderGroup(Datatype):
    id: str
    name: str
    sortType: int # enum
    gameIds: list[str]

class GameOrdering(Datatype):
    defaultGroups: list[GameOrderGroup]
    supporterGroups: list[GameOrderGroup]

class UserProfile(Datatype):

    userId: str
    bio: OptField[str]
    signupDate: int
    defaultView: int # enum, assuming fg/level?
    showMiscByDefault: bool
    gameOrdering:GameOrdering #TODO: make better names for these
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]

class UserLeaderboardProfile(Datatype):
    """UserProfile as returned by GetUserLeaderboard & GetUserPopoverData.
    
    Missing userStats and userSocialConnectionList."""
    userId: str
    bio: OptField[str]
    signupDate: int
    defaultView: int # enum, assuming fg/level?
    showMiscByDefault: bool
    gameOrdering:GameOrdering #TODO: make better names for these

class SeriesModerator(Datatype):
    seriesId: str
    userId: str
    level: int # enum

class GameModerator(Datatype):
    gameId: str
    userId: str
    level: int # enum

class ChallengeModerator(Datatype):
    
    challengeId: str
    userId: str
    level: GamePowerLevel

class GameBoost(Datatype):
    id: str
    createdAt: int
    updatedAt: int
    gameId: str
    donorUserId: str
    anonymous: bool
    recipientUserIds: list[str]
    """Appears to always be empty"""

class Region(Datatype):

    id: str
    name: str
    url: str
    flag: str

class Run(Datatype):

    id: str
    gameId: str
    categoryId: str
    levelId: OptField[str]
    time: OptField[float]
    timeWithLoads: OptField[float]
    igt: OptField[float]
    enforceMs: OptField[bool]
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: OptField[str]
    emulator: bool
    regionId: OptField[str]
    video: OptField[str]
    comment: OptField[str]
    submittedById: OptField[str]
    verified: int
    verifiedById: OptField[str]
    reason: OptField[str]
    date: int
    dateSubmitted: OptField[int]
    """Only omitted on some very old runs!"""
    dateVerified: OptField[int]
    hasSplits: bool
    obsolete: OptField[bool]
    place: OptField[int]
    playerIds: list[str]
    valueIds: list[str]
    orphaned: OptField[bool]
    estimated: OptField[bool] #TODO: Figure out what this means
    """Only shown in GetModerationRuns"""
    issues: OptField[Optional[list]] #TODO: fails when present

class ChallengeStanding(Datatype):
    challengeId: str
    place: int
    registeredPlayerIds: list[str]
    prizeAmount: int
    unregisteredPlayers: list[str] #TODO: str is an assumption
    prizeCurrency: str

class ChallengePrize(Datatype):
    place: int
    amount: int

class ChallengePrizeConfig(Datatype):
    prizePool: int
    currency: str
    prizes: list[ChallengePrize]

class Challenge(Datatype):

    id: str
    name: str
    announcement: str
    url: str
    gameId: str
    createDate: int
    updateDate: int
    startDate: int
    endDate: int
    state: int # enum
    description: str
    rules: str
    numPlayers: int
    exactPlayers: int
    playerMatchMode: int # enum
    timeDirection: int
    enforceMs: bool
    coverImagePath: str
    contest: bool
    contestRules: str
    runCommentsMode: int # enum
    prizeConfig: ChallengePrizeConfig

class ChallengeRun(Datatype):

    id: str
    gameId: str
    challengeId: str
    time: OptField[float]
    timeWithLoads: OptField[float]
    igt: OptField[float]
    enforceMs: OptField[bool]
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: OptField[str]
    emulator: bool
    regionId: OptField[str]
    video: OptField[str]
    comment: OptField[str]
    submittedById: OptField[str]
    screened: bool
    screenedById: OptField[str]
    verified: int
    verifiedById: OptField[str]
    reason: OptField[str]
    date: int
    dateSubmitted: int
    dateVerified: OptField[int]
    dateScreened: OptField[int]
    issues: OptField[Any] #TODO: Unknown type (Any)
    playerIds: list[str]
    commentsCount: int
    place: OptField[int]
    obsolete: OptField[bool]

class Theme(Datatype):
    id: str
    url: str
    name: OptField[str]
    primaryColor: str
    panelColor: str
    panelOpacity: int
    navbarColor: int
    backgroundColor: str
    backgroundFit: int
    backgroundPosition: int
    backgroundRepeat: int
    backgroundScrolling: int
    foregroundFit: int
    foregroundPosition: int
    foregroundRepeat: int
    foregroundScrolling: int
    touchDate: int
    staticAssets: list[StaticAsset]

class Pagination(Datatype):
    count: int
    page: int
    pages: int
    per: int

class Leaderboard(Datatype):
    category: Category
    game: Game
    pagination: Pagination
    platforms: list[Platform]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]
    variables: list[Variable]

class Guide(Datatype):
    id: str
    name: str
    text: str
    date: int
    userId: str
    gameId: str

class Resource(Datatype):
    id: str
    type: int # Enum
    name: str
    description: str
    date: int
    userId: str
    gameId: str
    path: OptField[str]
    link: OptField[str]
    fileName: OptField[str]
    authorNames: str #TODO: exhaustive check for lists

class Stream(Datatype):
    id: str
    gameId: OptField[str]
    userId: OptField[str]
    areaId: OptField[str]
    url: str
    title: str
    previewUrl: str
    channelName: str
    viewers: int
    hasPb: bool
    """If the stream has a PB on SRC (and has their account linked)""" #TODO: check

class GameSettings(Datatype):
    id: str
    name: str
    url: str
    twitchName: str
    releaseDate: int #TODO: check
    milliseconds: bool
    defaultView: int # enum
    loadTimes: bool
    igt: bool
    defaultTimer: int # enum, assume TimerName?
    showEmptyTimes: bool
    rulesView: Any #TODO: check
    emulator: int # enum
    verification: bool
    requireVideo: bool
    autoVerify: bool
    regionsObsolete: bool
    platformsObsolete: bool
    discordUrl: str 
    websiteUrl: str
    rules: str
    showOnStreamsPage: int # enum
    touchDate: int
    noEvents: bool
    promoted: bool
    runCommentsMode: int # enum
    noPromote: bool
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[int] # enums
    guidePermissionType: int # enum 
    resourcePermissionType: int # enum
    staticAssets: list[StaticAsset]
    staticAssetUpdates: Any # undocumented list

class SeriesSettings(Datatype):
    name: str
    url: str
    discordUrl: str
    websiteUrl: str
    staticAssets: list[StaticAsset]
    staticAssetUpdates: Any #TODO: undocumented list

class GameModerationStats(Datatype):
    gameId: str
    state: Any #TODO: check
    count: int
    minDate: int
    maxDate: int

class AuditLogEntry(Datatype):
    id: str
    date: int
    eventType: str # enum
    actorId: str
    gameId: str
    context: Any #TODO: check

class Conversation(Datatype):
    id: str
    participantUserIds: list[str]
    lastMessageId: str
    lastMessageUser: str
    lastMessageText: str
    lastMessageDate: int
    readDate: int

class ConversationParticipant(Datatype):
    conversationId: str
    userId: str
    joinedDate: int
    leftDate: int #TODO: OptField?

class ConversationMessage(Datatype):
    id: str
    conversationId: str 
    userId: str
    text: str
    date: int

class SystemMessage(Datatype):
    id: str
    userId: str
    text: str
    date: int
    read: bool

class ForumReadStatus(Datatype):
    forumId: str
    date: int

class Notification(Datatype):
    id: str 
    date: int
    title: str
    path: str
    read: bool

class GameFollower(Datatype):
    gameId: str
    followerId: str
    pos: OptField[int]
    accessCount: int
    lastAccessDate: int

class GameRunner(Datatype):
    gameId: str 
    userId: str
    runCount: int

class UserFollower(Datatype):
    userId: str
    followerId: str

class Session(Datatype):
    signedIn: bool
    showAds: bool
    user: OptField[User]
    theme: OptField[Theme]
    powerLevel: SitePowerLevel
    dateFormat: int # enum
    timeFormat: int # enum
    timeReference: int # enum
    timeUnits: int # enum
    homepageStream: int # enum
    disableThemes: bool
    csrfToken: str
    networkToken: OptField[str] #TODO: check
    gameList: list[Game]
    gameFollowerList: list[GameFollower]
    gameModeratorList: list[GameModerator]
    gameRunnerList: list[GameRunner]
    seriesList: list[Series]
    seriesModeratorList: list[SeriesModerator]
    boostAvailableTokens: OptField[int]
    boostNextTokenDate: int
    boostNextTokenAmount: int
    userFollowerList: list[UserFollower]
    enabledExperimentIds: Any # undocumented list
    challengeModeratorList: Any # undocumented list

class ThemeSettings(Datatype):
    primaryColor: str
    panelColor: str
    panelOpacity: int
    navbarColor: str
    backgroundColor: str
    backgroundFit: bool
    backgroundPosition: int # enum
    backgroundRepeat: bool #TODO: check
    backgroundScrolling: bool #TODO: check
    foregroundFit: bool
    foregroundPosition: int # enum
    foregroundRepeat: bool #TODO: check
    foregroundScrolling: bool #TODO: check
    staticAssets: list[StaticAsset]

class ThreadReadStatus(Datatype):
    threadId: str
    date: int

class Ticket(Datatype):
    id: str
    queue: int # enum
    type: int # enum TODO: check
    status: int # enum
    requestorId: str
    dateSubmitted: int
    metadata: str
    """This is a json object that may be dependent on type"""

class UserBlock(Datatype):
    blockerId: str
    blockeeId: str

class NotificationSetting(Datatype):
    type: Any #TODO: check
    gameId: OptField[str]
    site: bool
    email: bool

class UserSettings(Datatype):
    id: str
    name: str
    url: str
    email: str
    bio: str
    powerLevel: SitePowerLevel
    areaId: str
    theme: str # TODO: check what happens w/ custom theme
    color1id: str
    color2id: str
    colorAnimate: int # enum
    avatarDecoration: dict #TODO: enabled: bool
    defaultView: int # enum
    timeReference: int # enum
    timeUnits: int # enum
    dateFormat: int # enum
    timeFormat: int # enum
    iconType: int # enum
    disableThemes: bool
    emailAuthentication: bool
    latestMaxFollowed: int
    latestMinFollowed: int
    latestTimeFollowed: int
    showMiscByDefault: bool
    showOnStreamsPage: bool
    showUnofficialGameTypes: bool
    homepageStream: int # enum
    disableMessages: bool
    showAds: bool
    pronouns: list[str]
    nameChangeDate: int
    runCommentsDisabled: bool
    followedGamesDisabled: bool
    supporterEndDate: int
    boostEndDate: int
    supporterIconType: int # enum
    supporterIconPosition: int # enum
    staticAssets: list[StaticAsset]
    staticAssetUpdates: Any # Undocumented list

class SupporterSubscription(Datatype):
    id: str
    userId: str
    providerId: int # enum
    createdAt: int
    updatedAt: int
    expiresAt: int
    planId: int # enum
    nextPeriodPlanId: int # enum
    status: int # enum
    trialEndsAt: int
    """Default 0, undocumented but assume timestamp otherwise"""
    cancelAtPeriodEnd: bool
    canceledAt: int # assume timestamp
    
class Title(Datatype):
    id: str
    title: str
    comment: str
    referenceUrl: str