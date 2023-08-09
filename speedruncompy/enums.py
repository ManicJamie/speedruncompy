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

class forumType(IntEnum):
    FRONT_PAGE = 0
    SUPPORTER = 1
    GAME = 2

class timerType(IntEnum):
    RTA = 0
    LRT = 1 # i forgot to check this
    IGT = 2

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

class PowerLevel(IntEnum):
    BANNED = 0,
    USER = 1,
    CONTENT_MOD = 2,
    SITE_MOD = 3,
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