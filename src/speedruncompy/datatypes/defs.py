from typing import Literal

from bidict import frozenbidict

from ._impl import Duration_, Int64_, SpeedrunModel, Timestamp_
from .enums import *

# ruff: noqa: RUF012

class Date(SpeedrunModel):
    year: int
    month: int
    day: int
    
    def __str__(self): 
        return f"{self.year}-{self.month:02}-{self.day:02}"

class StaticAsset(SpeedrunModel):

    assetType: str
    path: str

class StaticAssetUpdate(SpeedrunModel):
    
    assetType: str
    updateContent: str
    """Example: data:image/png;base64,examplebase64data``"""
    deleteContent: bool | None = None

class VarValue(SpeedrunModel):

    variableId: str
    valueId: str

    def __str__(self):
        return f"Var {self.variableId} = {self.valueId}"

class VarValues(SpeedrunModel):

    variableId: str
    valueIds: list[str] = []


class CommentPermissions(SpeedrunModel):
    canManage: bool
    canViewComments: bool
    canPostComments: bool
    canEditComments: bool
    canDeleteComments: bool
    cannotViewReasons: list[str] = []
    cannotPostReasons: list[str] = []

class CommentableProperties(SpeedrunModel):
    disabled: bool
    locked: bool

class Commentable(SpeedrunModel):
    itemType: ItemType
    itemId: str
    properties: CommentableProperties
    permissions: CommentPermissions
    """Permissions of the logged in user.
    If not logged in, canPost will always be False."""


class Comment(SpeedrunModel):
    id: str
    itemType: ItemType
    itemId: str
    postedAt: Timestamp_
    userId: str
    text: str | None = None
    """May be omitted on deleted comments."""
    parentId: str | None = None
    editedById: str | None = None
    deleted: bool
    deletedById: str | None = None

class Like(SpeedrunModel):
    itemType: ItemType
    itemId: str
    userId: str
    likedAt: Timestamp_

class Forum(SpeedrunModel):
    id: str
    name: str
    url: str
    description: str | None = None
    type: ForumType
    threadCount: Int64_
    postCount: Int64_
    lastPostId: str | None = None
    lastPostUserId: str | None = None
    lastPostAt: Timestamp_ | None = None
    updatedAt: Timestamp_

class Thread(SpeedrunModel):
    id: str
    name: str
    forumId: str
    userId: str
    replies: Int64_
    createdAt: Timestamp_
    lastCommentId: str
    lastCommentUserId: str
    lastCommentAt: Timestamp_
    sticky: bool
    locked: bool

class RunSettings(SpeedrunModel):

    runId: str | None = None
    """Omitted when submitting a new run."""
    gameId: str
    categoryId: str
    playerNames: list[str] = []
    time: Duration_ | None = None  # Note: whichever timing method is primary to the game is required
    """LRT if it is enabled, otherwise RTA."""
    timeWithLoads: Duration_ | None = None
    """RTA if LRT is enabled."""
    igt: Duration_ | None = None
    platformId: str
    regionId: str | None = None
    emulator: bool
    video: str
    comment: str | None = None
    performedAt: Timestamp_
    values: list[VarValue] = []
    videoState: VideoState | None = None  # TODO: check if opt
    
    # TODO: this only guarantees RTA if both time and timeWithLoads is present in the run,
    # but if a LRT run is missing RTA then it will incorrectly return `time` rather than `None`
    # Correctly doing this would require knowledge of the Game data, so with cacheing or autoreqs.
    def _get_rta(self): return self.timeWithLoads if "timeWithLoads" in self.__dict__ else self.time
    def _set_rta(self, _val):
        if "timeWithLoads" in self.__dict__:
            self.timeWithLoads = _val
        else:
            self.time = _val
    _rta = property(fget=_get_rta, fset=_set_rta)
    """Decorator property that points to RTA, as this may be either `time` or `timeWithLoads`.
    
    WARN: only guaranteed RTA if RTA is not None, otherwise may falsely return LRT."""

class Series(SpeedrunModel):
    id: str
    name: str
    url: str
    addedAt: Timestamp_
    updatedAt: Timestamp_
    websiteUrl: str | None = None
    discordUrl: str | None = None
    runCount: Int64_
    activePlayerCount: Int64_
    totalPlayerCount: Int64_
    officialGameCount: Int64_
    staticAssets: list[StaticAsset] = []

