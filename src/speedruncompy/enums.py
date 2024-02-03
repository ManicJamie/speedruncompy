from enum import IntEnum, StrEnum

class itemType(IntEnum):
    LIKE = 1 # Unsure if "LIKE" is the correct term here.
    RUN = 2
    THREAD = 7  # Thread (comment?)
    GAME_NEWS = 27
    SITE_NEWS = 30

class verified(IntEnum):
    PENDING = 0
    VERIFIED = 1
    REJECTED = 2

class obsoleteFilter(IntEnum):
    HIDDEN = 0,
    SHOWN = 1,
    EXCLUSIVE = 2

class verifiedFilter(IntEnum):
    OPTIONAL = 0,
    REQUIRED = 1,
    MISSING = 2

class forumType(IntEnum):
    FRONT_PAGE = 0
    SUPPORTER = 1
    GAME = 2

class TimerName(IntEnum):
    """`time`, `timeWithLoads` and `igt`.

    `time` is LRT if present, otherwise RTA.
    `timeWithLoads` is RTA if LRT is present.
    `igt` is IGT
    """
    time = 0
    """LRT if present, otherwise RTA"""
    timeWithLoads = 1
    """RTA if LRT is present"""
    igt = 2
    """IGT"""

class modLevel(IntEnum):
    VERIFIER = -1
    MODERATOR = 0
    SUPERMOD = 1

class gameType(IntEnum):
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

class permissionType(IntEnum):
    ALL = 0
    DISABLED = 1
    VERIFIED_HERE = 2
    VERIFIED_ANY = 3
    MODS_ONLY = 4

class resourceType(IntEnum):
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

class eventType(StrEnum):
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

class VariableLevelScope(IntEnum):
    FULL_GAME = 0,
    SINGLE_LEVEL = 1,
    ALL_LEVELS = -1,
    FULL_GAME_AND_ALL_LEVELS = -2

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
    GAME_REQUEST = 1,
    SERIES_REQUEST = 2,
    MOD_REQUEST = 3,
    MARATHON_REQUEST = 4,
    CONTENT_REPORT = 5,
    USER_REPORT = 6,
    BUG_REPORT = 7,
    FRONT_PAGE_REQUEST = 8,
    FEEDBACK = 9,
    STAFF_APPLICATION = 10,
    OTHER_SUPPORT = 11,
    GAME_TYPE_UPDATE = 12,
    ADD_TO_SERIES_REQUEST = 13,
    ADD_PLATFORM_REQUEST = 14,
    OTHER_GAME_REQUEST = 15,
    SUPPORTER_HELP = 16

class TicketStatus(IntEnum):
    PENDING = 0,
    APPROVED = 1,
    DENIED = 2,
    REVIEWING = 3,
    WITHDRAWN = 4

class NetworkId(IntEnum):
    """NB: does not include deprecated values that may still be visible to the API"""
    BILIBILI = 3,
    DISCORD = 5,
    FACEBOOK = 8,
    INSTAGRAM = 11,
    NICONICO = 15,
    REDDIT = 18,
    TWITCH = 29,
    TWITTER = 30,
    URL = 31,
    YOUTUBE = 32