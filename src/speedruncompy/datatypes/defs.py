from ._impl import Datatype, OptField
from .enums import *

class StaticAsset(Datatype):

    assetType: str
    path: str

class StaticAssetUpdate(Datatype):
    
    assetType: str
    updateContent: str
    """Example: data:image/png;base64,examplebase64data``"""
    deleteContent: OptField[bool]

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

    def __init__(self, template: dict | tuple | float | int | None = None) -> None:
        if isinstance(template, (float, int)):
            self.hour = int(template // 3600)
            self.minute = int((template // 60) % 60)
            self.second = int(template % 60)
            self.millisecond = int((template * 1000) % 1)
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

class CommentableProperties(Datatype):
    disabled: bool
    locked: bool

class Commentable(Datatype):
    itemType: ItemType
    itemId: str
    properties: CommentableProperties
    permissions: CommentPermissions
    """Permissions of the logged in user.
    If not logged in, canPost will always be False."""


class Comment(Datatype):
    id: str
    itemType: ItemType
    itemId: str
    date: int
    userId: str
    text: OptField[str]
    """May be omitted on deleted comments."""
    parentId: OptField[str]
    deleted: bool
    deletedUserId: OptField[str]

class Like(Datatype):
    itemType: ItemType
    itemId: str
    userId: str
    date: int

class Forum(Datatype):
    id: str
    name: str
    url: str
    description: OptField[str]
    type: ForumType
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
    created: int
    lastCommentId: str
    lastCommentUserId: str
    lastCommentDate: int
    sticky: bool
    locked: bool

class RunSettings(Datatype):

    runId: OptField[str]
    """Omitted when submitting a new run."""
    gameId: str
    categoryId: str
    playerNames: list[str]
    time: OptField[RuntimeTuple]  # Note: whichever timing method is primary to the game is required
    """LRT if it is enabled, otherwise RTA."""
    timeWithLoads: OptField[RuntimeTuple]
    """RTA if LRT is enabled."""
    igt: OptField[RuntimeTuple]
    platformId: str
    emulator: bool
    video: str
    comment: str
    date: int
    values: list[VarValue]  # type:ignore
    
    # TODO: this only guarantees RTA if both time and timeWithLoads is present in the run,
    # but if a LRT run is missing RTA then it will incorrectly return `time` rather than `None`
    # Correctly doing this would require knowledge of the Game data, so with cacheing or autoreqs.
    def _get_rta(self): return self.timeWithLoads if "timeWithLoads" in self else self.time
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
    type: str  # enum? is this true? afaict is always "game"
    loadtimes: bool
    milliseconds: bool
    igt: bool
    verification: bool
    autoVerify: OptField[bool]  # Why is this OptField????? I hate SRC
    requireVideo: bool
    emulator: EmulatorType
    defaultTimer: TimerName
    validTimers: list[TimerName]
    releaseDate: OptField[int]
    addedDate: int
    touchDate: int
    baseGameId: OptField[str]
    coverPath: str
    trophy1stPath: OptField[str]
    trophy2ndPath: OptField[str]
    trophy3rdPath: OptField[str]
    trophy4thPath: OptField[str]
    runCommentsMode: PermissionType
    runCount: int
    activePlayerCount: int
    totalPlayerCount: int
    boostReceivedCount: int
    boostDistinctDonorsCount: int
    rules: OptField[str]
    viewPowerLevel: SitePowerLevel
    platformIds: list[str]
    regionIds: list[str]
    gameTypeIds: list[GameType]
    websiteUrl: OptField[str]
    discordUrl: OptField[str]
    defaultView: DefaultViewType
    guidePermissionType: PermissionType
    resourcePermissionType: PermissionType
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
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
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
    categoryScope: VarCategoryScope
    categoryId: OptField[str]
    levelScope: VarLevelScope
    levelId: OptField[str]
    isMandatory: bool
    isSubcategory: bool
    isUserDefined: bool
    isObsoleting: bool
    defaultValue: OptField[str]
    archived: bool
    displayMode: OptField[VarDisplayMode]

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
    publishTarget: str
    publishTags: list[str]
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
    body: OptField[str]
    """Omitted for all but the first item in `r_GetGameSummary.newsList[]`"""
    dateSubmitted: int

class Player(Datatype):
    """Fields from `User` present in `playerLists`. May also be an unregistered player, use property `_is_registered`"""
    id: str
    name: str
    url: OptField[str]
    powerLevel: OptField[SitePowerLevel]
    color1Id: OptField[str]
    color2Id: OptField[str]
    """OptField even on full `player`"""
    colorAnimate: OptField[int]
    areaId: OptField[str]
    isSupporter: OptField[bool]
    """OptField even on full `player`"""

    def _is_user(self): return not self.id.startswith("u-")
    # NOTE: `minimal regex: u-[a-f0-9]{8}-?[a-f0-9]{4}-?5[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}`
    _is_registered = property(fget=_is_user)
    """Checks if a player has an account or is a text label"""

class AvatarDecoration(Datatype):
    """Supporter feature for rings around names.
    
    @separateColors: If true, see this object's color Ids. If either is absent, inherit from username.
    """
    enabled: bool
    separateColors: OptField[bool]
    color1Id: OptField[str]
    """Defaults to username's color1Id"""
    color2Id: OptField[str]
    """Defaults to username's color2Id"""

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
    isSupporter: OptField[bool]
    avatarDecoration: OptField[AvatarDecoration]
    iconType: IconType
    onlineDate: int
    signupDate: int
    touchDate: int
    staticAssets: list[StaticAsset]
    supporterIconType: OptField[IconType]
    supporterIconPosition: OptField[IconPosition]
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
    runVideosAtRisk: int

class UserSocialConnection(Datatype):
    userId: str
    networkId: NetworkId
    value: str
    verified: bool

class UserModerationStats(Datatype):
    gameId: str
    level: GamePowerLevel
    totalRuns: int
    totalTime: int
    minDate: int
    maxDate: int

class UserGameFollow(Datatype):
    gameId: str
    accessCount: int
    lastAccessDate: int

class UserGameRunnerStats(Datatype):
    gameId: str
    totalRuns: int
    totalTime: int
    uniqueLevels: int
    uniqueCategories: int
    minDate: int
    maxDate: int

class GameOrderGroup(Datatype):
    id: str
    name: str
    sortType: GameSortType
    gameIds: list[str]
    open: OptField[bool]
    editing: OptField[bool]

class GameOrdering(Datatype):
    defaultGroups: list[GameOrderGroup]
    supporterGroups: list[GameOrderGroup]

class UserProfile(Datatype):  # TODO: check where this exists (if anywhere?)

    userId: str
    bio: OptField[str]
    signupDate: int
    defaultView: DefaultViewType
    showMiscByDefault: bool
    gameOrdering: GameOrdering
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]

class UserReducedProfile(Datatype):
    """UserProfile as returned by GetUserLeaderboard, GetUserSummary & GetUserPopoverData.
    
    Missing userStats and userSocialConnectionList."""
    userId: str
    bio: OptField[str]
    signupDate: int
    defaultView: DefaultViewType
    showMiscByDefault: bool
    gameOrdering: OptField[GameOrdering]

class SeriesModerator(Datatype):
    seriesId: str
    userId: str
    level: GamePowerLevel

class GameModerator(Datatype):
    gameId: str
    userId: str
    level: GamePowerLevel

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

class SocialNetwork(Datatype):
    id: NetworkId
    name: str
    major: bool
    pos: int
    pattern: str

class Area(Datatype):
    id: str
    name: str
    fullName: str
    label: str
    flagIcon: str
    lbFlagIcon: str
    lbName: str

class Color(Datatype):
    id: str
    name: str
    darkColor: str
    """Deprecated, darkColor is always used on the site"""
    lightColor: str
    """Deprecated, colors now seem to be sorted by their name's ascending alphabetical order (A-Z)"""
    pos: int

class GameTypeObj(Datatype):
    id: GameType
    name: str
    url: str
    description: str
    allowBaseGame: bool

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
    verified: Verified
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
    estimated: OptField[bool]
    """Only shown in GetModerationRuns"""
    issues: OptField[list[str] | None]
    videoState: VideoState

class ChallengeStanding(Datatype):
    challengeId: str
    place: int
    registeredPlayerIds: list[str]
    prizeAmount: int
    unregisteredPlayers: list[str]  # TODO: str is an assumption
    prizeCurrency: str

class ChallengePrize(Datatype):
    place: int
    amount: int

class ChallengePrizeConfig(Datatype):
    prizePool: int
    currency: str
    prizes: list[ChallengePrize]

class GlobalChallengeRanking(Datatype):
    """Sitewide rank based on all challenges entered."""
    userId: str
    rank: int
    totalEarnings: int
    firstPlaces: int
    secondPlaces: int
    thirdPlaces: int
    challengesEntered: int

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
    state: ChallengeState
    description: str
    rules: str
    numPlayers: int
    exactPlayers: bool
    playerMatchMode: PlayerMatchMode
    timeDirection: TimeDirection
    enforceMs: bool
    coverImagePath: str
    contest: bool
    contestRules: str
    runCommentsMode: PermissionType
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
    issues: OptField[None]  # TODO: Find if this is ever Not None
    playerIds: list[str]
    commentsCount: int
    place: OptField[int]
    obsolete: OptField[bool]
    videoState: VideoState

class Theme(Datatype):
    id: str
    url: str
    name: OptField[str]  # TODO: check optional
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
    values: list[Value]  # type:ignore
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
    type: ResourceType
    name: str
    description: str
    date: int
    userId: str
    gameId: str
    path: OptField[str]
    link: OptField[str]
    fileName: OptField[str]
    authorNames: str  # TODO: exhaustive check for lists

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
    """If the stream has a PB on SRC (and has their account linked)"""  # TODO: check

class GameSettings(Datatype):
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

class SeriesSettings(Datatype):
    name: str
    url: str
    discordUrl: str
    websiteUrl: str
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class GameModerationStats(Datatype):
    gameId: str
    state: int  # enum? appears to always be 0
    count: int
    minDate: OptField[int]
    maxDate: OptField[int]

class AuditLogEntry(Datatype):
    id: str
    date: int
    eventType: str  # EventType
    actorId: str
    gameId: str
    context: str
    """A json dict of extra context based on eventType."""
    userId: OptField[str]

class Conversation(Datatype):
    id: str
    participantUserIds: list[str]
    lastMessageId: str
    lastMessageUser: str
    lastMessageText: str
    lastMessageDate: int
    readDate: int

class ConversationLightweight(Datatype):
    id: str
    participantUserIds: list[str]  # TODO: May always be empty?
    lastMessageId: str
    lastMessageDate: int

class ConversationParticipant(Datatype):
    conversationId: str
    userId: str
    joinedDate: int
    leftDate: int  # TODO: OptField?

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
    dateFormat: DateFormat
    timeFormat: TimeFormat
    timeReference: TimeReference
    timeUnits: TimeDisplayUnits
    homepageStream: HomepageStreamType
    disableThemes: bool
    csrfToken: str
    networkToken: OptField[str]
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
    enabledExperimentIds: list[str]  # TODO: check
    challengeModeratorList: list[ChallengeModerator]  # TODO: check

class ThemeSettings(Datatype):
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

class ThreadReadStatus(Datatype):
    threadId: str
    date: int

class Ticket(Datatype):
    id: str
    queue: TicketQueueType
    type: TicketType
    status: TicketStatus
    requestorId: str
    dateSubmitted: int
    dateResolved: OptField[int]
    metadata: str
    """This is a json object that may be dependent on type"""

class TicketNote(Datatype):
    id: str
    ticketId: str
    readerId: str
    dateSubmitted: int
    note: str
    isMessage: bool
    isRead: bool

class UserCount(Datatype):
    userId: str
    count: int

class UserBlock(Datatype):
    blockerId: str
    blockeeId: str

class NotificationSetting(Datatype):
    type: int  # enum
    gameId: OptField[str]
    site: bool
    email: bool

"""A different type of notification are returned by `GetStaticData` than in other areas."""
class NotificationSettingStaticData(Datatype):
    id: int
    group: str
    title: str
    pos: int
    gameSpecific: bool
    siteDefault: int
    emailDefault: bool

class UserSettings(Datatype):
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
    color2Id: OptField[str]
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
    nameChangeDate: OptField[int]
    runCommentsDisabled: bool
    followedGamesDisabled: bool
    supporterEndDate: int
    boostEndDate: int
    supporterIconType: IconType
    supporterIconPosition: IconPosition
    staticAssets: list[StaticAsset]
    staticAssetUpdates: list[StaticAssetUpdate]

class SupporterCredit(Datatype):
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

class SupporterCode(Datatype):
    id: str
    code: str
    description: str
    duration: int
    userId: str
    createdAt: int
    updatedAt: int

class SupporterSubscription(Datatype):
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
    
class Title(Datatype):
    """User reward for completing a Challenge."""
    id: str
    title: str
    comment: str
    referenceUrl: str