class GameBase(SpeedrunModel):

    id: str
    name: str
    url: str
    type: str  # enum? is this true? afaict is always "game"
    loadTimes: bool
    milliseconds: bool
    igt: bool
    verification: bool
    autoVerify: bool | None = None  # TODO: recheck optional
    requireVideo: bool
    emulator: EmulatorType
    defaultTimer: TimerName
    validTimers: list[TimerName] = []
    releaseDate: Date | None = None  # TODO: check optional?
    addedAt: Timestamp_
    updatedAt: Timestamp_
    baseGameId: str | None = None
    trophy1stPath: str | None = None
    trophy2ndPath: str | None = None
    trophy3rdPath: str | None = None
    trophy4thPath: str | None = None
    runCommentsMode: PermissionType
    runCount: Int64_
    activePlayerCount: Int64_
    totalPlayerCount: Int64_
    boostReceivedCount: Int64_
    boostDistinctDonorsCount: Int64_
    rules: str | None = None
    rulesUpdatedAt: Timestamp_ | None = None
    viewPowerLevel: SitePowerLevel
    websiteUrl: str | None = None
    discordUrl: str | None = None
    defaultView: DefaultViewType
    guidePermissionType: PermissionType
    resourcePermissionType: PermissionType
    staticAssets: list[StaticAsset] = []
    embargoEndsAt: Timestamp_ | None = None
    embargoText: str | None = None

class Game(GameBase):
    platformIds: list[str] = []
    regionIds: list[str] = []
    gameTypeIds: list[GameType] = []

class GameStats(SpeedrunModel):
    gameId: str
    totalRuns: Int64_
    totalRunsFG: Int64_
    totalRunsIL: Int64_
    totalRunTime: Duration_
    recentRuns: Int64_
    recentRunsFG: Int64_
    recentRunsIL: Int64_
    totalPlayers: Int64_
    activePlayers: Int64_
    followers: Int64_
    guides: Int64_
    resources: Int64_
    totalRunsChallenge: Int64_
    recentRunsChallenge: Int64_

class RunCount(SpeedrunModel):

    gameId: str
    categoryId: str
    levelId: str | None = None
    variableId: str | None = None
    valueId: str | None = None
    count: int

class Category(SpeedrunModel):

    id: str
    name: str
    url: str
    position: Int64_
    gameId: str
    isMisc: bool
    isPerLevel: bool
    numPlayers: Int64_
    exactPlayers: bool
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
    enforceMs: bool
    rules: str | None = None
    rulesUpdatedAt: Timestamp_ | None = None
    archived: bool | None = None

class Variable(SpeedrunModel):

    id: str
    name: str
    url: str
    position: Int64_
    gameId: str
    description: str | None = None
    categoryScope: VarCategoryScope
    categoryId: str | None = None
    levelScope: VarLevelScope
    levelId: str | None = None
    isMandatory: bool
    isSubcategory: bool
    isUserDefined: bool
    isObsoleting: bool
    defaultValueId: str | None = None
    archived: bool
    displayMode: VarDisplayMode | None = None

class Value(SpeedrunModel):
    """Value of a variable. `VariableValue` is a selector on this type (and the underlying variable)"""
    id: str
    name: str
    url: str
    position: Int64_
    variableId: str
    isMisc: bool | None = None
    rules: str | None = None
    rulesUpdatedAt: Timestamp_ | None = None
    archived: bool

class Level(SpeedrunModel):

    id: str
    gameId: str
    name: str
    url: str
    position: Int64_
    rules: str | None = None
    rulesUpdatedAt: Timestamp_ | None = None
    archived: bool

class Platform(SpeedrunModel):

    id: str
    name: str
    url: str
    year: Int64_

class ArticleBase(SpeedrunModel):
    id: str
    slug: str
    title: str
    summary: str
    body: str
    createdAt: Timestamp_
    updatedAt: Timestamp_
    publishedAt: Timestamp_ | None = None  # TODO: check optional
    rejectedAt: Timestamp_ | None = None  # TODO: check optional
    publishTarget: str
    coverImagePath: str | None = None
    commentsCount: Int64_
    community: bool | None = None
    gameId: str | None = None
    userId: str | None = None
    editorId: str | None = None
    stickyEndsAt: Timestamp_ | None = None  # TODO: doc lists as non-optional, check

