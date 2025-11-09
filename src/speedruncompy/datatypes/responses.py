from types import NoneType
from typing import Any

from pydantic import PrivateAttr
from bidict import frozenbidict

from .defs import *
from ._impl import SpeedrunModel


class r_Empty(SpeedrunModel):
    """No Content"""

class r_Ok(SpeedrunModel):
    """Response only including `ok`."""
    ok: bool

    def __bool__(self): return self.ok


"""GET responses"""


class r_GetArticle(SpeedrunModel):
    article: Article
    relatedArticleList: list[Article]
    gameList: list[Game]
    userList: list[User]

class r_GetArticleList(SpeedrunModel):
    articleList: list[Article]
    pagination: Pagination
    gameList: list[Game]
    userList: list[User]
    
    _articleDict: dict[str, Article]
    _gameDict: dict[str, Game]
    _userDict: dict[str, User]
    
    __condenser_map__ = frozenbidict({
        "articleList": "_articleDict",
        "gameList": "_gameDict",
        "userList": "_userDict"
    })

class r_GetChallenge(SpeedrunModel):
    challenge: Challenge
    game: Game
    moderatorList: list[ChallengeModerator]
    standingList: list[ChallengeStanding]
    theme: Theme
    userList: list[User]
    challengeRunCount: int
    gameFollowerCount: int
    titleList: list[Title]
    platformList: list[Platform]

class r_GetChallengeLeaderboard(SpeedrunModel):
    challengeRunList: list[ChallengeRun]
    playerList: list[Player]
    userList: list[User]
    platformList: list[Platform]
    pagination: Pagination
    
    _challengeRunDict: dict[str, ChallengeRun]
    _playerDict: dict[str, Player]
    _userDict: dict[str, User]
    _platformDict: dict[str, Platform]
    
    __condenser_map__ = frozenbidict({
        "challengeRunList": "_challengeRunDict",
        "playerList": "_playerDict",
        "userList": "_userDict",
        "platformList": "_platformDict",
    })

class r_GetChallengeRun(SpeedrunModel):
    challenge: Challenge
    challengeRun: ChallengeRun
    game: Game
    playerList: list[Player]
    userList: list[User]
    platformList: list[Platform]

class r_GetChallengeGlobalRankingList(SpeedrunModel):
    rankingList: list[GlobalChallengeRanking]
    userList: list[User]

class r_GetCommentList(SpeedrunModel):
    commentable: Commentable
    commentList: list[Comment]
    likeList: list[Like]
    userList: list[User]
    pagination: Pagination
    
    _commentDict: dict[str, Comment]
    _likeDict: dict[str, Like]
    _userDict: dict[str, User]
    
    __condenser_map__ = frozenbidict({
        "commentList": "_commentDict",
        "likeList": "_likeDict",
        "userList": "_userDict",
    })

class r_GetForumList(SpeedrunModel):
    forumList: list[Forum]
    gameList: list[Game]
    userList: list[User]

class r_GetStaticData(SpeedrunModel):
    areas: list[Area]
    colors: list[Color]
    gameTypeList: list[GameTypeObj]
    notificationSettings: list[NotificationSettingStaticData]
    regionList: list[Region]
    socialNetworkList: list[SocialNetwork]
    supporterPlanList: Optional[list[Any] | None] = None  # Unknown type

class r_GetGameData(SpeedrunModel):
    game: Game
    categories: list[Category]
    levels: list[Level]
    moderators: list[GameModerator]
    platforms: list[Platform]
    regions: list[Region]
    theme: Optional[Theme] = None
    users: list[User]
    values: list[Value]  # type:ignore
    variables: list[Variable]

class r_GetGameLeaderboard(SpeedrunModel):
    leaderboard: Leaderboard  # not funny. didn't laugh

class r_GetGameLeaderboard2(SpeedrunModel):
    """_summary_

    Args:
        SpeedrunModel (r_GetGameLeaderboard2): _description_
    """
    runList: list[Run]
    playerList: list[Player]
    platformList: list[Platform]
    pagination: Pagination
    
    _runDict: dict[str, Run] = PrivateAttr()
    _playerDict: dict[str, Player] = PrivateAttr()
    _platformDict: dict[str, Platform] = PrivateAttr()
    
    __condenser_map__ = frozenbidict({
        "runList": "_runDict",
        "playerList": "_playerDict",
        "platformList": "_platformDict"
    })

class r_GetGameLevelSummary(SpeedrunModel):
    category: Category
    runList: list[Run]
    playerList: list[Player]

