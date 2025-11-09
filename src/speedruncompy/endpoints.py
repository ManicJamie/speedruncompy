from typing import Iterable
from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunClient
from .datatypes.enums import *
from .datatypes.responses import *
from .datatypes import Pagination

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

def _nested_params(**params: Any) -> dict:
    page = params.pop("page", None)
    param_construct = {"params": params, "page": page}
    return param_construct

class GetGameLeaderboard2(GetRequest[r_GetGameLeaderboard2], BasePaginatedRequest[r_GetGameLeaderboard2],
                          endpoint="GetGameLeaderboard2", response=r_GetGameLeaderboard2):
    """The default leaderboard view.
    
    NB: by default runs without video are excluded; provide `video = 0` to include them.
    
    ### Mandatory:
    - @gameId
    - @categoryId

    ### Optional:
    - @dateFrom: datestr = Release date # Needs to be in "YYYY-MM-DD" format
    - @dateTo: datestr = Now # Needs to be in "YYYY-MM-DD" format
    - @emulator: `EmulatorFilter`
    - @levelId: If `categoryId` refers to a level category.
    - @obsolete: `ObsoleteFilter` = 0
    - @platformIds
    - @regionIds
    - @timer: TimerName to sort by
    - @verified: `VerifiedFilter` = 1 # Runs will be filtered by status
    - @values: A list of `VarValues`
    - @video: `VideoFilter` = 1 (=Required (!))
    - @page
    """
    def __init__(
            self,
            gameId: str,
            categoryId: str,
            
            _client: SpeedrunClient | None = None,
            dateFrom: str | None = None,
            dateTo: str | None = None,
            emulator: EmulatorFilter | None = None,
            levelId: str | None = None,
            obsolete: ObsoleteFilter | None = None,
            platformIds: list[str] | None = None,
            regionIds: list[str] | None = None,
            timer: TimerName | None = None,
            verified: VerifiedFilter | None = None,
            values: list[VarValues] | None = None,
            video: VideoFilter | None = None,
            **params
        ) -> None:
        super().__init__(_client=_client, **_nested_params(
            gameId=gameId,
            categoryId=categoryId,
            dateFrom=dateFrom,
            dateTo=dateTo,
            emulator=emulator,
            levelId=levelId,
            obsolete=obsolete,
            platformIds=platformIds,
            regionIds=regionIds,
            timer=timer,
            verified=verified,
            values=values,
            video=video,
            **params
        ))

class GetGameLeaderboard(GetRequest[r_GetGameLeaderboard], BasePaginatedRequest[r_GetGameLeaderboard],
                         endpoint="GetGameLeaderboard", response=r_GetGameLeaderboard):
    """A secondary leaderboard view. WARNING: Not used on the site, may be removed at any time!

    ### Mandatory:
    - @gameId
    - @categoryId

    ### Optional: # These are copied from GetGameLeaderboard2 - impart from verified
    - @dateFrom: datestr = Release date # Needs to be in "YYYY-MM-DD" format
    - @dateTo: datestr = Now # Needs to be in "YYYY-MM-DD" format
    - @emulator: `EmulatorFilter`
    - @levelId: If `categoryId` refers to a level category.
    - @obsolete: `ObsoleteFilter` = 0
    - @platformIds
    - @regionIds
    - @timer: TimerName to sort by
    - @values: A list of `VarValues`
    - @video: `VideoFilter` = 1 (=Required (!))
    - @page
    """
    def __init__(
            self,
            gameId: str,
            categoryId: str,
            
            _client: SpeedrunClient | None = None,
            dateFrom: str | None = None,
            dateTo: str | None = None,
            emulator: EmulatorFilter | None = None,
            levelId: str | None = None,
            obsolete: ObsoleteFilter | None = None,
            platformIds: list[str] | None = None,
            regionIds: list[str] | None = None,
            timer: TimerName | None = None,
            values: list[VarValues] | None = None,
            video: VideoFilter | None = None,
            **params
        ) -> None:
        super().__init__(_client=_client, **_nested_params(
            gameId=gameId,
            categoryId=categoryId,
            dateFrom=dateFrom,
            dateTo=dateTo,
            emulator=emulator,
            levelId=levelId,
            obsolete=obsolete,
            platformIds=platformIds,
            regionIds=regionIds,
            timer=timer,
            values=values,
            video=video,
            **params
        ))
    
    # Overrides to compensate for pagination being nested
    def _get_pagination(self, p: r_GetGameLeaderboard) -> Pagination:
        return p.leaderboard.pagination
    
    @classmethod
    def _combine_pages(cls, responses: Iterable[r_GetGameLeaderboard]) -> r_GetGameLeaderboard:
        return r_GetGameLeaderboard.model_construct(leaderboard=BasePaginatedRequest._combine_pages(r.leaderboard for r in responses)) 
        

class GetGameData(GetRequest[r_GetGameData], 
                  endpoint="GetGameData", response=r_GetGameData):
    """Gets game data used for discovering runs.
    
    ### Mandatory:
    #### One of:
    - @gameId
    - @gameUrl
    """
    def __init__(self, 
                 gameId: str | None = None, 
                 gameUrl: str | None = None, 
                 
                 _client: SpeedrunClient | None = None, 
                 **params) -> None:
        super().__init__(gameId=gameId, gameUrl=gameUrl, _client=_client, **params)

class GetGameSummary(GetRequest[r_GetGameSummary], 
                     endpoint="GetGameSummary", response=r_GetGameSummary):
    """Gets game metadata used for discovering forums, news, stats, threads etc.
    ### Mandatory:
    #### One of:
    - @gameId
    - @gameUrl
    """
    def __init__(self, 
                 gameId: str | None = None, 
                 gameUrl: str | None = None, 
                 
                 _client: SpeedrunClient | None = None,
                 **params) -> None:
        super().__init__(gameId=gameId, gameUrl=gameUrl, _client=_client, **params)