class Article(ArticleBase):
    publishTags: list[str] = []

class News(SpeedrunModel):

    id: str
    gameId: str
    userId: str
    title: str
    body: str | None = None
    """Omitted for all but the first item in `r_GetGameSummary.newsList[] `"""
    submittedAt: Timestamp_
    editedAt: Timestamp_ | None = None

class Player(SpeedrunModel):
    """Fields from `User` present in `playerLists`. May also be an unregistered player, use property `_is_registered`"""
    id: str
    name: str
    url: str | None = None
    powerLevel: SitePowerLevel | None = None
    color1Id: str | None = None
    color2Id: str | None = None
    """OptField even on full `player`"""
    colorAnimate: int | None = None
    areaId: str | None = None
    isSupporter: bool | None = None
    """OptField even on full `player`"""

    def _is_user(self): return not self.id.startswith("u-")
    # NOTE: `minimal regex: u-[a-f0-9]{8}-?[a-f0-9]{4}-?5[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}`
    _is_registered = property(fget=_is_user)
    """Checks if a player has an account or is a text label"""

class DeletedPlayer(SpeedrunModel):
    """Challenge leaderboards will continue to contain nonexistent playerList entries that no longer have an account as their IDs only."""
    id: str

class AvatarDecoration(SpeedrunModel):
    """Supporter feature for rings around names.
    
    @separateColors: If true, see this object's color Ids. If either is absent, inherit from username.
    """
    enabled: bool
    separateColors: bool | None = None
    color1Id: str | None = None
    """Defaults to username's color1Id"""
    color2Id: str | None = None
    """Defaults to username's color2Id"""

class UserBase(SpeedrunModel):
    id: str
    name: str
    altname: str | None = None
    url: str
    powerLevel: SitePowerLevel
    """Site-level, 1 is default, Meta is 4"""
    color1Id: str
    color2Id: str | None = None
    colorAnimate: int | None = None
    areaId: str
    isSupporter: bool | None = None
    avatarDecoration: AvatarDecoration | None = None
    iconType: IconType
    lastOnlineAt: Timestamp_ | None
    signedUpAt: Timestamp_
    updatedAt: Timestamp_
    staticAssets: list[StaticAsset] = []
    supporterIconType: IconType | None = None
    supporterIconPosition: IconPosition | None = None
    titleId: str | None = None
    """ID for a title given for completing a Challenge"""

class User(UserBase):
    pronouns: list[str] = []

class UserStats(SpeedrunModel):
    userId: str
    followers: Int64_
    runs: Int64_
    runsFg: Int64_
    runsIl: Int64_
    runsPending: Int64_
    runTime: Duration_ | None = None
    minRunDate: Date | None = None
    maxRunDate: Date | None = None
    commentsPosted: Int64_
    guidesCreated: Int64_
    resourcesCreated: Int64_
    threadsCreated: Int64_
    gamesBoosted: Int64_
    usersBoosted: Int64_
    followingGames: Int64_
    followingUsers: Int64_
    challengeRuns: Int64_
    challengeRunsPending: Int64_
    runVideosAtRisk: Int64_

class UserSocialConnection(SpeedrunModel):
    userId: str
    networkId: NetworkId
    value: str
    verified: bool

class UserModerationStats(SpeedrunModel):
    gameId: str
    level: GamePowerLevel
    totalRuns: Int64_
    totalTime: Duration_
    minVerifiedAt: Timestamp_
    maxVerifiedAt: Timestamp_

class UserGameFollow(SpeedrunModel):
    gameId: str
    accessCount: Int64_
    lastAccessDate: int

class UserGameRunnerStats(SpeedrunModel):
    gameId: str
    totalRuns: Int64_
    totalTime: Duration_
    uniqueLevels: Int64_
    uniqueCategories: Int64_
    minVerifiedAt: Date | None = None
    maxVerifiedAt: Date | None = None

class GameOrderGroup(SpeedrunModel):
    id: str
    name: str
    sortType: GameSortType
    gameIds: list[str] = []
    open: bool | None = None
    editing: bool | None = None

class GameOrdering(SpeedrunModel):
    defaultGroups: list[GameOrderGroup] = []
    supporterGroups: list[GameOrderGroup] = []

