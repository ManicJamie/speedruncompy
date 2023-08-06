from enum import Enum

class itemType(Enum):
    LIKE = 1 # Unsure if "LIKE" is the correct term here.
    RUN = 2
    THREAD = 7  # Thread (comment?)
    GAME_NEWS = 27
    SITE_NEWS = 30

class verified(Enum):
    PENDING = 0
    VERIFIED = 1
    REJECTED = 2

class forumType(Enum):
    FRONT_PAGE = 0
    SUPPORTER = 1
    GAME = 2

class timerType(Enum):
    RTA = 0
    LRT = 1 # i forgot to check this
    IGT = 2

class modLevel(Enum):
    VERIFIER = -1
    MODERATOR = 0
    SUPERMOD = 1