class GetGameRecordHistory(GetRequest[r_GetGameRecordHistory], 
                           endpoint="GetGameRecordHistory", response=r_GetGameRecordHistory):
    """Get the record history of a category.
    
    ### Mandatory:
    - @gameId
    - @categoryId

    ### Other:
    - @values: A list of VariableValues
    - @emulator: EmulatorFilter
    - @obsolete: ObsoleteFilter
    """
    def __init__(self, 
                 gameId: str, 
                 categoryId: str, 
                 _client: SpeedrunClient | None = None, 
                 **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__(_client=_client, page=page, **param_construct)

class GetSearch(GetRequest[r_GetSearch], 
                endpoint="GetSearch", response=r_GetSearch):
    """Search for an object based on its name. May include multiple types to search for at once.

    ### Optional:
    - @query: str
    - @favorExactMatches: bool = False
    - @includeGames: bool = False
    - @includeNews: bool = False
    - @includePages: bool = False
    - @includeSeries: bool = False
    - @includeUsers: bool = False
    - @includeChallenges: bool = False
    - @limit: <= 500 = 500
    """
    def __init__(
            self,
            query: str,
            favorExactMatches: bool | None = None,
            includeGames: bool | None = None,
            includeNews: bool | None = None,
            includePages: bool | None = None,
            includeSeries: bool | None = None,
            includeUsers: bool | None = None,
            includeChallenges: bool | None = None,
            **params) -> None:
        super().__init__(query=query, favorExactMatches=favorExactMatches,
                         includeGames=includeGames, includeNews=includeNews, includePages=includePages,
                         includeSeries=includeSeries, includeUsers=includeUsers,
                         includeChallenges=includeChallenges, **params)

class GetLatestLeaderboard(GetRequest[r_GetLatestLeaderboard], 
                           endpoint="GetLatestLeaderboard", response=r_GetLatestLeaderboard):
    """Gets most recent runs.

    ### Optional:
    - @gameId
    - @seriesId
    - @limit: <= 999 = 10
    """
    def __init__(self, gameId: str | None = None, seriesId: str | None = None, **params) -> None:
        super().__init__(gameId=gameId, seriesId=seriesId, **params)

class GetRun(GetRequest[r_GetRun], 
             endpoint="GetRun", response=r_GetRun):
    """Gets all parameters pertinent to displaying a single run.
    
    ### Mandatory:
    - @runId
    """
    def __init__(self, runId: str, **params) -> None:
        super().__init__(runId=runId, **params)

class GetUserSummary(GetRequest[r_GetUserSummary], 
                     endpoint="GetUserSummary", response=r_GetUserSummary):
    """Gets a user's profile data.
    
    ### Mandatory:
    - @url
    """
    def __init__(self, url: str, **params) -> None:
        super().__init__(url=url, **params)

class GetUserComments(GetRequest[r_GetUserComments], BasePaginatedRequest[r_GetUserComments], 
                      endpoint="GetUserComments", response=r_GetUserComments):
    """Get all of a user's comments.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

class GetUserPopoverData(GetRequest[r_GetUserPopoverData], 
                         endpoint="GetUserPopoverData", response=r_GetUserPopoverData):
    """Gets data for user popovers. Includes `userSocialConnectionList`, `userStats` & `titleList`.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId, **params) -> None:
        super().__init__(userId=userId, **params)

class GetTitleList(GetRequest[r_GetTitleList],
                   endpoint="GetTitleList", response=r_GetTitleList):
    """Gets a list of all titles available on the site.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetTitle(GetRequest[r_GetTitle],
               endpoint="GetTitle", response=r_GetTitle):
    """Gets a specific title.
    
    ### Mandatory:
    - @titleId
    """
    def __init__(self, titleId, **params) -> None:
        super().__init__(titleId=titleId, **params)

class GetArticleList(BasePaginatedRequest[r_GetArticleList], GetRequest[r_GetArticleList],
                     endpoint="GetArticleList", response=r_GetArticleList):
    """Gets a list of articles on the site.
    
    ### Optional:
    - @published: bool = True # If published articles should be included
    - @rejected: bool = True # If rejected articles should be included
    - @search: str
    - @tags: [] # List of a tag's text to filter by
    - @target: str # Filters by where the article's meant to be published
    - @limit: <= 500 = 500. Number of elements per page.
    """
    def __init__(
            self,
            published: bool | None = None,
            rejected: bool | None = None,
            search: str | None = None,
            tags: list[str] | None = None,
            target: str | None = None,
            limit: int | None = None,
            **params
        ) -> None:
        super().__init__(published=published, rejected=rejected, search=search,
                         tags=tags, target=target, limit=limit, **params)

class GetArticle(GetRequest[r_GetArticle], 
                 endpoint="GetArticle", response=r_GetArticle):
    """Gets a specific article from the site.
    
    ### Mandatory:
    #### One of:
    - @id
    - @slug
    """
    def __init__(self, id: str | None = None, slug: str | None = None, **params) -> None:
        super().__init__(id=id, slug=slug, **params)

class GetGameList(GetRequest[r_GetGameList], BasePaginatedRequest[r_GetGameList],
                  endpoint="GetGameList", response=r_GetGameList):
    """Gets a list of all games on the site.
    
    ### Optional:
    - @seriesId: filter by series
    - @platformId: filter by platform
    - @search: str
    - @orderType: `GameOrderType` = 1
    - @limit: <= 200 = 500 (!)"""
    def __init__(
            self,
            seriesId: str | None = None,
            platformId: str | None = None,
            search: str | None = None,
            orderType: GameOrderType | None = None,
            **params
        ) -> None:
        super().__init__(seriesId=seriesId, platformId=platformId,
                         search=search, orderType=orderType, **params)

class GetHomeSummary(GetRequest[r_GetHomeSummary],
                     endpoint="GetHomeSummary", response=r_GetHomeSummary):
    """Gets information for the home page. Often empty.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetSeriesList(GetRequest[r_GetSeriesList], BasePaginatedRequest[r_GetSeriesList],
                    endpoint="GetSeriesList", response=r_GetSeriesList):
    """Gets a list of series on the site.

    ### Optional:
    - @search: str
    - @orderType: `GameOrderType` = 1
    - @limit: <= 500 = 500
    """
    def __init__(
            self,
            search: str | None = None,
            orderType: GameOrderType | None = None,
            **params) -> None:
        super().__init__(search=search, orderType=orderType, **params)

class GetSeriesSummary(GetRequest[r_GetSeriesSummary],
                       endpoint="GetSeriesSummary", response=r_GetSeriesSummary):
    """Gets most information pertinent to a series.
    
    ### Mandatory:
    #### One of:
    - @seriesId
    - @seriesUrl
    """
    def __init__(self, seriesId: str | None = None, seriesUrl: str | None = None, **params) -> None:
        super().__init__(seriesId=seriesId, seriesUrl=seriesUrl, **params)

class GetGameLevelSummary(GetRequest[r_GetGameLevelSummary],
                          endpoint="GetGameLevelSummary", response=r_GetGameLevelSummary):
    """Gets the top 3 runs from all levels under a level category.
    
    ### Mandatory:
    - @gameId
    - @categoryId

    ### Optional:
    - @dateFrom: datestr = Release date # Needs to be in "YYYY-MM-DD" format
    - @dateTo: datestr = Now # Needs to be in "YYYY-MM-DD" format
    - @emulator: `EmulatorFilter`
    - @levelId: If `categoryId` refers to a level category.
    - @obsolete: `ObsoleteFilter` = 0
    - @platformIds
    - @regionIds
    - @timer: TimerName to sort by
    - @verified: `VerifiedFilter` = 1 # If runs other than verified should be included
    - @values: A list of `VarValues`
    - @video: `VideoFilter` = 1 (=Required (!))
    - @page
    """
    def __init__(
            self,
            gameId: str,
            categoryId: str,
            
            _client: SpeedrunClient | None = None,
            dateFrom: str | None = None,
            dateTo: str | None = None,
            emulator: EmulatorFilter | None = None,
            levelId: str | None = None,
            obsolete: ObsoleteFilter | None = None,
            platformIds: list[str] | None = None,
            regionIds: list[str] | None = None,
            timer: TimerName | None = None,
            verified: VerifiedFilter | None = None,
            values: list[VarValues] | None = None,
            video: VideoFilter | None = None,
            **params) -> None:
        super().__init__(_client=_client, **_nested_params(
            gameId=gameId,
            categoryId=categoryId,
            dateFrom=dateFrom,
            dateTo=dateTo,
            emulator=emulator,
            levelId=levelId,
            obsolete=obsolete,
            platformIds=platformIds,
            regionIds=regionIds,
            timer=timer,
            verified=verified,
            values=values,
            video=video,
            **params))