class r_GetGameList(SpeedrunModel):
    gameList: list[Game]
    platformList: list[Platform]
    pagination: Pagination
    
    _gameDict: dict[str, Game]
    _platformDict: dict[str, Platform]
    
    __condenser_map__ = frozenbidict({
        "gameList": "_gameDict",
        "platformList": "_platformDict",
    })

class r_GetGameRecordHistory(SpeedrunModel):
    playerList: list[Player]
    runList: list[Run]

class r_GetGameSummary(SpeedrunModel):
    game: Game
    gameBoosts: list[GameBoost]
    gameModerators: list[GameModerator]
    forum: Forum
    newsList: list[News]
    gameStats: list[GameStats]
    stats: GameStats
    relatedGames: list[Game]
    seriesList: list[Series]
    platformList: list[Platform]
    theme: Theme
    threadList: list[Thread]
    users: list[User]
    challengeList: list[Challenge]
    challengeCount: int
    guideCount: int
    levelCount: int
    newsCount: int
    relatedCount: int
    resourceCount: int
    streamCount: int
    threadCount: int

class r_GetGuide(SpeedrunModel):
    guide: Guide
    users: list[User]

class r_GetGuideList(SpeedrunModel):
    guideList: list[Guide]
    users: list[User]

class r_GetHomeSummary(SpeedrunModel):
    stream: Optional[Stream] = None

class r_GetLatestLeaderboard(SpeedrunModel):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]  # type:ignore
    variables: list[Variable]
    platforms: list[Platform]

class r_GetNews(SpeedrunModel):
    news: News
    users: list[User]

class r_GetNewsList(SpeedrunModel):
    newsList: list[News]
    users: list[User]

class r_GetResourceList(SpeedrunModel):
    resourceList: list[Resource]
    users: list[User]

class r_GetRun(SpeedrunModel):
    game: Game
    category: Category
    level: Optional[Level] = None
    platform: Optional[Platform] = None
    players: list[Player]
    region: Optional[Region] = None
    run: Run
    users: list[User]
    values: list[Value]  # type:ignore
    variables: list[Variable]

class r_GetSearch(SpeedrunModel):
    gameList: list[Game]
    newsList: list[News]
    pageList: list[Article]
    seriesList: list[Series]
    userList: list[User]
    challengeList: list[Challenge]
    platformList: list[Platform]

class r_GetSeriesList(SpeedrunModel):
    seriesList: list[Series]
    pagination: Pagination
    
    _seriesDict: dict[str, Series]
    
    __condenser_map__ = frozenbidict({
        "seriesList": "_seriesDict",
    })

class r_GetSeriesSummary(SpeedrunModel):
    series: Series
    forum: Forum
    gameList: list[Game]
    moderatorList: list[SeriesModerator]
    theme: Theme
    threadList: list[Thread]
    userList: list[User]
    gameCount: int
    streamCount: int
    threadCount: int

class r_GetStreamList(SpeedrunModel):
    gameList: list[Game]
    streamList: list[Stream]
    userList: list[User]
    pagination: Pagination

class r_GetThread(SpeedrunModel):
    thread: Thread
    commentList: list[Comment]
    userList: list[User]
    likeList: list[Like]
    pagination: Pagination
    
    _commentDict: dict[str, Comment]
    _userDict: dict[str, User]
    _likeDict: dict[str, Like]
    
    __condenser_map__ = frozenbidict({
        "commentList": "_commentDict",
        "userList": "_userDict",
        "likeList": "_likeDict",
    })

class r_GetThreadList(SpeedrunModel):
    threadList: list[Thread]
    pagination: Pagination
    users: list[User]

class r_GetUserLeaderboard(SpeedrunModel):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    platforms: list[Platform]
    regions: list[Region]
    runs: list[Run]
    user: User
    userProfile: UserReducedProfile
    users: list[User]
    """Always empty"""
    players: list[Player]
    values: list[Value]  # type:ignore
    variables: list[Variable]
    followedGameIds: NoneType
    """Unused null key"""
    challengeList: list[Challenge]
    challengeRunList: list[ChallengeRun]

class r_GetUserSummary(SpeedrunModel):
    user: User
    userProfile: UserReducedProfile
    userStats: UserStats
    userGameFollowerStats: list[UserGameFollow]
    """Empty list if the user has set game follows to private."""
    userGameModeratorStats: list[UserModerationStats]
    userGameRunnerStats: list[UserGameRunnerStats]
    userSocialConnectionList: list[UserSocialConnection]
    games: list[Game]
    theme: Theme
    titleList: list[Title]

