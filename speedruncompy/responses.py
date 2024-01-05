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
    standingList: list[Any] #TODO place, registeredPlayerIds[str]

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
    commentsList: list[Comment]
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