class GetGuideList(GetRequest[r_GetGuideList],
                   endpoint="GetGuideList", response=r_GetGuideList):
    """Gets all guides on a game.

    ### Mandatory
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__(gameId=gameId, **params)

class GetGuide(GetRequest[r_GetGuide],
               endpoint="GetGuide", response=r_GetGuide):
    """Get a specific guide by id.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id: str, **params) -> None:
        super().__init__(id=id, **params)

class GetNewsList(GetRequest[r_GetNewsList],
                  endpoint="GetNewsList", response=r_GetNewsList):
    """Get a list of game news articles.
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__(gameId=gameId, **params)

class GetNews(GetRequest[r_GetNews],
              endpoint="GetNews", response=r_GetNews):
    """Get a game news article.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id: str, **params) -> None:
        super().__init__(id=id, **params)

class GetResourceList(GetRequest[r_GetResourceList],
                      endpoint="GetResourceList", response=r_GetResourceList):
    """Get a list of a game's resources.
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__(gameId=gameId, **params)

class GetStreamList(GetRequest[r_GetStreamList],
                    endpoint="GetStreamList", response=r_GetStreamList):
    """Gets a list of live runners.
    
    ## Optional:
    - @seriesId
    - @gameId
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetThreadList(GetRequest[r_GetThreadList],
                    endpoint="GetThreadList", response=r_GetThreadList):
    """Get threads on a forum.
    
    ### Mandatory:
    - @forumId
    """
    def __init__(self, forumId: str, **params) -> None:
        super().__init__(forumId=forumId, **params)

class GetChallenge(GetRequest[r_GetChallenge],
                   endpoint="GetChallenge", response=r_GetChallenge):
    """Get a specific Challenge.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id, **params) -> None:
        super().__init__(id=id, **params)

class GetChallengeLeaderboard(GetRequest[r_GetChallengeLeaderboard], BasePaginatedRequest[r_GetChallengeLeaderboard],
                              endpoint="GetChallengeLeaderboard", response=r_GetChallengeLeaderboard):
    """Get runs from a Challenge board.
    
    NB: While this response is paginated, the default "per" set is 1,000,000, so depagination is not particularly necessary.

    ### Mandatory:
    - @challengeId
    """
    def __init__(self, challengeId, **params) -> None:
        super().__init__(challengeId=challengeId, **params)

class GetChallengeGlobalRankingList(GetRequest[r_GetChallengeGlobalRankingList],
                                    endpoint="GetChallengeGlobalRankingList", response=r_GetChallengeGlobalRankingList):
    """Get a sitewide leaderboard for users who have won the most in Challenges.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetChallengeRun(GetRequest[r_GetChallengeRun],
                      endpoint="GetChallengeRun", response=r_GetChallengeRun):
    """Get a specific Challenge run (not the same as a normal run!)
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id, **params) -> None:
        super().__init__(id=id, **params)

# The below are POSTed by the site, but also accept GET so are placed here to separate from endpoints requiring auth.
class GetUserLeaderboard(GetRequest[r_GetUserLeaderboard],
                         endpoint="GetUserLeaderboard", response=r_GetUserLeaderboard):
    """Get a user's runs for display on their profile.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

class GetCommentList(GetRequest[r_GetCommentList], BasePaginatedRequest[r_GetCommentList],
                     endpoint="GetCommentList", response=r_GetCommentList):
    """Get a list of comments on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType: ItemType of the above `itemId`
    """
    def __init__(self, itemId: str, itemType: ItemType, **params) -> None:
        super().__init__(itemId=itemId, itemType=itemType, **params)

class GetThread(GetRequest[r_GetThread], BasePaginatedRequest[r_GetThread],
                endpoint="GetThread", response=r_GetThread):
    """Get a specific thread.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id: str, **params) -> None:
        super().__init__(id=id, **params)

class GetForumList(GetRequest[r_GetForumList],
                   endpoint="GetForumList", response=r_GetForumList):
    """Get a list of site-wide forums. When logged in, may include forums of followed games.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetStaticData(GetRequest[r_GetStaticData],
                    endpoint="GetStaticData", response=r_GetStaticData):
    """Get static data for the site. Including all areas, colors, gameTypes, platforms, etc.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)


"""
POST requests may require auth
"""

# Session
class PutAuthLogin(PostRequest[r_PutAuthLogin],
                   endpoint="PutAuthLogin", response=r_PutAuthLogin):
    """Logs in. If 2FA is enabled, first provide `name` & `password`, then check `tokenChallengeSent` and repeat w/ token.
    Provide `_client` to authorise a specific API instance, otherwise the default instance will be used.
    
    ### Mandatory:
    - @name
    - @password
    - @token: On second attempt if 2FA is enabled.
    """
    def __init__(self, name: str, password: str, token: str | None = None, **params) -> None:
        super().__init__(name=name, password=password, token=token, **params)

class PutAuthLogout(PostRequest[r_Empty],
                    endpoint="PutAuthLogout", response=r_Empty):
    """Logs out.
    Provide `_client` to log out a specific API instance, otherwise the default instance will be used.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class PutAuthSignup(PostRequest[r_PutAuthSignup],
                    endpoint="PutAuthSignup", response=r_PutAuthSignup):
    """Creates & logs in to a new account.
    
    Parameters undocumented.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetSession(PostRequest[r_GetSession],
                 endpoint="GetSession", response=r_GetSession):
    """Gets information about the current user's session.
    Includes `csrfToken`, required for some endpoints.
    """
    def __init__(self, **params) -> None:
        super().__init__( **params)
    
class PutSessionPing(PostRequest[r_Empty],
                     endpoint="PutSessionPing", response=r_Empty):
    """Tells SRC to renew your session. Some other endpoints will renew your session.
    May be required to keep your session alive without re-login.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

# Supermod actions
class GetAuditLogList(PostRequest[r_GetAuditLogList], BasePaginatedRequest[r_GetAuditLogList],
                      endpoint="GetAuditLogList", response=r_GetAuditLogList):
    """Gets a game, series or user's audit log.
    
    ### Mandatory:
    - @eventType: Type to filter by (default "")
    - @page
    #### One of:
    - @gameId
    - @seriesId
    - @userId: Every change that has happened to this user
    - @actorId: Every change this user has made (Admin only)
    """
    def __init__(self, 
                 gameId: str | None = None, 
                 seriesId: str | None = None, 
                 userId: str | None = None, 
                 actorId: str | None = None,
                 eventType: EventType = EventType.NONE, 
                 page: int = 1, 
                 **params
                 ) -> None:
        super().__init__(gameId=gameId, seriesId=seriesId, userId=userId, actorId=actorId, 
                         eventType=eventType, page=page, **params)

