from typing import Optional
from bidict import frozenbidict

from .enums import *
from ._impl import SpeedrunModel

class StaticAsset(SpeedrunModel):

    assetType: str
    path: str

class StaticAssetUpdate(SpeedrunModel):
    
    assetType: str
    updateContent: str
    """Example: data:image/png;base64,examplebase64data``"""
    deleteContent: Optional[bool] = None

class VarValue(SpeedrunModel):

    variableId: str
    valueId: str

    def __str__(self):
        return f"Var {self.variableId} = {self.valueId}"

class VarValues(SpeedrunModel):

    variableId: str
    valueIds: list[str]

class RuntimeTuple(SpeedrunModel):

    hour: int
    minute: int
    second: int
    millisecond: int
    
    @classmethod
    def from_combined_time(cls, time: float | int):
        return cls.model_construct(values={
            "hour": int(time // 3600),
            "minute": int((time // 60) % 60),
            "second": int(time % 60),
            "millisecond": int((time * 1000) % 1)
        })
    
    def __str__(self):
        return f"{f'{self.hour}:' if self.hour != 0 else ''}{self.minute:02}:{self.second:02}{f'.{self.millisecond:03}' if self.millisecond != 0 else ''}"
    
    def __repr__(self) -> str:
        return f"{self.hour}:{self.minute:02}:{self.second:02}.{self.millisecond:03}"

class CommentPermissions(SpeedrunModel):
    canManage: bool
    canViewComments: bool
    canPostComments: bool
    canEditComments: bool
    canDeleteComments: bool
    cannotViewReasons: list[str]
    cannotPostReasons: list[str]

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
    date: int
    userId: str
    text: Optional[str] = None
    """May be omitted on deleted comments."""
    parentId: Optional[str] = None
    deleted: bool
    deletedUserId: Optional[str] = None

class Like(SpeedrunModel):
    itemType: ItemType
    itemId: str
    userId: str
    date: int

class Forum(SpeedrunModel):
    id: str
    name: str
    url: str
    description: Optional[str] = None
    type: ForumType
    threadCount: int
    postCount: int
    lastPostId: str
    lastPostUserId: str
    lastPostDate: int
    touchDate: int

class Thread(SpeedrunModel):
    id: str
    name: str
    gameId: str
    forumId: str
    userId: str
    replies: int
    created: int
    lastCommentId: str
    lastCommentUserId: str
    lastCommentDate: int
    sticky: bool
    locked: bool

class RunSettings(SpeedrunModel):

    runId: Optional[str] = None
    """Omitted when submitting a new run."""
    gameId: str
    categoryId: str
    playerNames: list[str]
    time: Optional[RuntimeTuple] = None  # Note: whichever timing method is primary to the game is required
    """LRT if it is enabled, otherwise RTA."""
    timeWithLoads: Optional[RuntimeTuple] = None
    """RTA if LRT is enabled."""
    igt: Optional[RuntimeTuple] = None
    platformId: str
    emulator: bool
    video: str
    comment: str
    date: int
    values: list[VarValue]  # type:ignore
    videoState: Optional[VideoState] = None  # TODO: check if opt
    
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
    addedDate: int
    touchDate: int
    websiteUrl: Optional[str] = None
    discordUrl: Optional[str] = None
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    officialGameCount: int
    staticAssets: list[StaticAsset]

class Game(SpeedrunModel):

    id: str
    name: str
    url: str
    type: str  # enum? is this true? afaict is always "game"
    loadtimes: bool
    milliseconds: bool
    igt: bool
    verification: bool
    autoVerify: Optional[bool] = None  # Why is this OptField????? I hate SRC
    requireVideo: bool
    emulator: EmulatorType
    defaultTimer: TimerName
    validTimers: list[TimerName]
    releaseDate: Optional[int] = None
    addedDate: int
    touchDate: int
    baseGameId: Optional[str] = None
    coverPath: str
    trophy1stPath: Optional[str] = None
    trophy2ndPath: Optional[str] = None
    trophy3rdPath: Optional[str] = None
    trophy4thPath: Optional[str] = None
    runCommentsMode: PermissionType
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    boostReceivedCount: int
    boostDistinctDonorsCount: int
    rules: Optional[str] = None
    viewPowerLevel: SitePowerLevel
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[GameType]
    websiteUrl: Optional[str] = None
    discordUrl: Optional[str] = None
    defaultView: DefaultViewType
    guidePermissionType: PermissionType
    resourcePermissionType: PermissionType
    staticAssets: list[StaticAsset]
    embargoDate: Optional[int] = None
    embargoText: Optional[str] = None

class GameStats(SpeedrunModel):
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
    totalRunsChallenge: int
    recentRunsChallenge: int

class RunCount(SpeedrunModel):

    gameId: str
    categoryId: str
    levelId: Optional[str] = None
    variableId: Optional[str] = None
    valueId: Optional[str] = None
    count: int

class Category(SpeedrunModel):

    id: str
    name: str
    url: str
    pos: int
    gameId: str
    isMisc: bool
    isPerLevel: bool
    numPlayers: int
    exactPlayers: bool
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
    enforceMs: bool
    rules: Optional[str] = None
    archived: Optional[bool] = None

class Variable(SpeedrunModel):

    id: str
    name: str
    url: str
    pos: int
    gameId: str
    description: Optional[str] = None
    categoryScope: VarCategoryScope
    categoryId: Optional[str] = None
    levelScope: VarLevelScope
    levelId: Optional[str] = None
    isMandatory: bool
    isSubcategory: bool
    isUserDefined: bool
    isObsoleting: bool
    defaultValue: Optional[str] = None
    archived: bool
    displayMode: Optional[VarDisplayMode] = None

class Value(SpeedrunModel):
    """Value of a variable. `VariableValue` is a selector on this type (and the underlying variable)"""
    id: str
    name: str
    url: str
    pos: int
    variableId: str
    isMisc: Optional[bool] = None
    rules: Optional[str] = None
    archived: bool

class Level(SpeedrunModel):

    id: str
    gameId: str
    name: str
    url: str
    pos: int
    rules: Optional[str] = None
    archived: bool

class Platform(SpeedrunModel):

    id: str
    name: str
    url: str
    year: int

class Article(SpeedrunModel):

    id: str
    slug: str
    title: str
    summary: str
    body: str
    createDate: int
    updateDate: int
    publishDate: Optional[int] = None
    rejectDate: Optional[int] = None
    publishTarget: str
    publishTags: list[str]
    coverImagePath: Optional[str] = None
    commentsCount: int
    community: Optional[bool] = None
    gameId: Optional[str] = None
    userId: Optional[str] = None
    editorId: Optional[str] = None
    stickyDate: Optional[int] = None

class News(SpeedrunModel):

    id: str
    gameId: str
    userId: str
    title: str
    body: Optional[str] = None
    """Omitted for all but the first item in `r_GetGameSummary.newsList[]`"""
    dateSubmitted: int

class Player(SpeedrunModel):
    """Fields from `User` present in `playerLists`. May also be an unregistered player, use property `_is_registered`"""
    id: str
    name: str
    url: Optional[str] = None
    powerLevel: Optional[SitePowerLevel] = None
    color1Id: Optional[str] = None
    color2Id: Optional[str] = None
    """OptField even on full `player`"""
    colorAnimate: Optional[int] = None
    areaId: Optional[str] = None
    isSupporter: Optional[bool] = None
    """OptField even on full `player`"""

    def _is_user(self): return not self.id.startswith("u-")
    # NOTE: `minimal regex: u-[a-f0-9]{8}-?[a-f0-9]{4}-?5[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}`
    _is_registered = property(fget=_is_user)
    """Checks if a player has an account or is a text label"""

class AvatarDecoration(SpeedrunModel):
    """Supporter feature for rings around names.
    
    @separateColors: If true, see this object's color Ids. If either is absent, inherit from username.
    """
    enabled: bool
    separateColors: Optional[bool] = None
    color1Id: Optional[str] = None
    """Defaults to username's color1Id"""
    color2Id: Optional[str] = None
    """Defaults to username's color2Id"""

class User(SpeedrunModel):
    id: str
    name: str
    altname: Optional[str] = None
    url: str
    pronouns: list[str]
    powerLevel: SitePowerLevel
    """Site-level, 1 is default, Meta is 4"""
    color1Id: str
    color2Id: Optional[str] = None
    colorAnimate: Optional[int] = None
    areaId: str
    isSupporter: Optional[bool] = None
    avatarDecoration: Optional[AvatarDecoration] = None
    iconType: IconType
    onlineDate: int
    signupDate: int
    touchDate: int
    staticAssets: list[StaticAsset]
    supporterIconType: Optional[IconType] = None
    supporterIconPosition: Optional[IconPosition] = None
    titleId: Optional[str] = None
    """ID for a title given for completing a Challenge"""

class UserStats(SpeedrunModel):
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
    runVideosAtRisk: int

class UserSocialConnection(SpeedrunModel):
    userId: str
    networkId: NetworkId
    value: str
    verified: bool

class UserModerationStats(SpeedrunModel):
    gameId: str
    level: GamePowerLevel
    totalRuns: int
    totalTime: int
    minDate: int
    maxDate: int

class UserGameFollow(SpeedrunModel):
    gameId: str
    accessCount: int
    lastAccessDate: int

class UserGameRunnerStats(SpeedrunModel):
    gameId: str
    totalRuns: int
    totalTime: int
    uniqueLevels: int
    uniqueCategories: int
    minDate: int
    maxDate: int

class GameOrderGroup(SpeedrunModel):
    id: str
    name: str
    sortType: GameSortType
    gameIds: list[str]
    open: Optional[bool] = None
    editing: Optional[bool] = None

class GameOrdering(SpeedrunModel):
    defaultGroups: list[GameOrderGroup]
    supporterGroups: list[GameOrderGroup]

class UserProfile(SpeedrunModel):  # TODO: check where this exists (if anywhere?)

    userId: str
    bio: Optional[str] = None
    signupDate: int
    defaultView: DefaultViewType
    showMiscByDefault: bool
    gameOrdering: GameOrdering
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]

class UserReducedProfile(SpeedrunModel):
    """UserProfile as returned by GetUserLeaderboard, GetUserSummary & GetUserPopoverData.
    
    Missing userStats and userSocialConnectionList."""
    userId: str
    bio: Optional[str] = None
    signupDate: int
    defaultView: DefaultViewType
    showMiscByDefault: bool
    gameOrdering: Optional[GameOrdering] = None

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
    createdAt: int
    updatedAt: int
    gameId: str
    anonymous: bool
    donorUserId: Optional[str] = None
    """Omitted if anonymous is True"""
    recipientUserIds: list[str]
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
    pos: int
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
    pos: int

class GameTypeObj(SpeedrunModel):
    id: GameType
    name: str
    url: str
    description: str
    allowBaseGame: bool

class Run(SpeedrunModel):

    id: str
    gameId: str
    categoryId: str
    levelId: Optional[str] = None
    time: Optional[float] = None
    timeWithLoads: Optional[float] = None
    igt: Optional[float] = None
    enforceMs: Optional[bool] = None
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: Optional[str] = None
    emulator: bool
    regionId: Optional[str] = None
    video: Optional[str] = None
    comment: Optional[str] = None
    submittedById: Optional[str] = None
    verified: Verified
    verifiedById: Optional[str] = None
    reason: Optional[str] = None
    date: int
    dateSubmitted: Optional[int] = None
    """Only omitted on some very old runs!"""
    dateVerified: Optional[int] = None
    hasSplits: bool
    obsolete: Optional[bool] = None
    place: Optional[int] = None
    playerIds: list[str]
    valueIds: list[str]
    orphaned: Optional[bool] = None
    estimated: Optional[bool] = None
    """Only shown in GetModerationRuns"""
    issues: Optional[list[str] | None] = None
    videoState: VideoState

class ChallengeStanding(SpeedrunModel):
    challengeId: str
    place: int
    registeredPlayerIds: list[str]
    prizeAmount: int
    unregisteredPlayers: list[str]  # TODO: str is an assumption
    prizeCurrency: str

class ChallengePrize(SpeedrunModel):
    place: int
    amount: int

class ChallengePrizeConfig(SpeedrunModel):
    prizePool: int
    currency: str
    prizes: list[ChallengePrize]

class GlobalChallengeRanking(SpeedrunModel):
    """Sitewide rank based on all challenges entered."""
    userId: str
    rank: int
    totalEarnings: int
    firstPlaces: int
    secondPlaces: int
    thirdPlaces: int
    challengesEntered: int

class Challenge(SpeedrunModel):

    id: str
    name: str
    announcement: str
    url: str
    gameId: str
    createDate: int
    updateDate: int
    startDate: int
    endDate: int
    state: ChallengeState
    description: str
    rules: str
    numPlayers: int
    exactPlayers: bool
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
    enforceMs: bool
    coverImagePath: str
    challengeRules: str
    runCommentsMode: PermissionType
    prizeConfig: ChallengePrizeConfig
    type: int  # TODO: enum
    phase: int  # TODO: enum

class ChallengeRun(SpeedrunModel):

    id: str
    gameId: str
    challengeId: str
    time: Optional[float] = None
    timeWithLoads: Optional[float] = None
    igt: Optional[float] = None
    enforceMs: Optional[bool] = None
    """Deprecated recent addition, bug SRC to readd this"""
    platformId: Optional[str] = None
    emulator: bool
    regionId: Optional[str] = None
    video: Optional[str] = None
    comment: Optional[str] = None
    submittedById: Optional[str] = None
    screened: bool
    screenedById: Optional[str] = None
    verified: int
    verifiedById: Optional[str] = None
    reason: Optional[str] = None
    date: int
    dateSubmitted: int
    dateVerified: Optional[int] = None
    dateScreened: Optional[int] = None
    issues: Optional[None] = None  # TODO: Find if this is ever Not None
    playerIds: list[str]
    commentsCount: int
    place: Optional[int] = None
    obsolete: Optional[bool] = None
    videoState: VideoState

class Theme(SpeedrunModel):
    id: str
    url: str
    name: Optional[str] = None  # TODO: check optional
    primaryColor: str
    panelColor: str
    panelOpacity: int
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
    touchDate: int
    staticAssets: list[StaticAsset]

class Pagination(SpeedrunModel):
    count: int
    page: int
    pages: int
    per: int

class Leaderboard(SpeedrunModel):
    category: Category
    game: Game
    pagination: Pagination
    platforms: list[Platform]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]
    variables: list[Variable]
    
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
    date: int
    userId: str
    gameId: str

class Resource(SpeedrunModel):
    id: str
    type: ResourceType
    name: str
    description: str
    date: int
    userId: str
    gameId: str
    path: Optional[str] = None
    link: Optional[str] = None
    fileName: Optional[str] = None
    authorNames: str  # TODO: exhaustive check for lists

class Stream(SpeedrunModel):
    id: str
    gameId: Optional[str] = None
    userId: Optional[str] = None
    areaId: Optional[str] = None
    url: str
    title: str
    previewUrl: str
    channelName: str
    viewers: int
    hasPb: bool
    """If the stream has a PB on SRC (and has their account linked)"""  # TODO: check

class GameSettings(SpeedrunModel):
    id: str
    name: str
    url: str
    twitchName: str
    releaseDate: int
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
    showOnStreamsPage: int  # enum
    touchDate: int
    noEvents: bool
    promoted: bool
    runCommentsMode: PermissionType
    noPromote: bool
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[GameType]
    guidePermissionType: PermissionType
    resourcePermissionType: PermissionType
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class SeriesSettings(SpeedrunModel):
    name: str
    url: str
    discordUrl: str
    websiteUrl: str
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class GameModerationStats(SpeedrunModel):
    gameId: str
    state: int  # enum? appears to always be 0
    count: int
    minDate: Optional[int] = None
    maxDate: Optional[int] = None

class AuditLogEntry(SpeedrunModel):
    id: str
    date: int
    eventType: str  # EventType
    actorId: str
    gameId: str
    context: str
    """A json dict of extra context based on eventType."""
    userId: Optional[str] = None

class Conversation(SpeedrunModel):
    id: str
    participantUserIds: list[str]
    lastMessageId: str
    lastMessageUser: str
    lastMessageText: str
    lastMessageDate: int
    readDate: int

class ConversationLightweight(SpeedrunModel):
    id: str
    participantUserIds: list[str]  # TODO: May always be empty?
    lastMessageId: str
    lastMessageDate: int

class ConversationParticipant(SpeedrunModel):
    conversationId: str
    userId: str
    joinedDate: int
    leftDate: int  # TODO: OptField?

class ConversationMessage(SpeedrunModel):
    id: str
    conversationId: str
    userId: str
    text: str
    date: int

class SystemMessage(SpeedrunModel):
    id: str
    userId: str
    text: str
    date: int
    read: bool

class ForumReadStatus(SpeedrunModel):
    forumId: str
    date: int

class Notification(SpeedrunModel):
    id: str
    date: int
    title: str
    path: str
    read: bool

class GameFollower(SpeedrunModel):
    gameId: str
    followerId: str
    pos: Optional[int] = None
    accessCount: int
    lastAccessDate: int

class GameRunner(SpeedrunModel):
    gameId: str
    userId: str
    runCount: int

class UserFollower(SpeedrunModel):
    userId: str
    followerId: str

class Session(SpeedrunModel):
    signedIn: bool
    showAds: bool
    user: Optional[User] = None
    theme: Optional[Theme] = None
    powerLevel: SitePowerLevel
    dateFormat: DateFormat
    timeFormat: TimeFormat
    timeReference: TimeReference
    timeUnits: TimeDisplayUnits
    homepageStream: HomepageStreamType
    disableThemes: bool
    csrfToken: str
    networkToken: Optional[str] = None
    gameList: list[Game]
    gameFollowerList: list[GameFollower]
    gameModeratorList: list[GameModerator]
    gameRunnerList: list[GameRunner]
    seriesList: list[Series]
    seriesModeratorList: list[SeriesModerator]
    boostAvailableTokens: Optional[int] = None
    boostNextTokenDate: int
    boostNextTokenAmount: int
    userFollowerList: list[UserFollower]
    enabledExperimentIds: list[str]  # TODO: check
    challengeModeratorList: list[ChallengeModerator]  # TODO: check

class ThemeSettings(SpeedrunModel):
    primaryColor: str
    panelColor: str
    panelOpacity: int  # TODO: may be an enum of every 5 between 70 and 100
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
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class ThreadReadStatus(SpeedrunModel):
    threadId: str
    date: int

class Ticket(SpeedrunModel):
    id: str
    queue: TicketQueueType
    type: TicketType
    status: TicketStatus
    requestorId: str
    dateSubmitted: int
    dateResolved: Optional[int] = None
    metadata: str
    """This is a json object that may be dependent on type"""

class TicketNote(SpeedrunModel):
    id: str
    ticketId: str
    readerId: str
    dateSubmitted: int
    note: str
    isMessage: bool
    isRead: bool

class UserCount(SpeedrunModel):
    userId: str
    count: int

class UserBlock(SpeedrunModel):
    blockerId: str
    blockeeId: str

class NotificationSetting(SpeedrunModel):
    type: int  # enum
    gameId: Optional[str] = None
    site: bool
    email: bool

"""A different type of notification are returned by `GetStaticData` than in other areas."""
class NotificationSettingStaticData(SpeedrunModel):
    id: int
    group: str
    title: str
    pos: int
    gameSpecific: bool
    siteDefault: int
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
    color2Id: Optional[str] = None
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
    latestMaxFollowed: int
    latestMinFollowed: int
    latestTimeFollowed: int
    showMiscByDefault: bool
    showOnStreamsPage: bool
    showUnofficialGameTypes: bool
    homepageStream: HomepageStreamType
    disableMessages: bool
    showAds: bool
    pronouns: list[str]
    nameChangeDate: Optional[int] = None
    runCommentsDisabled: bool
    followedGamesDisabled: bool
    supporterEndDate: int
    boostEndDate: int
    supporterIconType: IconType
    supporterIconPosition: IconPosition
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class SupporterCredit(SpeedrunModel):
    id: str
    userId: str
    providerId: int  # enum
    createdAt: int
    updatedAt: int
    creditType: int  # enum
    amount: int
    currency: str
    receivedAt: int
    subscriptionId: str
    periodStartsAt: int
    periodEndsAt: int
    providerItemId: str

class SupporterCode(SpeedrunModel):
    id: str
    code: str
    description: str
    duration: int
    userId: str
    createdAt: int
    updatedAt: int

class SupporterSubscription(SpeedrunModel):
    id: str
    userId: str
    providerId: int  # enum
    createdAt: int
    updatedAt: int
    expiresAt: int
    planId: int  # enum
    nextPeriodPlanId: int  # enum
    status: int  # enum
    trialEndsAt: int
    """Default 0, undocumented but assume timestamp otherwise"""
    cancelAtPeriodEnd: bool
    canceledAt: int  # TODO assume timestamp
    
class Title(SpeedrunModel):
    """User reward for completing a Challenge."""
    id: str
    title: str
    comment: str
    referenceUrl: str
