from .datatypes import *
from typing import Any

class r_Empty(Datatype):
    """No Content"""

class r_Ok(Datatype):
    """Response only including `ok`."""
    ok: bool

    def __bool__(self): return self.ok


"""GET responses"""


class r_GetArticle(Datatype):
    article: Article
    relatedArticleList: list[Article]
    gameList: list[Game]
    userList: list[User]

class r_GetArticleList(Datatype):
    articleList: list[Article]
    pagination: Pagination
    gameList: list[Game]
    userList: list[User]

class r_GetChallenge(Datatype):
    challenge: Challenge
    game: Game
    moderatorList: list[ChallengeModerator]
    standingList: list[ChallengeStanding]
    theme: Theme
    userList: list[User]
    challengeRunCount: int
    gameFollowerCount: int
    titleList: list[Title]

class r_GetChallengeLeaderboard(Datatype):
    challengeRunList: list[ChallengeRun]
    playerList: list[Player]
    userList: list[User]
    pagination: Pagination

class r_GetChallengeRun(Datatype):
    challenge: Challenge
    challengeRun: ChallengeRun
    game: Game
    playerList: list[Player]
    userList: list[User]

class r_GetChallengeGlobalRankingList(Datatype):
    rankingList: list[GlobalChallengeRanking]
    userList: list[User]

class r_GetCommentList(Datatype):
    commentable: Commentable
    commentList: list[Comment]
    likeList: list[Like]
    userList: list[User]
    pagination: Pagination

class r_GetForumList(Datatype):
    forumList: list[Forum]
    gameList: list[Game]
    userList: list[User]

class r_GetGameData(Datatype):
    game: Game
    categories: list[Category]
    levels: list[Level]
    moderators: list[GameModerator]
    platforms: list[Platform]
    regions: list[Region]
    runCounts: list[RunCount]
    theme: OptField[Theme]
    users: list[User]
    values: list[Value]
    variables: list[Variable]

class r_GetGameLeaderboard(Datatype):
    leaderboard: Leaderboard  # not funny. didn't laugh

class r_GetGameLeaderboard2(Datatype):
    runList: list[Run]
    playerList: list[Player]
    pagination: Pagination

class r_GetGameLevelSummary(Datatype):
    category: Category
    runList: list[Run]
    playerList: list[Player]

class r_GetGameList(Datatype):
    gameList: list[Game]
    pagination: Pagination

class r_GetGameRecordHistory(Datatype):
    playerList: list[Player]
    runList: list[Run]

class r_GetGameSummary(Datatype):
    game: Game
    gameBoosts: list[GameBoost]
    gameModerators: list[GameModerator]
    forum: Forum
    newsList: list[News]
    gameStats: list[GameStats]
    stats: GameStats
    relatedGames: list[Game]
    seriesList: list[Series]
    theme: Theme
    threadList: list[Thread]
    users: list[User]
    challengeList: list[Challenge]  # TODO: Check (Any)
    challengeCount: int
    guideCount: int
    levelCount: int
    newsCount: int
    relatedCount: int
    resourceCount: int
    streamCount: int
    threadCount: int

class r_GetGuide(Datatype):
    guide: Guide
    users: list[User]

class r_GetGuideList(Datatype):
    guideList: list[Guide]
    users: list[User]

class r_GetHomeSummary(Datatype):
    stream: OptField[Stream]

class r_GetLatestLeaderboard(Datatype):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]
    variables: list[Variable]
    platforms: list[Platform]

class r_GetNews(Datatype):
    news: News
    users: list[User]

class r_GetNewsList(Datatype):
    newsList: list[News]
    users: list[User]

class r_GetResourceList(Datatype):
    resourceList: list[Resource]
    users: list[User]

class r_GetRun(Datatype):
    game: Game
    category: Category
    level: OptField[Level]
    platform: OptField[Platform]
    players: list[Player]
    region: OptField[Region]
    run: Run
    users: list[User]
    values: list[Value]
    variables: list[Variable]

class r_GetSearch(Datatype):
    gameList: list[Game]
    newsList: list[News]
    pageList: list[Article]  # TODO: check
    seriesList: list[Series]
    userList: list[User]
    challengeList: list[Challenge]

class r_GetSeriesList(Datatype):
    seriesList: list[Series]
    pagination: Pagination

class r_GetSeriesSummary(Datatype):
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

class r_GetStreamList(Datatype):
    gameList: list[Game]
    streamList: list[Stream]
    userList: list[User]
    pagination: Pagination

class r_GetThread(Datatype):
    thread: Thread
    commentList: list[Comment]
    userList: list[User]
    likeList: list[Like]
    pagination: Pagination

class r_GetThreadList(Datatype):
    threadList: list[Thread]
    pagination: Pagination
    users: list[User]

class r_GetUserLeaderboard(Datatype):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    platforms: list[Platform]
    regions: list[Region]
    runs: list[Run]
    user: User
    userProfile: UserLeaderboardProfile
    users: list[User]
    """Always empty"""
    players: list[Player]
    values: list[Value]
    variables: list[Variable]
    followedGameIds: Optional[Any]  # TODO: find if this is ever not null
    """Unused null key"""
    challengeList: list[Challenge]
    challengeRunList: list[ChallengeRun]