#region GameSettings
class GetGameSettings(PostRequest[r_GetGameSettings],
                      endpoint="GetGameSettings", response=r_GetGameSettings):
    """Get a game's settings. Must be at least a verifier on the game.
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__(gameId=gameId, **params)

class PutGameSettings(PostRequest[r_Empty],
                      endpoint="PutGameSettings", response=r_Empty):
    """Set a game's settings. Must be at least a moderator on the game.

    ### Mandatory:
    - @gameId: Must be provided even though `settings` contains `id`.
    - @settings
    """
    def __init__(self, gameId: str, settings: GameSettings, **params) -> None:
        super().__init__(gameId=gameId, settings=settings, **params)

class PutCategory(PostRequest[r_Empty],
                  endpoint="PutCategory", response=r_Empty):
    """Creates a new category.
    
    ### Mandatory:
    - @gameId
    - @category
    """
    def __init__(self, gameId: str, category: Category, **params) -> None:
        super().__init__(gameId=gameId, category=category, **params)

class PutCategoryUpdate(PostRequest[r_Empty],
                        endpoint="PutCategoryUpdate", response=r_Empty):
    """Updates an existing category.
    
    ### Mandatory:
    - @gameId
    - @categoryId
    - @category
    """
    def __init__(self, gameId: str, categoryId: str, category: Category, **params) -> None:
        super().__init__(gameId=gameId, categoryId=categoryId, category=category, **params)

class PutCategoryArchive(PostRequest[r_Empty],
                         endpoint="PutCategoryArchive", response=r_Empty):
    """Archives a category.
    
    ### Mandatory:
    - @gameId
    - @categoryId
    """
    def __init__(self, gameId: str, categoryId: str, **params) -> None:
        super().__init__(gameId=gameId, categoryId=categoryId, **params)

class PutCategoryRestore(PostRequest[r_Empty],
                         endpoint="PutCategoryRestore", response=r_Empty):
    """Restores an archived category.
    
    ### Mandatory:
    - @gameId
    - @categoryId
    """
    def __init__(self, gameId: str, categoryId: str, **params) -> None:
        super().__init__(gameId=gameId, categoryId=categoryId, **params)

class PutCategoryOrder(PostRequest[r_Empty],
                       endpoint="PutCategoryOrder", response=r_Empty):
    """Re-orders categories.
    
    ### Mandatory:
    - @gameId
    - @categoryIds
    """
    def __init__(self, gameId: str, categoryIds: list[str], **params) -> None:
        super().__init__(gameId=gameId, categoryIds=categoryIds, **params)

class PutLevel(PostRequest[r_Empty],
               endpoint="PutLevel", response=r_Empty):
    """Creates a new level.
    
    ### Mandatory:
    - @gameId
    - @level
    """
    def __init__(self, gameId: str, level: Level, **params) -> None:
        super().__init__(gameId=gameId, level=level, **params)

class PutLevelUpdate(PostRequest[r_Empty],
                     endpoint="PutLevelUpdate", response=r_Empty):
    """Updates an existing level.
    
    ### Mandatory:
    - @gameId
    - @levelId
    - @level
    """
    def __init__(self, gameId: str, levelId: str, level: Level, **params) -> None:
        super().__init__(gameId=gameId, levelId=levelId, level=level, **params)

class PutLevelArchive(PostRequest[r_Empty],
                      endpoint="PutLevelArchive", response=r_Empty):
    """Archives a level.
    
    ### Mandatory:
    - @gameId
    - @levelId
    """
    def __init__(self, gameId: str, levelId: str, **params) -> None:
        super().__init__(gameId=gameId, levelId=levelId, **params)

class PutLevelRestore(PostRequest[r_Empty],
                      endpoint="PutLevelRestore", response=r_Empty):
    """Restores an archived level.
    
    ### Mandatory:
    - @gameId
    - @levelId
    """
    def __init__(self, gameId: str, levelId: str, **params) -> None:
        super().__init__(gameId=gameId, levelId=levelId, **params)

class PutLevelOrder(PostRequest[r_Empty],
                    endpoint="PutLevelOrder", response=r_Empty):
    """Re-orders levels.
    
    ### Mandatory:
    - @gameId
    - @levelIds
    """
    def __init__(self, gameId: str, levelIds: list[str], **params) -> None:
        super().__init__(gameId=gameId, levelIds=levelIds, **params)

class PutVariable(PostRequest[r_Empty],
                  endpoint="PutVariable", response=r_Empty):
    """Creates a new variable.
    
    ### Mandatory:
    - @gameId
    - @variable
    - @values
    """
    def __init__(self, gameId: str, variable: Variable, values: list[Value], **params) -> None:
        super().__init__(gameId=gameId, variable=variable, values=values, **params)

class PutVariableUpdate(PostRequest[r_Empty],
                        endpoint="PutVariableUpdate", response=r_Empty):
    """Updates an existing variable.
    
    ### Mandatory:
    - @gameId
    - @variableId
    - @variable
    """
    def __init__(self, gameId: str, variableId: str, variable: Variable, values: list[Value], **params) -> None:
        super().__init__(gameId=gameId, variableId=variableId, variable=variable, values=values, **params)

class PutVariableArchive(PostRequest[r_Empty],
                         endpoint="PutVariableArchive", response=r_Empty):
    """Archives a variable.
    
    ### Mandatory:
    - @gameId
    - @variableId
    """
    def __init__(self, gameId: str, variableId: str, **params) -> None:
        super().__init__(gameId=gameId, variableId=variableId, **params)

class PutVariableRestore(PostRequest[r_Empty],
                         endpoint="PutVariableRestore", response=r_Empty):
    """Restores an archived variable.
    
    ### Mandatory:
    - @gameId
    - @variableId
    """
    def __init__(self, gameId: str, variableId: str, **params) -> None:
        super().__init__(gameId=gameId, variableId=variableId, **params)

class PutVariableOrder(PostRequest[r_Empty],
                       endpoint="PutVariableOrder", response=r_Empty):
    """Re-orders variables. NOTE: only all subcategories OR all annotations are taken at once.
    
    ### Mandatory:
    - @gameId
    - @variableIds
    """
    def __init__(self, gameId: str, variableIds: list[str], **params) -> None:
        super().__init__(gameId=gameId, variableIds=variableIds, **params)

class PutVariableApplyDefault(PostRequest[r_Ok],
                              endpoint="PutVariableApplyDefault", response=r_Ok):
    """Set the default value on a variable.
    
    ### Mandatory:
    - @gameId
    - @variableId
    """
    def __init__(self, gameId: str, variableId: str, **params) -> None:
        super().__init__(gameId=gameId, variableId=variableId, **params)

#endregion GameSettings

#region GameMetadata

class PutNews(PostRequest[r_Empty],
              endpoint="PutNews", response=r_Empty):
    """Posts a news item to a game.
    
    ### Mandatory: # TODO: check all
    - @gameId
    - @userId: of the author
    - @title
    - @body
    - @date
    """
    def __init__(self, gameId: str, userId: str, title: str,
                 body: str, date: int, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, title=title, body=body, date=date, **params)

class PutNewsUpdate(PostRequest[r_Empty],
                    endpoint="PutNewsUpdate", response=r_Empty):
    """Updates a news item.
    
    ### Mandatory: # TODO: check all
    - @newsId
    - @userId: of the author
    - @title
    - @body
    - @date
    """
    def __init__(self, newsId: str, userId: str, title: str,
                 body: str, date: int, **params) -> None:
        super().__init__(newsId=newsId, userId=userId, title=title, body=body, date=date, **params)

class PutNewsDelete(PostRequest[r_Empty],
                    endpoint="PutNewsDelete", response=r_Empty):
    """Deletes a news item.
    
    ### Mandatory:
    - @newsId
    """
    def __init__(self, newsId: str, **params) -> None:
        super().__init__(newsId=newsId, **params)

class PutGuide(PostRequest[r_Empty],
               endpoint="PutGuide", response=r_Empty):
    """Posts a guide item to a game.
    
    ### Mandatory: # TODO: check all
    - @gameId
    - @userId: of the author
    - @name
    - @text
    - @date
    """
    def __init__(self, gameId: str, userId: str, name: str,
                 text: str, date: int, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, name=name, text=text, date=date, **params)

class PutGuideUpdate(PostRequest[r_Empty],
                     endpoint="PutGuideUpdate", response=r_Empty):
    """Updates a guide item.
    
    ### Mandatory: # TODO: check all
    - @guideId
    - @userId: of the author
    - @name
    - @text
    - @date
    """
    def __init__(self, guideId: str, userId: str, name: str,
                 text: str, date: int, **params) -> None:
        super().__init__(guideId=guideId, userId=userId, name=name, text=text, date=date, **params)

class PutGuideDelete(PostRequest[r_Empty],
                     endpoint="PutGuideDelete", response=r_Empty):
    """Deletes a guide item.
    
    ### Mandatory:
    - @guideId
    """
    def __init__(self, guideId: str, **params) -> None:
        super().__init__(guideId=guideId, **params)

class PutResource(PostRequest[r_Empty],
                  endpoint="PutResource", response=r_Empty):
    """Posts a resource item to a game.
    
    ### Mandatory: # TODO: check all, check base64 encoding of content
    - @gameId
    - @userId: Manager ID
    - @authorNames: Comma-separated list of names
    - @date
    - @name
    - @description
    - @type: ResourceType
    
    EITHER:
    - @link
    
    OR:
    - @uploadFilename
    - @uploadContent: str "data:application/json;base64,examplebase64data"
    """
    def __init__(self, gameId: str, userId: str, name: str,
                 description: str, date: int, type: ResourceType, authorNames: str, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, name=name, description=description,
                         date=date, type=type, authorNames=authorNames, **params)

class PutResourceUpdate(PostRequest[r_Empty],
                        endpoint="PutResourceUpdate", response=r_Empty):
    """Updates a resource item.
    
    ### Mandatory: # TODO: check all, check base64 encoding of content
    - @gameId
    - @userId: Manager ID
    - @authorNames: Comma-separated list of names
    - @date
    - @name
    - @description
    - @type: ResourceType
    ### Optional:
    
    EITHER
    - @link
    
    OR:
    - @uploadFilename
    - @uploadContent: str "data:application/json;base64,examplebase64data"
    """
    def __init__(self, resourceId: str, userId: str, name: str,
                 description: str, date: int, type: ResourceType, authorNames: str, **params) -> None:
        super().__init__(resourceId=resourceId, userId=userId, name=name, description=description,
                         date=date, type=type, authorNames=authorNames, **params)

class PutResourceDelete(PostRequest[r_Empty],
                        endpoint="PutResourceDelete", response=r_Empty):
    """Deletes a resource item.
    
    ### Mandatory:
    - @resourceId
    """
    def __init__(self, resourceId: str, **params) -> None:
        super().__init__(resourceId=resourceId, **params)

#endregion GameMetadata

# Run verification
class GetModerationGames(PostRequest[r_GetModerationGames],
                         endpoint="GetModerationGames", response=r_GetModerationGames):
    """Get moderation games & stats for the logged in user.
        WARN: does not error when not logged in, instead the response fields will be None.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetModerationRuns(PostRequest[r_GetModerationRuns], BasePaginatedRequest[r_GetModerationRuns],
                        endpoint="GetModerationRuns", response=r_GetModerationRuns):
    """Get data for runs waiting in the moderation queue for a game.

    ### Mandatory:
    - @gameId
    - @limit: int <= 200
    - @page

    ### Optional:
    - @search
    - @verified: `Verified`
    - @verifiedById
    - @videoState: `VideoState`
    """

    # Default for `limit` is 20 which is what the site uses
    def __init__(self, gameId: str, limit: int = 20, page: int = 1, **params) -> None:
        super().__init__(gameId=gameId, limit=limit, page=page, **params)

