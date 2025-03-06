from enum import IntEnum, StrEnum

class ItemType(IntEnum):
    """The type of the item this object is referencing (eg. a comment on either a run or a thread)"""
    UNKNOWN = 0
    COMMENT = 1
    RUN = 2
    GAME = 3
    GUIDE = 4
    RESOURCE = 5
    USER = 6
    THREAD = 7
    GAME_MOD = 8
    CATEGORY = 9
    LEVEL = 10
    GAME_REQUEST = 11
    TICKET = 22
    TICKET_NOTE = 23
    NEWS = 27
    GAME_BOOST_TOKEN = 28
    GAME_BOOST = 29
    ARTICLE = 30
    USER_FOLLOWER = 31
    CHALLENGE = 32
    CHALLENGE_RUN = 33

class Verified(IntEnum):
    PENDING = 0
    VERIFIED = 1
    REJECTED = 2

class ObsoleteFilter(IntEnum):
    HIDDEN = 0
    SHOWN = 1
    EXCLUSIVE = 2

class VerifiedFilter(IntEnum):
    AWAITING = 0  # Speedrun.com calls it "Awaiting" in its code on this enum
    VERIFIED = 1
    REJECTED = 2

class VideoFilter(IntEnum):
    OPTIONAL = 0
    REQUIRED = 1
    MISSING = 2

class VideoState(IntEnum):
    """Video at-risk status for Twitch Highlights and the like."""
    UNKNOWN = 0
    AT_RISK = 1
    SAFE = 2
    ABANDONED = 3

class EmulatorFilter(IntEnum):
    HIDDEN = 0
    SHOWN = 1
    EXCLUSIVE = 2

class ForumType(IntEnum):
    FRONT_PAGE = 1
    SUPPORTER = 2
    GAME = 3

class TimerName(IntEnum):
    """`time` is LRT if present, otherwise RTA.
    
    `timeWithLoads` is RTA if LRT is present.
    
    `igt` is IGT
    """
    time = 0
    """LRT if present, otherwise RTA"""
    timeWithLoads = 1
    """RTA if LRT is present"""
    igt = 2
    """IGT"""

class GameType(IntEnum):
    """Classifiers for games, provided in `Game.gameTypeIds`."""
    ROM_HACK = 1
    MODIFICATION = 2
    FAN_GAME = 3
    WEB_GAME = 4
    PRERELEASE_GAME = 5
    MOBILE_GAME = 6
    EXPANSION = 7
    CATEGORY_EXTENSIONS = 8
    MULTIPLE_GAMES = 9
    MINI_GAME = 10
    SERVER_MAP = 11
    HOMEBREW_GAME = 12

class GameOrderType(IntEnum):
    NAME = 1
    NEWEST_RELEASED = 2
    OLDEST_RELEASED = 3
    MOST_ACTIVE = 4
    LEAST_ACTIVE = 5
    MOST_PLAYERS = 6
    LEAST_PLAYERS = 7
    MOST_RUNS = 8
    LEAST_RUNS = 9
    NEWEST_ADDED = 10
    OLDEST_ADDED = 11

class ResourceType(IntEnum):
    TOOL = 1
    SAVE = 2
    SPLITS = 3
    PATCH = 4

class GamePowerLevel(IntEnum):
    VERIFIER = -1
    MOD = 0
    SUPERMOD = 1

class SitePowerLevel(IntEnum):
    BANNED = 0
    USER = 1
    CONTENT_MOD = 2
    SITE_MOD = 3
    SITE_ADMIN = 4

class EventType(StrEnum):
    NONE = ""
    CATEGORY_CREATED = "category-created"
    CATEGORY_REMOVED = "category-removed"
    CATEGORY_RESTORED = "category-restored"
    CATEGORY_UPDATED = "category-updated"
    COMMENT_CREATED = "comment-created"
    COMMENT_DELETED = "comment-deleted"
    COMMENT_UPDATED = "comment-updated"
    GAME_COVERS_UPDATED = "game-covers-updated"
    GAME_CREATED = "game-created"
    GAME_MODERATOR_CREATED = "game-moderator-created"
    GAME_MODERATOR_REMOVED = "game-moderator-removed"
    GAME_MODERATOR_UPDATED = "game-moderator-updated"
    GAME_NEWS_POST_CREATED = "game-news-post-created"
    GAME_NEWS_POST_EDITED = "game-news-post-edited"
    GAME_NEWS_POST_REMOVED = "game-news-post-removed"
    GAME_RESTORED = "game-restored"
    GAME_UPDATED = "game-updated"
    GAMEREQUEST_REVIEWED = "gamerequest-reviewed"
    LEVEL_CREATED = "level-created"

class TicketQueueType(IntEnum):
    GAME_REQUESTS = 1
    SERIES_REQUESTS = 2
    MOD_REPORTS = 3
    MARATHON_REQUESTS = 4
    CONTENT_REPORTS = 5
    USER_REPORTS = 6
    BUG_REPORTS = 7
    FRONT_PAGE_REQUESTS = 8
    FEEDBACK = 9
    STAFF_APPLICATIONS = 10
    SUPPORT = 11
    CONTENT_REQUESTS = 12
    SUPPORTER = 13

