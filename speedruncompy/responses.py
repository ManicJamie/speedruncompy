from .datatypes import *
from typing import Any

class r_DefaultResponse(dict):
    ...

"""GET responses"""

class r_GetArticle(Datatype):
    article: Article
    relatedArticleList: Any # Currently unknown typed list, leaving as Any for now
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
    theme: Optional[Theme]
    users: list[User]
    values: list[Value]
    variables: list[Variable]

class r_GetGameLeaderboard(Datatype):
    leaderboard: Leaderboard # not funny. didn't laugh

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
    gameStats: GameStats
    stats: GameStats
    relatedGames: list[Game]
    seriesList: list[Series]
    theme: Theme
    threadList: list[Thread]
    users: list[User]
    challengeList: list[Challenge] #TODO: Check (Any)
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
    stream: Stream

class r_GetLatestLeaderboard(Datatype):
    categories: list[Category]
    games: list[Game]
    levels: list[Level]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]
    values: list[Value]
    variables: list[Variable]

class r_GetNews(Datatype):
    news: News
    users: list[User]

class r_GetNewsList(Datatype):
    newsList: list[News]
    users: list[User]

class r_GetResourceList(Datatype):
    resourceList: list[Resource]

class r_GetRun(Datatype):
    game: Game
    category: Category
    level: Optional[Level]
    platform: Optional[Platform]
    players: list[Player]
    region: Region
    run: Run
    users: list[User]
    values: list[Value]
    variables: list[Variable]

class r_GetSearch(Datatype):
    gameList: list[Game]
    newsList: list[News]
    pageList: list[Article] #TODO: check
    seriesList: list[Series]
    userList: list[User]

class r_GetSeriesList(Datatype):
    seriesList: list[Series]
    pagination: Pagination

class r_GetStreamList(Datatype):
    gameList: list[Game]
    streamList: list[Stream]
    userList: list[User]

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
    userProfile: UserProfile
    users: list[User]
    """Always empty"""
    values: list[Value]
    variables: list[Variable]
    followedGameIds: None
    """Unused null key"""
    challengeList: list[Challenge]
    challengeRunList: list[ChallengeRun]

class r_GetUserPopoverData(Datatype):
    user: User
    userProfile: UserProfile
    userStats: UserStats
    userSocialConnectionList: list[UserSocialConnection]
    games: list[Game]
    """Always empty"""

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

class r_GetForumReadStatus(Datatype):
    forumReadStatusList: ForumReadStatus

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
    categories:  list[Category]
    games: list[Game]
    levels: list[Level]
    pagination: Pagination
    platforms: list[Platform]
    players: list[Player]
    regions: list[Region]
    runs: list[Run]

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
    settings: ThemeSettings
    theme: Theme

class r_GetThreadReadStatus(Datatype):
    threadReadStatusList: list[ThreadReadStatus]

class r_GetTickets(Datatype):
    ticketList: list[Ticket]
    ticketNoteList: Any #TODO: document
    pagination: Pagination
    userList: list[User]
    gameList: list[Game]

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
    supporterCreditList: Any #TODO: document
    supportCodeList: Any #TODO: document
    supporterSubscription: Optional[Any]
    experimentList: Any
    enabledExperimentIds: Any

class r_GetUserSupporterData(Datatype):
    supporterEndDate: int
    boostEndDate: int

class r_PutAuthLogin(Datatype):
    loggedIn: bool
    tokenChallengeSent: Optional[bool]

class r_PutAuthSignup(Datatype):
    loggedIn: bool
    tokenChallengeSent: Optional[bool]

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

class r_PutRunSettings(Datatype):
    runId: str

class r_PutRunVerification(Datatype):
    ok: bool