class PutRunAssignee(PostRequest[r_Empty],
                     endpoint="PutRunAssignee", response=r_Empty):
    """Assigns a verifier to a run."""
    def __init__(self, assigneeId: str, runId: str, **params) -> None:
        super().__init__(assigneeId=assigneeId, runId=runId, **params)

class PutRunVerification(PostRequest[r_Ok],
                         endpoint="PutRunVerification", response=r_Ok):
    """Assigns a verification level `Verified` to a run.
    
    ### Mandatory:
    - @runId
    - @verified: `Verified.PENDING`, `Verified.VERIFIED`, `Verified.REJECTED`
    """
    def __init__(self, runId: str, verified: Verified, **params) -> None:
        super().__init__(runId=runId, verified=verified, **params)

class PutRunVideoState(PostRequest[r_Ok],
                       endpoint="PutRunVideoState", response=r_Ok):
    """Assigns a video-at-risk state to a run.
    
    ### Mandatory:
    - @runId
    - @videoState
    """
    def __init__(self, runId: str, videoState: VideoState, **params) -> None:
        super().__init__(runId=runId, videoState=videoState, **params)

# Run management
class GetRunSettings(PostRequest[r_GetRunSettings],
                     endpoint="GetRunSettings", response=r_GetRunSettings):
    """Gets a run's settings
    """
    def __init__(self, runId: str, **params) -> None:
        super().__init__(runId=runId, **params)

class PutRunSettings(PostRequest[r_PutRunSettings],
                     endpoint="PutRunSettings", response=r_PutRunSettings):
    """Sets a run's settings OR submit a new run if `settings.runId` is None.
    
    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @settings: Existing run settings if `runId is not None`, otherwise new run's settings.
    - @autoverify: If the run should be automatically verified after editing or not. - only works for game moderators.
    """
    def __init__(self, csrfToken: str, settings: RunSettings, autoverify: bool, **params) -> None:
        """Sets a run's settings. Note that the runId is contained in `settings`."""
        super().__init__(csrfToken=csrfToken, settings=settings, autoverify=autoverify, **params)