class r_GetUserComments(SpeedrunModel):
    articleList: list[Article]
    commentList: list[Comment]
    forumList: list[Forum]
    gameList: list[Game]
    likeList: list[Like]
    newsList: list[News]
    runList: list[Run]
    threadList: list[Thread]
    userList: list[User]
    pagination: Pagination
    
    _articleDict: dict[str, Article]
    _commentDict: dict[str, Comment]
    _forumDict: dict[str, Forum]
    _gameDict: dict[str, Game]
    _likeDict: dict[str, Like]
    _newsDict: dict[str, News]
    _runDict: dict[str, Run]
    _threadDict: dict[str, Thread]
    _userDict: dict[str, User]
    
    __condenser_map__ = frozenbidict({
        "articleList": "_articleDict",
        "commentList": "_commentDict",
        "forumList": "_forumDict",
        "gameList": "_gameDict",
        "likeList": "_likeDict",
        "newsList": "_newsDict",
        "runList": "_runDict",
        "threadList": "_threadDict",
        "userList": "_userDict",
    })

class r_GetUserPopoverData(SpeedrunModel):
    user: User
    userProfile: UserReducedProfile
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]
    games: list[Game]
    """Contains games sometimes:tm:"""
    titleList: list[Title]

class r_GetTitleList(SpeedrunModel):
    titleList: list[Title]

class r_GetTitle(SpeedrunModel):
    title: Title


"""POST responses"""


class r_GetAuditLogList(SpeedrunModel):
    auditLogList: list[AuditLogEntry]
    userList: list[User]
    gameList: list[Game]
    categoryList: list[Category]
    levelList: list[Level] | None
    """WARN: is None when empty rather than []."""
    variableList: list[Variable]
    valueList: list[Value]
    runList: list[Run]
    pagination: Pagination
    
    _auditLogDict: dict[str, AuditLogEntry]
    _userDict: dict[str, User]
    _gameDict: dict[str, Game]
    _categoryDict: dict[str, Category]
    _levelDict: dict[str, Level]
    _variableDict: dict[str, Variable]
    _valueDict: dict[str, Value]
    _runDict: dict[str, Run]
    
    __condenser_map__ = frozenbidict({
        "auditLogList": "_auditLogDict",
        "userList": "_userDict",
        "gameList": "_gameDict",
        "categoryList": "_categoryDict",
        "levelList": "_levelDict",
        "variableList": "_variableDict",
        "valueList": "_valueDict",
        "runList": "_runDict",
    })

class r_GetCommentable(SpeedrunModel):
    commentable: Commentable

class r_GetConversationMessages(SpeedrunModel):
    conversation: Conversation
    participants: list[ConversationParticipant]
    messages: list[ConversationMessage]
    users: list[User]
    userBlocks: list[UserBlock]

class r_GetConversations(SpeedrunModel):
    conversations: list[Conversation]
    participants: list[ConversationParticipant]
    users: list[User]
    systemMessages: list[SystemMessage]

class r_GetForumReadStatus(SpeedrunModel):
    forumReadStatusList: list[ForumReadStatus]

class r_GetGameSettings(SpeedrunModel):
    settings: GameSettings
    moderatorList: list[GameModerator]
    theme: Theme
    gameList: list[Game]
    userList: list[User]

class r_GetModerationGames(SpeedrunModel):
    games: list[Game] | None
    """Is null when not logged in."""
    gameModerationStats: list[GameModerationStats] | None
    """Is null when not logged in."""

class r_GetModerationRuns(SpeedrunModel):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    pagination: Pagination
    platforms: list[Platform]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]  # type:ignore
    variables: list[Variable]
    users: list[User]
    
    _categoryDict: dict[str, Category]
    _gameDict: dict[str, Game]
    _levelDict: dict[str, Level]
    _platformDict: dict[str, Platform]
    _playerDict: dict[str, Player]
    _regionDict: dict[str, Region]
    _runDict: dict[str, Run]
    _variableDict: dict[str, Variable]
    _valueDict: dict[str, Value]
    _userDict: dict[str, User]
    
    __condenser_map__ = frozenbidict({
        "categories": "_categoryDict",
        "games": "_gameDict",
        "levels": "_levelDict",
        "platforms": "_platformDict",
        "players": "_playerDict",
        "regions": "_regionDict",
        "runs": "_runDict",
        "variables": "_variableDict",
        "values": "_valueDict",
        "users": "_userDict",
    })

class r_GetNotifications(SpeedrunModel):
    unreadCount: int
    notifications: list[Notification]
    pagination: Pagination
    
    _notificationDict: dict[str, Notification]
    
    __condenser_map__ = frozenbidict({
        "notifications": "_notificationDict",
    })

class r_GetRunSettings(SpeedrunModel):
    settings: RunSettings
    users: list[User]

class r_GetSeriesSettings(SpeedrunModel):
    settings: SeriesSettings
    moderatorList: list[SeriesModerator]
    gameList: list[Game]
    theme: Theme
    userList: list[User]