class UserProfile(SpeedrunModel):  # TODO: check where this exists (if anywhere?)

    userId: str
    bio: str | None = None
    signedUpAt: Timestamp_
    defaultView: DefaultViewType
    featuredFullGameRunId: str
    showMiscByDefault: bool
    gameOrdering: GameOrdering
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection] = []

class UserReducedProfile(SpeedrunModel):
    """UserProfile as returned by GetUserLeaderboard, GetUserSummary & GetUserPopoverData.
    
    Missing userStats and userSocialConnectionList."""
    userId: str
    bio: str | None = None
    signedUpAt: Timestamp_
    defaultView: DefaultViewType
    showMiscByDefault: bool
    gameOrdering: GameOrdering | None = None

class SeriesModerator(SpeedrunModel):
    seriesId: str
    userId: str
    level: GamePowerLevel

class GameModerator(SpeedrunModel):
    gameId: str
    userId: str
    level: GamePowerLevel

class ChallengeModerator(SpeedrunModel):
    
    challengeId: str
    userId: str
    level: GamePowerLevel

class GameBoost(SpeedrunModel):
    id: str
    createdAt: Timestamp_
    updatedAt: Timestamp_
    gameId: str
    anonymous: bool
    donorUserId: str | None = None
    """Omitted if anonymous is True"""
    recipientUserIds: list[str] = []
    """Appears to always be empty"""

class Region(SpeedrunModel):
    id: str
    name: str
    url: str
    flag: str

class SocialNetwork(SpeedrunModel):
    id: NetworkId
    name: str
    major: bool
    position: Int64_
    pattern: str

class Area(SpeedrunModel):
    id: str
    name: str
    fullName: str
    label: str
    flagIcon: str
    lbFlagIcon: str
    lbName: str

class Color(SpeedrunModel):
    id: str
    name: str
    darkColor: str
    """Deprecated, darkColor is always used on the site"""
    lightColor: str
    """Deprecated, colors now seem to be sorted by their name's ascending alphabetical order (A-Z)"""
    position: Int64_

class GameTypeObj(SpeedrunModel):
    id: GameType
    name: str
    url: str
    description: str

class Run(SpeedrunModel):

    id: str
    gameId: str
    categoryId: str
    levelId: str | None = None
    time: Duration_ | None = None
    timeWithLoads: Duration_ | None = None
    igt: Duration_ | None = None
    enforceMs: bool | None = None
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: str | None = None
    emulator: bool
    regionId: str | None = None
    video: str | None = None
    comment: str | None = None
    submittedById: str | None = None
    verified: Verified
    verifiedById: str | None = None
    reason: str | None = None
    performedAt: Timestamp_ | None = None
    """Appears to be omitted on some >10y old submissions"""
    submittedAt: Timestamp_ | None = None
    """Only omitted on some very old runs!"""
    verifiedAt: Timestamp_ | None = None
    obsolete: bool | None = None
    place: Int64_ | None = None
    playerIds: list[str] = []
    valueIds: list[str] = []
    orphaned: bool | None = None
    estimated: bool | None = None
    """Only shown in GetModerationRuns"""
    issues: list[str] | None = None
    videoState: VideoState

class RecordEvent(SpeedrunModel):
    performedAt: Timestamp_
    recordImprovedBy: Duration_ | None = None
    runList: list[Run] = []

class ChallengeStanding(SpeedrunModel):
    challengeId: str
    place: Int64_
    registeredPlayerIds: list[str] = []
    prizeAmount: Int64_
    unregisteredPlayers: list[str] = []  # TODO: str is an assumption
    prizeCurrency: str

class ChallengePrize(SpeedrunModel):
    place: Int64_
    amount: Int64_

class ChallengePrizeConfig(SpeedrunModel):
    prizePool: Int64_
    currency: str
    prizes: list[ChallengePrize] = []

class ChallengeGlobalRanking(SpeedrunModel):
    """Sitewide rank based on all challenges entered."""
    userId: str
    rank: Int64_
    totalEarnings: Int64_
    firstPlaces: Int64_
    secondPlaces: Int64_
    thirdPlaces: Int64_
    challengesEntered: Int64_