# User inbox actions
class GetConversations(PostRequest[r_GetConversations],
                       endpoint="GetConversations", response=r_GetConversations):
    """Gets conversations the user is involved in.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class GetConversationMessages(PostRequest[r_GetConversationMessages],
                              endpoint="GetConversationMessages", response=r_GetConversationMessages):
    """Gets messages from a given conversation.
    
    ### Mandatory:
    - @conversationId
    """
    def __init__(self, conversationId, **params) -> None:
        super().__init__(conversationId=conversationId, **params)

class PutConversation(PostRequest[r_PutConversation],
                      endpoint="PutConversation", response=r_PutConversation):
    """Creates a new conversation. May include several users.
    If the conversation already exists, the message is sent to the existing conversation.
    
    NOTE: if the conversation exists but the user has left it, they will _not_ rejoin the conversation.
    
    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @recipientIds: A list of other users to add to the conversation.
    - @text: Content of the initial message.
    """
    def __init__(self, csrfToken: str, recipientIds: list[str], text: str, **params) -> None:
        super().__init__(csrfToken=csrfToken, recipientIds=recipientIds, text=text, **params)

class PutConversationMessage(PostRequest[r_PutConversationMessage],
                             endpoint="PutConversationMessage", response=r_PutConversationMessage):
    """Sends a message to a conversation.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    - @text
    """
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__(csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

class PutConversationLeave(PostRequest[r_Empty],
                           endpoint="PutConversationLeave", response=r_Empty):
    """Leaves a conversation.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    """
    def __init__(self, csrfToken: str, conversationId: str, **params) -> None:
        super().__init__(csrfToken=csrfToken, conversationId=conversationId, **params)

class PutConversationReport(PostRequest[r_Ok],
                            endpoint="PutConversationReport", response=r_Ok):
    """Reports a conversation.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    - @text: User description of the report
    """
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__(csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

# User notifications & follows
class GetNotifications(PostRequest[r_GetNotifications], BasePaginatedRequest[r_GetNotifications],
                       endpoint="GetNotifications", response=r_GetNotifications):
    """Gets the user's notifications.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class PutGameFollower(PostRequest[r_Empty],
                      endpoint="PutGameFollower", response=r_Empty):
    """Follow a game.
    
    ### Mandatory:
    - @gameId
    - @userId: own userId
    """
    def __init__(self, gameId: str, userId: str, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, **params)

class PutGameFollowerDelete(PostRequest[r_Empty],
                            endpoint="PutGameFollowerDelete", response=r_Empty):
    """Unfollow a game.
    
    ### Mandatory:
    - @gameId
    - @userId: own userId
    """
    def __init__(self, gameId: str, userId: str, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, **params)

class PutUserFollower(PostRequest[r_Empty],
                      endpoint="PutUserFollower", response=r_Empty):
    """Follow a user.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

class PutUserFollowerDelete(PostRequest[r_Empty],
                            endpoint="PutUserFollowerDelete", response=r_Empty):
    """Unfollow a user.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

# User settings
class GetUserSettings(PostRequest[r_GetUserSettings],
                      endpoint="GetUserSettings", response=r_GetUserSettings):
    """Gets a user's settings.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are a site moderator.
    """
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__(userUrl=userUrl, **params)

class PutUserSettings(PostRequest[r_PutUserSettings],
                      endpoint="PutUserSettings", response=r_PutUserSettings):
    """Sets a user's settings.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are a site moderator.
    - @settings
    """
    def __init__(self, userUrl: str, settings: UserSettings, **params) -> None:
        super().__init__(userUrl=userUrl, settings=settings, **params)

class PutUserUpdateFeaturedRun(PostRequest[r_Empty],
                               endpoint="PutUserUpdateFeaturedRun", response=r_Empty):
    """Sets the run featured on a user's profile.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are an admin.
    - @fullRunId: If omitted, clears the full game featured run.
    - @levelRunId: If omitted, clears the level featured run
    """
    def __init__(self, userUrl: str, fullRunId: str | None = None, levelRunId: str | None = None, **params) -> None:
        super().__init__(userUrl=userUrl, fullRunId=fullRunId, levelRunId=levelRunId, **params)

class PutUserUpdateGameOrdering(PostRequest[r_Empty],
                                endpoint="PutUserUpdateGameOrdering", response=r_Empty):
    """Updates the order of games displayed on your profile.
    
    Note that having multiple GameOrderGroups is a Supporter-only feature. The default group has fixed id "default".
    
    ### Mandatory:
    - @userUrl: must be your own unless you are an admin.
    - @groups: Groups to display on the profile.
    """
    def __init__(self, userUrl: str, groups: list[GameOrderGroup], **params) -> None:
        super().__init__(userUrl=userUrl, groups=groups, **params)

class GetUserApiKey(PostRequest[r_GetUserApiKey],
                    endpoint="GetUserApiKey", response=r_GetUserApiKey):
    """Get a user's API key.

    ### Mandatory:
    - @userId

    ### Optional:
    - @regenerate: bool = False # Returns a new API key if True
    """
    def __init__(self, userId: str, regenerate: bool | None = None, **params) -> None:
        super().__init__(userId=userId, regenerate=regenerate, **params)

class GetUserGameBoostData(PostRequest[r_GetUserGameBoostData],
                           endpoint="GetUserGameBoostData", response=r_GetUserGameBoostData):
    """Get a list of games that a user has boosted.

    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

class GetUserDataExport(PostRequest[r_GetUserDataExport],
                        endpoint="GetUserDataExport", response=r_GetUserDataExport):
    """Get a user's exported data.

    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__(userId=userId, **params)

class PutGameFollowerOrder(PostRequest[r_Empty],
                           endpoint="PutGameFollowerOrder", response=r_Empty):
    """Reorder a user's followed games.

    ### Mandatory:
    - @gameIds: list of game Ids in the order they should be in
    - @userId
    """
    def __init__(self, gameIds: list[str], userId: str, **params) -> None:
        super().__init__(gameIds=gameIds, userId=userId, **params)

# PUT IT HERE

# Comment Actions
class GetCommentable(PostRequest[r_GetCommentable],
                     endpoint="GetCommentable", response=r_GetCommentable):
    """Checks the comment permissions on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType
    """
    def __init__(self, itemId: str, itemType: ItemType, **params) -> None:
        super().__init__(itemId=itemId, itemType=itemType, **params)

class PutComment(PostRequest[r_Empty],
                 endpoint="PutComment", response=r_Empty):
    """Posts a comment on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType
    - @text
    """
    def __init__(self, itemId: str, itemType: ItemType, text: str, **params) -> None:
        super().__init__(itemId=itemId, itemType=itemType, text=text, **params)

class PutLike(PostRequest[r_PutLike],
              endpoint="PutLike", response=r_PutLike):
    """Adds or removes a like to a comment.
    
    ### Mandatory:
    - @itemId
    - @itemType
    - @like
    """
    def __init__(self, itemId: str, itemType: ItemType, like: bool, **params) -> None:
        super().__init__(itemId=itemId, itemType=itemType, like=like, **params)