class r_GetSession(SpeedrunModel):
    session: Session

class r_GetThemeSettings(SpeedrunModel):
    """NB: if no theme is set then this response will be empty"""
    settings: Optional[ThemeSettings] = None
    theme: Optional[Theme] = None

class r_GetThreadReadStatus(SpeedrunModel):
    threadReadStatusList: list[ThreadReadStatus]

class r_GetTickets(SpeedrunModel):
    ticketList: list[Ticket]
    ticketNoteList: list[TicketNote]
    """Admins can see all notes, users can see messages here."""
    pagination: Pagination
    userList: list[User]
    gameList: list[Game]
    userModCountList: list[UserCount]
    userRunCountList: list[UserCount]
    
    _ticketDict: dict[str, Ticket]
    _ticketNoteDict: dict[str, TicketNote]
    _userDict: dict[str, User]
    _gameDict: dict[str, Game]
    _userModCountDict: dict[str, UserCount]
    _userRunCountDict: dict[str, UserCount]
    
    __condenser_map__ = frozenbidict(({
        "ticketList": "_ticketDict",
        "ticketNoteList": "_ticketNoteDict",
        "userList": "_userDict",
        "gameList": "_gameDict",
        "userModCountList": "_userModCountDict",
        "userRunCountList": "_userRunCountDict",
    }))
    
    __condenser_overrides__ = {
        "userModCountList": "userId",
        "userRunCountList": "userId",
    }

class r_GetUserBlocks(SpeedrunModel):
    userBlocks: list[UserBlock]

class r_GetUserSettings(SpeedrunModel):
    settings: UserSettings
    gameFollowerList: list[GameFollower]
    gameModeratorList: list[GameModerator]
    notificationSettings: list[NotificationSetting]
    userSocialConnectionList: list[UserSocialConnection]
    gameList: list[Game]
    themeList: list[Theme]
    titleList: list[Title]
    supporterCreditList: list[SupporterCredit]
    supporterCodeList: list[SupporterCode]
    supporterSubscription: Optional[SupporterSubscription] = None
    experimentList: Any
    enabledExperimentIds: Any

class r_GetUserSupporterData(SpeedrunModel):
    supporterEndDate: int
    boostEndDate: int

class r_PutUserSupporterNewSubscription(SpeedrunModel):
    subscription: SupporterSubscription
    paymentIntentClientSecret: str

class r_PutAuthLogin(SpeedrunModel):
    loggedIn: bool
    tokenChallengeSent: Optional[bool] = None

class r_PutAuthSignup(SpeedrunModel):
    loggedIn: bool
    tokenChallengeSent: Optional[bool] = None

class r_PutConversation(SpeedrunModel):
    ok: bool
    conversationId: str
    messageId: str

class r_PutConversationMessage(SpeedrunModel):
    ok: bool
    conversationId: str
    messageId: str

class r_PutGame(SpeedrunModel):
    game: Game

class r_PutRunSettings(SpeedrunModel):
    runId: str

class r_PutThread(SpeedrunModel):
    thread: Thread

class r_PutLike(SpeedrunModel):
    likeList: list[Like]
    userList: list[User]

class r_PutTicket(SpeedrunModel):
    ticketId: str

class r_PutUserSettings(SpeedrunModel):
    settings: UserSettings

class r_GetUserApiKey(SpeedrunModel):
    apiKey: str

class r_GetUserGameBoostData(SpeedrunModel):
    boostAvailableTokens: int
    boostDistinctGamesCount: int
    boostDistinctUsersCount: int
    boostEndDate: int
    boostGiftedCount: int
    boostLastTokenDate: int
    boostNextTokenAmount: int
    boostNextTokenDate: int
    boostReceivedCount: int
    gameBoostList: list[GameBoost]
    gameList: list[Game]
    isBoosted: bool
    userList: list[User]

class r_GetUserDataExport(SpeedrunModel):
    articleList: list[Article]
    commentList: list[Comment]
    conversationList: list[ConversationLightweight]
    gameFollowerList: list[GameFollower]
    guideList: list[Guide]
    likeList: list[Like]
    messageList: list[ConversationMessage]
    newsList: list[News]
    resourceList: list[Resource]
    runList: list[Run]
    threadList: list[Thread]
    ticketList: list[Ticket]
    ticketNoteList: list[TicketNote]
    user: User
    userFollowerList: list[UserFollower]
    userSettings: UserSettings
    userSocialConnectionList: list[UserSocialConnection]

class r_PutUserUpdateEmail(SpeedrunModel):
    emailChanged: bool
    tokenChallengeSent: bool