class Challenge(SpeedrunModel):

    id: str
    name: str
    announcement: str
    url: str
    gameId: str
    createdAt: Timestamp_
    updatedAt: Timestamp_
    startsAt: Timestamp_
    endsAt: Timestamp_
    state: ChallengeState
    description: str
    rules: str
    rulesUpdatedAt: Timestamp_ | None = None
    numPlayers: Int64_
    exactPlayers: bool
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
    enforceMs: bool
    coverImagePath: str
    challengeRules: str
    challengeRulesUpdatedAt: Timestamp_ | None = None
    runCommentsMode: PermissionType
    prizeConfig: ChallengePrizeConfig
    type: int  # TODO: enum
    phase: int  # TODO: enum

class ChallengeRun(SpeedrunModel):

    id: str
    gameId: str
    challengeId: str
    time: Duration_ | None = None
    timeWithLoads: Duration_ | None = None
    igt: Duration_ | None = None
    enforceMs: bool | None = None
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: str | None = None
    emulator: bool
    regionId: str | None = None
    video: str | None = None
    comment: str | None = None
    submittedById: str | None = None
    screened: bool
    screenedById: str | None = None
    verified: int
    verifiedById: str | None = None
    reason: str | None = None
    performedAt: Timestamp_
    submittedAt: Timestamp_
    verifiedAt: Timestamp_ | None = None
    screenedAt: Timestamp_ | None = None
    issues: None = None  # TODO: Find if this is ever Not None
    playerIds: list[str] = []
    commentsCount: Int64_
    place: Int64_ | None = None
    obsolete: bool | None = None
    videoState: VideoState

class Theme(SpeedrunModel):
    id: str
    url: str
    name: str | None = None  # TODO: check optional
    primaryColor: str
    panelColor: str
    panelOpacity: Int64_
    navbarColor: NavbarColorType
    backgroundColor: str
    backgroundFit: FitType
    backgroundPosition: PositionType
    backgroundRepeat: RepeatType
    backgroundScrolling: ScrollType
    foregroundFit: FitType
    foregroundPosition: PositionType
    foregroundRepeat: RepeatType
    foregroundScrolling: ScrollType
    updatedAt: Timestamp_
    staticAssets: list[StaticAsset] = []

class DefaultTheme(SpeedrunModel):
    """Stub theme occasionally returned by the site in place of Theme"""
    name: Literal['Default']
    url: Literal['default']
    staticAssets: list[StaticAsset] = []
    """Should always be empty"""

class Pagination(SpeedrunModel):
    count: Int64_
    page: Int64_
    pages: Int64_
    per: Int64_

class Leaderboard(SpeedrunModel):
    category: Category
    game: Game
    pagination: Pagination
    platforms: list[Platform] = []
    players: list[Player] = []
    regions: list[Region] = []
    runs: list[Run] = []
    values: list[Value] = []
    variables: list[Variable] = []
    
    _platformDict: dict[str, Platform]
    _playerDict: dict[str, Player]
    _regionDict: dict[str, Region]
    _runDict: dict[str, Run]
    _variableDict: dict[str, Variable]
    _valueDict: dict[str, Value]
    
    __condenser_map__ = frozenbidict({
        "platforms": "_platformDict",
        "players": "_playerDict",
        "regions": "_regionDict",
        "runs": "_runDict",
        "values": "_valueDict",
        "variables": "_variableDict",
    })

class Guide(SpeedrunModel):
    id: str
    name: str
    text: str
    updatedAt: Timestamp_
    userId: str
    gameId: str

class Resource(SpeedrunModel):
    id: str
    type: ResourceType
    name: str
    description: str
    updatedAt: Timestamp_
    userId: str
    gameId: str | None = None
    path: str | None = None
    link: str | None = None
    fileName: str | None = None
    authorNames: str  # TODO: exhaustive check for lists

class Stream(SpeedrunModel):
    id: str
    gameId: str | None = None
    userId: str | None = None
    areaId: str | None = None
    url: str
    title: str
    previewUrl: str
    channelName: str
    viewers: Int64_
    hasPb: bool
    """If the stream has a PB on SRC (and has their account linked)"""  # TODO: check