class PutCommentableSettings(PostRequest[r_Empty],
                             endpoint="PutCommentableSettings", response=r_Empty):
    """Updates commentable settings on an item.

    ### Mandatory:
    - @itemId
    - @itemType
    - @disabled
    - @locked
    """
    def __init__(self, itemId: str, itemType: ItemType, **params) -> None:
        super().__init__(itemId=itemId, itemType=itemType, **params)

# Thread Actions
class GetThreadReadStatus(PostRequest[r_GetThreadReadStatus],
                          endpoint="GetThreadReadStatus", response=r_GetThreadReadStatus):
    """Gets whether a set of threads have been read by the user.
    
    ### Mandatory:
    - @threadIds: list of IDs
    """
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__(threadIds=threadIds, **params)

class PutThreadRead(PostRequest[r_Empty],
                    endpoint="PutThreadRead", response=r_Empty):
    """Sets a thread as read by the user.

    ### Mandatory:
    - @threadId
    """
    def __init__(self, threadId: str, **params) -> None:
        super().__init__(threadId=threadId, **params)

# Forum actions
class GetForumReadStatus(PostRequest[r_GetForumReadStatus],
                         endpoint="GetForumReadStatus", response=r_GetForumReadStatus):
    """Gets whether a set of forums have been read by the user.

    ### Mandatory:
    - @forumIds: list of IDs
    """
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__(forumIds=forumIds, **params)

# Theme actions
class GetThemeSettings(PostRequest[r_GetThemeSettings],
                       endpoint="GetThemeSettings", response=r_GetThemeSettings):
    """Gets a user, game or series' theme.  # TODO: check noargs & series

    ### Mandatory:
    #### One of:
    - @userId
    - @gameId
    - @seriesId
    """
    def __init__(
            self,
            userId: str | None = None,
            gameId: str | None = None,
            seriesId: str | None = None,
            **params) -> None:
        super().__init__(userId=userId, gameId=gameId,
                         seriesId=seriesId, **params)

class PutThemeSettings(PostRequest[r_Empty],
                       endpoint="PutThemeSettings", response=r_Empty):
    """Sets a user, game or series' theme.

    ### Mandatory:
    #### One of:
    - @userId
    - @gameId
    - @seriesId
    - @settings: ThemeSettings
    """
    def __init__(self, settings: ThemeSettings, userId: str | None = None, gameId: str | None = None, seriesId: str | None = None, **params) -> None:
        super().__init__(userId=userId, gameId=gameId, seriesId=seriesId, settings=settings, **params)

# Supporter
class GetUserSupporterData(PostRequest[r_GetUserSupporterData],
                           endpoint="GetUserSupporterData", response=r_GetUserSupporterData):
    """Gets supporter data for a user. # TODO: check auth

    ### Mandatory:
    - @userUrl
    """
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__(userUrl=userUrl, **params)

class PutUserSupporterNewSubscription(PostRequest[r_PutUserSupporterNewSubscription],
                                      endpoint="PutUserSupporterNewSubscription", response=r_PutUserSupporterNewSubscription):
    """Get data used to construct a payment form.
    
    ## Mandatory:
    - @planKey: strEnum ("monthly" or "yearly")
    - @userUrl
    """
    def __init__(self, planKey: SupportPlanPeriod, userUrl: str, **params) -> None:
        super().__init__(planKey=planKey, userUrl=userUrl, **params)

class PutGameBoostGrant(PostRequest[r_Empty],
                        endpoint="PutGameBoostGrant", response=r_Empty):
    """Adds a boost to a game.
    
    ### Mandatory:
    - @gameId
    - @anonymous
    """
    def __init__(self, gameId: str, anonymous: bool, **params) -> None:
        super().__init__(gameId=gameId, anonymous=anonymous, **params)

# To Be Sorted
class PutAdvertiseContact(PostRequest[r_Empty],
                          endpoint="PutAdvertiseContact", response=r_Empty):
    """Sends a request for contact to SRC for collaboration.
    
    ### Mandatory:
    - @name
    - @company
    - @email
    - @message
    """
    def __init__(self, name: str, company: str, email: str, message: str, **params) -> None:
        super().__init__(name=name, company=company, email=email, message=message, **params)

class GetTickets(PostRequest[r_GetTickets], BasePaginatedRequest[r_GetTickets],
                 endpoint="GetTickets", response=r_GetTickets):
    """Gets tickets submitted by the user.

    ### Optional:
    - @ticketIds: list of ticket IDs to fetch
    - @queues: list of `TicketQueueType` to filter by
    - @types: list of `TicketType`
    - @statuses: list of `TicketStatus`
    - @requestorIds: list of userIds who requested the ticket. - this is meant for use by site admins
    - @search: str
    """
    def __init__(
            self,
            ticketIds: list[str] | None = None,
            queues: list[TicketQueueType] | None = None,
            types: list[TicketType] | None = None,
            statuses: list[TicketStatus] | None = None,
            requestorIds: list[str] | None = None,
            search: str | None = None,
            **params
        ) -> None:
        super().__init__(ticketIds=ticketIds, queues=queues,
                         types=types, statuses=statuses, requestorIds=requestorIds,
                         search=search, **params)

class GetSeriesSettings(PostRequest[r_GetSeriesSettings],
                        endpoint="GetSeriesSettings", response=r_GetSeriesSettings):
    """Gets settings of a series.

    ### Mandatory:
    - @seriesId
    """
    def __init__(self, seriesId: str, **params) -> None:
        super().__init__(seriesId=seriesId, **params)

class GetUserBlocks(PostRequest[r_GetUserBlocks],
                    endpoint="GetUserBlocks", response=r_GetUserBlocks):
    """Gets blocks relevant to a user, both as blocker and blockee.
    """
    def __init__(self, **params) -> None:
        super().__init__(**params)

class PutUserBlock(PostRequest[r_Empty],
                   endpoint="PutUserBlock", response=r_Empty):
    """Blocks or unblocks a user.
    
    ## Mandatory:
    - @block
    - @blockeeId
    """
    def __init__(self, block: bool, blockeeId: str, **params) -> None:
        super().__init__(block=block, blockeeId=blockeeId, **params)

class PutGame(PostRequest[r_PutGame],
              endpoint="PutGame", response=r_PutGame):  # TODO: needs param testing
    """Add a new game.

    ### Mandatory:
    - @name
    - @releaseDate

    ### Optional:
    - @gameTypeIds: list of `GameType`
    - @baseGame: str # If one of the GameTypes supports a baseGame, then this can be included with a game id.

    #### Optional:
    - @seriesId
    """
    def __init__(
            self,
            name: str,
            releaseDate: int,
            gameTypeIds: list[GameType] | None = None,
            baseGame: str | None = None,
            seriesId: str | None = None,
            **params
        ) -> None:
        super().__init__(name=name, releaseDate=releaseDate, gameTypeIds=gameTypeIds,
                         baseGame=baseGame, seriesId=seriesId, **params)