class r_GetUserPopoverData(Datatype):
    user: User
    userProfile: UserLeaderboardProfile
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]
    games: list[Game]
    """Contains games sometimes:tm:"""
    titleList: list[Title]

class r_GetTitleList(Datatype):
    titleList: list[Title]


"""POST responses"""


class r_GetAuditLogList(Datatype):
    auditLogList: list[AuditLogEntry]

class r_GetCommentable(Datatype):
    commentable: Commentable

class r_GetConversationMessages(Datatype):
    conversation: Conversation
    participants: list[ConversationParticipant]
    messages: list[ConversationMessage]
    users: list[User]
    userBlocks: list[UserBlock]

class r_GetConversations(Datatype):
    conversations: list[Conversation]
    participants: list[ConversationParticipant]
    users: list[User]
    systemMessages: list[SystemMessage]

class r_GetForumReadStatus(Datatype):
    forumReadStatusList: list[ForumReadStatus]

class r_GetGameSettings(Datatype):
    settings: GameSettings
    moderatorList: list[GameModerator]
    theme: Theme
    gameList: list[Game]
    userList: list[User]

class r_GetModerationGames(Datatype):
    games: list[Game]
    gameModerationStats: list[GameModerationStats]

class r_GetModerationRuns(Datatype):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    pagination: Pagination
    platforms: list[Platform]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]
    variables: list[Variable]
    users: list[User]

class r_GetNotifications(Datatype):
    unreadCount: int
    notifications: list[Notification]
    pagination: Pagination

class r_GetRunSettings(Datatype):
    settings: RunSettings
    users: list[User]

class r_GetSeriesSettings(Datatype):
    settings: SeriesSettings
    moderatorList: list[SeriesModerator]
    gameList: list[Game]
    theme: Theme
    userList: list[User]

class r_GetSession(Datatype):
    session: Session

class r_GetThemeSettings(Datatype):
    """NB: if no theme is set then this response will be empty"""
    settings: OptField[ThemeSettings]
    theme: OptField[Theme]

class r_GetThreadReadStatus(Datatype):
    threadReadStatusList: list[ThreadReadStatus]

class r_GetTickets(Datatype):
    ticketList: list[Ticket]
    ticketNoteList: list[TicketNote]
    """May only be accessible to admins"""
    pagination: Pagination
    userList: list[User]
    gameList: list[Game]
    userModCountList: list[Any]  # TODO: document
    userRunCountList: list[Any]  # TODO: document

class r_GetUserBlocks(Datatype):
    userBlocks: list[UserBlock]

class r_GetUserSettings(Datatype):
    settings: UserSettings
    gameFollowerList: list[GameFollower]
    gameModeratorList: list[GameModerator]
    notificationSettings: list[NotificationSetting]
    userSocialConnectionList: list[UserSocialConnection]
    gameList: list[Game]
    themeList: list[Theme]
    titleList: list[Title]
    supporterCreditList: list[Any]  # TODO: document
    supporterCodeList: list[Any]  # TODO: document
    supporterSubscription: OptField[Any]
    experimentList: Any
    enabledExperimentIds: Any

class r_GetUserSupporterData(Datatype):
    supporterEndDate: int
    boostEndDate: int

class r_PutAuthLogin(Datatype):
    loggedIn: bool
    tokenChallengeSent: OptField[bool]

class r_PutAuthLogout(Datatype):
    """No content"""

class r_PutAuthSignup(Datatype):
    loggedIn: bool
    tokenChallengeSent: OptField[bool]

class r_PutComment(Datatype):
    """No content"""

class r_PutCommentableSettings(Datatype):
    """No content"""

class r_PutCommentDelete(Datatype):
    """No content"""

class r_PutCommentRestore(Datatype):
    """No content"""

class r_PutConversation(Datatype):
    ok: bool
    conversationId: str
    messageId: str

class r_PutConversationMessage(Datatype):
    ok: bool
    conversationId: str
    messageId: str

class r_PutGame(Datatype):
    game: Game

class r_PutGameBoostGrant(Datatype):
    """No content"""

class r_PutGameModerator(Datatype):
    """No content"""

class r_PutGameModeratorDelete(Datatype):
    """No content"""

class r_PutGameSettings(Datatype):
    """No content"""

class r_PutRunAssignee(Datatype):
    """No content"""

class r_PutRunDelete(Datatype):
    """No content"""

class r_PutRunSettings(Datatype):
    runId: str

class r_PutRunVerification(Datatype):
    ok: bool

class r_PutSeriesGame(Datatype):
    """No content"""

class r_PutSeriesGameDelete(Datatype):
    """No content"""

class r_PutSessionPing(Datatype):
    """No content"""

class r_PutThread(Datatype):
    thread: Thread

class r_PutThreadDelete(Datatype):
    """No content"""

class r_PutThreadLocked(Datatype):
    """No content"""

class r_PutThreadRead(Datatype):
    """No content"""

class r_PutThreadSticky(Datatype):
    """No content"""

class r_PutTicket(Datatype):
    ticketId: str

class r_PutUserSettings(Datatype):
    settings: UserSettings

class r_PutUserUpdateFeaturedRun(Datatype):
    """No content"""

class r_PutUserSocialConnection(Datatype):
    """No content"""

class r_PutUserSocialConnectionDelete(Datatype):
    """No content"""

class r_PutUserUpdatePassword(Datatype):
    ...  # TODO: document