class GameSettings(SpeedrunModel):
    id: str
    name: str
    url: str
    twitchName: str
    releaseDate: Date
    embargoEndsAt: Timestamp_ | None = None
    milliseconds: bool
    defaultView: DefaultViewType
    loadTimes: bool
    igt: bool
    defaultTimer: TimerName
    showEmptyTimes: bool
    rulesView: bool
    emulator: EmulatorType
    verification: bool
    requireVideo: bool
    autoVerify: bool
    regionsObsolete: bool
    platformsObsolete: bool
    discordUrl: str
    websiteUrl: str
    rules: str
    rulesUpdatedAt: Timestamp_ | None = None
    showOnStreamsPage: Int64_
    updatedAt: Timestamp_
    noEvents: bool
    promoted: bool
    runCommentsMode: PermissionType
    noPromote: bool
    platformIds: list[str] = []
    regionIds: list[str] = []
    gameTypeIds: list[GameType] = []
    guidePermissionType: PermissionType
    resourcePermissionType: PermissionType
    staticAssets: list[StaticAsset] = []
    staticAssetUpdates: list[StaticAssetUpdate] = []

class SeriesSettings(SpeedrunModel):
    name: str
    url: str
    discordUrl: str
    websiteUrl: str
    releaseDate: Date | None = None
    staticAssets: list[StaticAsset] = []
    staticAssetUpdates: list[StaticAssetUpdate] = []

class GameModerationStats(SpeedrunModel):
    gameId: str
    state: int  # enum? appears to always be 0
    count: Int64_
    minSubmittedAt: Timestamp_ | None = None
    maxSubmittedAt: Timestamp_ | None = None

class AuditLogEntry(SpeedrunModel):
    id: str
    recordedAt: Timestamp_
    eventType: str  # EventType
    actorId: str
    gameId: str
    context: str
    """A json dict of extra context based on eventType."""
    userId: str | None = None
    references: list[dict]  = []  # TODO: narrow type

class Conversation(SpeedrunModel):
    id: str
    participantUserIds: list[str] = []
    lastMessageId: str
    lastMessageUserId: str | None = None
    lastMessageText: str | None = None
    lastMessageAt: Timestamp_
    lastReadAt: Timestamp_

class ConversationLightweight(SpeedrunModel):  # TODO: update
    id: str
    participantUserIds: list[str]  # TODO: May always be empty?
    lastMessageId: str
    lastMessageDate: int

class ConversationParticipant(SpeedrunModel):
    conversationId: str
    userId: str
    leftAt: Timestamp_ | None = None

class MessageBase(SpeedrunModel):
    id: str
    userId: str
    text: str
    sentAt: Timestamp_

class ConversationMessage(MessageBase):
    conversationId: str

class SystemMessage(MessageBase):
    read: bool

class ForumReadStatus(SpeedrunModel):
    forumId: str
    lastReadAt: Timestamp_

class Notification(SpeedrunModel):
    id: str
    createdAt: Timestamp_
    title: str
    path: str
    read: bool

class GameFollower(SpeedrunModel):
    gameId: str
    followerId: str
    position: Int64_ | None = None  # TODO: recheck optional
    accessCount: Int64_
    lastAccessedAt: Timestamp_

class GameRunner(SpeedrunModel):
    gameId: str
    userId: str
    runCount: Int64_

class UserFollower(SpeedrunModel):
    userId: str
    followerId: str

class Session(SpeedrunModel):
    signedIn: bool
    showAds: bool
    user: User | None = None
    theme: Theme | None = None
    powerLevel: SitePowerLevel
    dateFormat: DateFormat
    timeFormat: TimeFormat
    timeReference: TimeReference
    timeUnits: TimeDisplayUnits
    homepageStream: HomepageStreamType
    disableThemes: bool
    csrfToken: str
    networkToken: str | None = None
    gameList: list[Game] = []
    gameFollowerList: list[GameFollower] = []
    gameModeratorList: list[GameModerator] = []
    gameRunnerList: list[GameRunner] = []
    seriesList: list[Series] = []
    seriesModeratorList: list[SeriesModerator] = []
    boostAvailableTokens: Int64_ | None = None
    boostNextTokenAt: Timestamp_ | None = None
    boostNextTokenAmount: Int64_
    userFollowerList: list[UserFollower] = []
    enabledExperimentIds: list[str] = [] # TODO: check
    challengeModeratorList: list[ChallengeModerator] = [] # TODO: check

class ThemeSettings(SpeedrunModel):
    primaryColor: str
    panelColor: str
    panelOpacity: Int64_  # TODO: quantized mod 5?
    navbarColor: NavbarColorType
    backgroundColor: str
    backgroundFit: FitType
    backgroundPosition: PositionType
    backgroundRepeat: RepeatType
    backgroundScrolling: ScrollType
    foregroundFit: FitType
    foregroundPosition: PositionType
    foregroundRepeat: RepeatType
    foregroundScrolling: ScrollType
    staticAssets: list[StaticAsset] = []
    staticAssetUpdates: list[StaticAssetUpdate] = []