class PutGameModerator(PostRequest[r_Empty],
                       endpoint="PutGameModerator", response=r_Empty):
    """Add a moderator to a game.
    
    ### Mandatory:
    - @gameId
    - @userId
    - @level: GamePowerLevel (-1 = verifier, 0 = mod, 1 = supermod)
    """
    def __init__(self, gameId: str, userId: str, level: GamePowerLevel, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, level=level, **params)

class PutGameModeratorDelete(PostRequest[r_Empty],
                             endpoint="PutGameModeratorDelete", response=r_Empty):  # TODO: test `level` necessity & enum type
    """Remove a moderator from a game.
    
    ### Mandatory:
    - @gameId
    - @userId
    """
    def __init__(self, gameId: str, userId: str, **params) -> None:
        super().__init__(gameId=gameId, userId=userId, **params)

class PutSeriesGame(PostRequest[r_Empty],
                    endpoint="PutSeriesGame", response=r_Empty):
    """Add an existing game to a series.
    
    ### Mandatory:
    - @seriesId
    - @gameId
    """
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__(seriesId=seriesId, gameId=gameId, **params)

class PutSeriesGameDelete(PostRequest[r_Empty],
                          endpoint="PutSeriesGameDelete", response=r_Empty):
    """Remove a game from a series. Does not delete the game.
    
    ### Mandatory:
    - @seriesId
    - @gameId
    """
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__(seriesId=seriesId, gameId=gameId, **params)

class PutTicket(PostRequest[r_PutTicket],
                endpoint="PutTicket", response=r_PutTicket):
    """Submits support tickets.

    ### Mandatory:
    - @metadata: a JSON string of ticket data
    - @type: `TicketType` # TODO: check TicketType vs TicketQueue Type
    """
    def __init__(self, metadata: str, type: TicketType, **params) -> None:
        super().__init__(metadata=metadata, type=type, **params)

class PutTicketNote(PostRequest[r_Ok],
                    endpoint="PutTicketNote", response=r_Ok):
    """Adds a note/message to a ticket. When `isMessage` is `false`, only admins can post or read the note.
    
    ### Mandatory:
    - @ticketId
    - @note
    - @isMessage: whether the note is a message to the user. `False` only permitted for admins.
    """
    def __init__(self, ticketId: str, note: str, isMessage: bool, **params) -> None:
        super().__init__(ticketId=ticketId, note=note, isMessage=isMessage, **params)

class PutUserSocialConnection(PostRequest[r_Empty],
                              endpoint="PutUserSocialConnection", response=r_Empty):  # TODO: verification?
    """Modifies a user's social connection.

    ### Mandatory:
    - @userId
    - @networkId: see `NetworkId`
    - @value
    """
    def __init__(self, userId: str, networkId: NetworkId, value: str, **params) -> None:
        super().__init__(userId=userId, networkId=networkId, value=value, **params)

class PutUserSocialConnectionDelete(PostRequest[r_Empty],
                                    endpoint="PutUserSocialConnectionDelete", response=r_Empty):
    """Remove a user's social connection.
    
    ### Mandatory:
    - @userId
    - @networkId: see `NetworkId`
    """
    def __init__(self, userId: str, networkId: NetworkId, **params) -> None:
        super().__init__(userId=userId, networkId=networkId, **params)

class PutUserUpdatePassword(PostRequest[r_Ok],
                            endpoint="PutUserUpdatePassword", response=r_Ok):
    """Update a user's password.
    
    ### Mandatory:
    - @userUrl
    - @oldPassword
    - @newPassword
    """
    def __init__(self, userUrl: str, oldPassword: str, newPassword: str, **params) -> None:
        super().__init__(userUrl=userUrl, oldPassword=oldPassword, newPassword=newPassword, **params)

class PutUserUpdateEmail(PostRequest[r_PutUserUpdateEmail],
                         endpoint="PutUserUpdateEmail", response=r_PutUserUpdateEmail):
    """Update a user's email.
    First, you send userUrl, email and password. SRC will respond with `tokenChallengeSent: true`
    Afterwards, you send the above data again but this time with `token` set.
    
    ### Mandatory:
    - @userUrl: str
    - @email: str

    ### Optional:
    - @token: str
    - @password: str # Only optional if the user is authed as an admin
    """
    def __init__(self, userUrl: str, email: str, password: str | None = None, token: str | None = None, **params) -> None:
        super().__init__(userUrl=userUrl, email=email, password=password, token=token, **params)

class PutUserUpdateName(PostRequest[r_Ok],
                        endpoint="PutUserUpdateName", response=r_Ok):  # TODO: check what the response is
    """Update a user's name.
    
    ### Mandatory:
    - @userUrl: str # URL of the user to update
    - @newName: str
    - @acceptTerms: bool
    """  # TODO: check if these are mandatory
    def __init__(self, userUrl: str, newName: str, acceptTerms: bool, **params) -> None:
        super().__init__(userUrl=userUrl, newName=newName, acceptTerms=acceptTerms, **params)

class PutCommentDelete(PostRequest[r_Empty],
                       endpoint="PutCommentDelete", response=r_Empty):
    """Delete a comment.

    ### Mandatory:
    - @commentId
    """
    def __init__(self, commentId: str, **params) -> None:
        super().__init__(commentId=commentId, **params)

class PutCommentRestore(PostRequest[r_Empty],
                        endpoint="PutCommentRestore", response=r_Empty):
    """Restores a deleted comment

    ### Mandatory:
    - @commentId
    """
    def __init__(self, commentId: str, **params) -> None:
        super().__init__(commentId=commentId, **params)

class PutThread(PostRequest[r_PutThread],
                endpoint="PutThread", response=r_PutThread):
    """Create a new thread on a forum.

    ### Mandatory:
    - @forumId
    - @name
    - @body
    """
    def __init__(self, forumId: str, name: str, body: str, **params) -> None:
        super().__init__(forumId=forumId, name=name, body=body, **params)

class PutThreadLocked(PostRequest[r_Empty],
                      endpoint="PutThreadLocked", response=r_Empty):
    """Lock or unlock a thread.

    ### Mandatory:
    - @threadId
    - @locked
    """
    def __init__(self, threadId: str, locked: bool, **params) -> None:
        super().__init__(threadId=threadId, locked=locked, **params)

class PutThreadSticky(PostRequest[r_Empty],
                      endpoint="PutThreadSticky", response=r_Empty):
    """Sticky or un-sticky a thread.

    ### Mandatory:
    - @threadId
    - @sticky
    """
    def __init__(self, threadId: str, sticky: bool, **params) -> None:
        super().__init__(threadId=threadId, sticky=sticky, **params)

class PutThreadDelete(PostRequest[r_Empty],
                      endpoint="PutThreadDelete", response=r_Empty):
    """Delete a thread.

    ### Mandatory:
    - @threadId
    """
    def __init__(self, threadId: str, **params) -> None:
        super().__init__(threadId=threadId, **params)