class TicketType(IntEnum):
    GAME_REQUEST = 1
    SERIES_REQUEST = 2
    MOD_REQUEST = 3
    MARATHON_REQUEST = 4
    CONTENT_REPORT = 5
    USER_REPORT = 6
    BUG_REPORT = 7
    FRONT_PAGE_REQUEST = 8
    FEEDBACK = 9
    STAFF_APPLICATION = 10
    OTHER_SUPPORT = 11
    GAME_TYPE_UPDATE = 12
    ADD_TO_SERIES_REQUEST = 13
    ADD_PLATFORM_REQUEST = 14
    OTHER_GAME_REQUEST = 15
    SUPPORTER_HELP = 16

class TicketStatus(IntEnum):
    PENDING = 0
    APPROVED = 1
    DENIED = 2
    REVIEWING = 3
    WITHDRAWN = 4

class DefaultViewType(IntEnum):
    FULL_GAME = 0
    LEVELS = 1

class ChallengeState(IntEnum):
    DRAFT = 0
    PUBLISHED = 1
    FINALIZED = 2

#region Game

class TimeDirection(IntEnum):
    ASCENDING = 0
    DESCENDING = 1

class VarCategoryScope(IntEnum):
    SINGLE = 1
    ALL = -1

class VarLevelScope(IntEnum):
    FULL_GAME = 0
    SINGLE_LEVEL = 1
    LEVELS = -1
    ALL = -2

class VarDisplayMode(IntEnum):
    AUTO = 0
    DROPDOWN = 1
    BUTTONS = 2

class EmulatorType(IntEnum):
    HIDDEN = 0
    SHOWN = 1
    BANNED = -1

class PlayerMatchMode(IntEnum):
    ALL_PLAYERS_IN_ORDER = 0
    ALL_PLAYERS_ANY_ORDER = 1
    ANY_PLAYERS_IN_ORDER = 2
    ANY_PLAYERS_ANY_ORDER = 3

class PermissionType(IntEnum):
    """Who is allowed to perform an action (posting comments, guides or resources)."""
    ALL = 0
    DISABLED = 1
    VERIFIED_HERE = 2
    VERIFIED_ANY = 3
    MODS_ONLY = 4

#endregion Game

#region User

class IconType(IntEnum):
    NONE = 0
    DEFAULT = 1
    CUSTOM = 2

class IconPosition(IntEnum):
    BEFORE = 0
    AFTER = 1

class HomepageStreamType(IntEnum):
    MUTED = 0
    PAUSED = 1
    HIDDEN = 2

class GameSortType(IntEnum):
    ALPHABETICAL = 0
    CHRONOLOGICAL = 1
    CUSTOM = 2

class TimeDisplayUnits(IntEnum):
    EXPLICIT = 0
    COLON = 1

class TimeReference(IntEnum):
    ABSOLUTE = 0
    RELATIVE = 1

class DateFormat(IntEnum):
    YYYY_MM_DD = 0
    DD_MM_YYYY = 1
    MM_DD_YYYY = 2

class TimeFormat(IntEnum):
    HH_MM = 0
    HH_MM_SS = 1
    HH_MM_12h = 2
    HH_MM_SS_12h = 3

class NetworkId(IntEnum):
    """NB: Values prefixed with `_` are deprecated and not visible on the site or settable, but may still be returned by the API."""
    BILIBILI = 3
    DISCORD = 5
    FACEBOOK = 8
    INSTAGRAM = 11
    NICONICO = 15
    REDDIT = 18
    TWITCH = 29
    TWITTER = 30
    WEBSITE = 31
    YOUTUBE = 32
    BLUESKY = 34
    THREADS = 35
    # Deprecated values
    _ASK_FM = 1
    _BATTLE_NET = 2
    _DEVIANTART = 4
    _DOUYU = 6
    _DUOLINGO = 7
    _GOOGLEPLUS = 9
    _GPODCASTS = 10
    _ITUNES = 12
    _MIXER = 13
    _SPLITS_IO = 22
    _MMRTA = 14
    _PATREON = 16
    _PINTEREST = 17
    _SMASHCAST = 19
    _SNAPCHAT = 20
    _SOUNDCLOUD = 21
    _SPLITSIO = 22
    _SPOTIFY = 23
    _SPOTIFYSHOW = 24
    _SRL = 25
    _STEAM = 26
    _STITCHER = 27
    _TUMBLR = 28
    _ZSR = 33

#endregion User

#region Theme

class NavbarColorType(IntEnum):
    PRIMARY = 0
    PANEL = 1

class ScrollType(IntEnum):
    NONE = 0
    SLOW = 1
    MEDIUM = 2
    FAST = 3

class PositionType(IntEnum):
    TL = 0
    T = 1
    TR = 2
    L = 3
    C = 4
    R = 5
    BL = 6
    B = 7
    BR = 8

class RepeatType(IntEnum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = 3

class FitType(IntEnum):
    ORIGINAL = 0
    FIT = 1

#endregion Theme

#region Supporter
class SupportPlanPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"

#endregion Supporter