class ThreadReadStatus(SpeedrunModel):
    threadId: str
    lastReadAt: Timestamp_

class Ticket(SpeedrunModel):
    id: str
    queue: TicketQueueType
    type: TicketType
    status: TicketStatus
    requestedById: str
    submittedAt: Timestamp_
    resolvedAt: Timestamp_ | None = None
    metadata: str
    """This is a json object that may be dependent on type"""

class TicketNote(SpeedrunModel):
    id: str
    ticketId: str
    readerId: str
    submittedAt: Timestamp_
    note: str
    isMessage: bool
    isRead: bool

class UserCount(SpeedrunModel):
    userId: str
    count: Int64_

class UserBlock(SpeedrunModel):
    blockerId: str
    blockeeId: str

class NotificationSetting(SpeedrunModel):
    type: int  # enum
    gameId: str | None = None
    site: bool
    email: bool

"""A different type of notification are returned by `GetStaticData` than in other areas."""
class NotificationSettingStaticData(SpeedrunModel):
    id: int  # NOTE: This is actually transmitted as a number, despite being an integer. Damnit.
    group: str
    title: str
    position: Int64_
    gameSpecific: bool
    siteDefault: bool
    emailDefault: bool

class UserSettings(SpeedrunModel):
    id: str
    name: str
    url: str
    email: str
    bio: str
    powerLevel: SitePowerLevel
    areaId: str
    theme: str
    """May be `<gameUrl>`, `user/<userUrl>` or `Default`"""
    color1Id: str
    color2Id: str | None = None
    colorAnimate: int  # enum
    avatarDecoration: AvatarDecoration  # TODO: check
    defaultView: DefaultViewType
    timeReference: TimeReference
    timeUnits: TimeDisplayUnits
    dateFormat: DateFormat
    timeFormat: TimeFormat
    iconType: IconType
    disableThemes: bool
    emailAuthentication: bool
    latestMaxFollowed: Int64_
    latestMinFollowed: Int64_
    latestTimeFollowed: Duration_
    showMiscByDefault: bool
    showOnStreamsPage: bool
    homepageStream: HomepageStreamType
    disableMessages: bool
    showAds: bool
    pronouns: list[str] = []
    nameChangedAt: Timestamp_ | None = None
    runCommentsDisabled: bool
    followedGamesDisabled: bool
    supporterEndsAt: Timestamp_ | None = None
    boostEndsAt: Timestamp_ | None = None
    supporterIconType: IconType
    supporterIconPosition: IconPosition
    featuredFullGameRunId: str | None = None
    featuredLevelRunId: str | None = None
    staticAssets: list[StaticAsset] = []
    staticAssetUpdates: list[StaticAssetUpdate] = []

class SupporterCredit(SpeedrunModel):
    id: str
    userId: str
    providerId: int  # enum
    createdAt: Timestamp_
    updatedAt: Timestamp_
    creditType: int  # enum
    amount: Int64_
    currency: str
    receivedAt: Timestamp_
    subscriptionId: str
    periodStartsAt: Timestamp_
    periodEndsAt: Timestamp_
    providerItemId: str

class SupporterCode(SpeedrunModel):
    id: str
    code: str
    description: str
    duration: Duration_
    userId: str
    createdAt: Timestamp_
    updatedAt: Timestamp_
    redeemedAt: Timestamp_ | None
    revokedAt: Timestamp_ | None

class SupporterSubscription(SpeedrunModel):
    id: str
    userId: str
    providerId: int  # enum
    createdAt: Timestamp_
    updatedAt: Timestamp_
    expiresAt: Timestamp_ | None
    planId: Int64_  # enum
    nextPeriodPlanId: Int64_  # enum
    status: int  # enum
    trialEndsAt: Timestamp_
    """Default 0, undocumented but assume timestamp otherwise"""
    cancelAtPeriodEnd: bool
    canceledAt: Timestamp_
    
class Title(SpeedrunModel):
    """User reward for completing a Challenge."""
    id: str
    title: str
    comment: str
    referenceUrl: str
