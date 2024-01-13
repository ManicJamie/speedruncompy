from typing import Any, Coroutine
from speedruncompy.datatypes import Datatype
from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunComPy, _log
from .exceptions import SrcpyException
from .enums import *
from .responses import *

SUPPRESS_WARNINGS = False

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

class GetGameLeaderboard2(GetRequest, BasePaginatedRequest):
    """The default leaderboard view."""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLeaderboard2", returns=r_GetGameLeaderboard2, _api=_api,
                          page=page, **param_construct)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameLeaderboard2:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameLeaderboard2]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetGameLeaderboard2]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetGameLeaderboard2:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["runList"]
        extras: r_GetGameLeaderboard2 = pages[1]
        extras.pop("runList")
        extras.pagination.page = 0
        return r_GetGameLeaderboard2({"runList": runList}, skipChecking=True) | extras

class GetGameLeaderboard(GetRequest, BasePaginatedRequest):
    """WARN: This is NOT the view used by SRC! It may be removed at any time!

    This view is included as it is special & returns a bunch of extra information that may be useful."""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLeaderboard", returns=r_GetGameLeaderboard, _api=_api, page=page, **param_construct)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameLeaderboard:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameLeaderboard]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetGameLeaderboard]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetGameLeaderboard:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["runs"]
        extras: Datatype = pages[1]
        extras.pop("runs")
        extras["pagination"]["page"] = 0
        return r_GetGameLeaderboard({"runs": runList}, skipChecking=True) | extras

class GetGameData(GetRequest):
    def __init__(self, gameId: str = None, gameUrl: str = None, **params) -> None:
        if gameId is None and gameUrl is None: raise SrcpyException("GetGameData requires gameId or gameUrl")
        super().__init__("GetGameData", returns=r_GetGameData, gameId=gameId, gameUrl=gameUrl, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameData:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameData]:
        return super().perform_async(retries, delay, **kwargs)

class GetGameSummary(GetRequest):
    def __init__(self, gameId:str, **params) -> None:
        super().__init__("GetGameSummary", returns=r_GetGameSummary, gameId=gameId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameSummary:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameSummary]:
        return super().perform_async(retries, delay, **kwargs)

class GetGameRecordHistory(GetRequest):
    """Get the record history of a category.
    
    #### Other parameters
    - `values[]: list[variableId, valueIds[]]`
    - `emulator: (bool?)` TODO: check
    - `obsolete: bool`"""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameRecordHistory", returns=r_GetGameRecordHistory, _api=_api, page=page, **param_construct)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameRecordHistory:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameRecordHistory]:
        return super().perform_async(retries, delay, **kwargs)

class GetSearch(GetRequest):
    """Search for an object based on its name.

    #### Other parameters:
    - `limit: int` max. 500
    - `includeGames: bool`
    - `includeNews: bool`
    - `includePages: bool`
    - `includeSeries: bool`
    - `includeUsers: bool`
    """
    def __init__(self, query: str, **params) -> None:
        super().__init__("GetSearch", returns=r_GetSearch, query=query, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetSearch:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetSearch]:
        return super().perform_async(retries, delay, **kwargs)

class GetLatestLeaderboard(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetLatestLeaderboard", returns=r_GetLatestLeaderboard, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetLatestLeaderboard:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetLatestLeaderboard]:
        return super().perform_async(retries, delay, **kwargs)

class GetRun(GetRequest):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRun", returns=r_GetRun, runId=runId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetRun:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetRun]:
        return super().perform_async(retries, delay, **kwargs)

class GetUserPopoverData(GetRequest):
    def __init__(self, userId, **params) -> None:
        super().__init__("GetUserPopoverData", returns=r_GetUserPopoverData, userId=userId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetUserPopoverData:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetUserPopoverData]:
        return super().perform_async(retries, delay, **kwargs)

class GetArticleList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetArticleList", returns=r_GetArticleList, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetArticleList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetArticleList]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetArticleList]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetArticleList:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        if not SUPPRESS_WARNINGS:
            _log.warning("GetArticleList depagination is currently untested, as fewer than 500 pages exist on the site.")
        articleList = []
        for p in pages.values():
            articleList += p["articleList"]
        extras: r_GetArticleList = pages[1]
        extras.pop("articleList")
        extras.pagination.page = 0
        return r_GetArticleList({"articleList": articleList}, skipChecking=True) | extras

class GetArticle(GetRequest):
    def __init__(self, id = None, slug = None, **params) -> None:
        if id is None and slug is None: raise SrcpyException("GetArticle requires id or slug")
        super().__init__("GetArticle", returns=r_GetArticle, id=id, slug=slug, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetArticle:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetArticle]:
        return super().perform_async(retries, delay, **kwargs)

class GetGameList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetGameList", returns=r_GetGameList, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameList]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetGameList]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetGameList:
        return super().perform_all(retries, delay)
    
    def _combine_results(self, pages: dict):
        gameList = []
        for p in pages.values():
            gameList += p["gameList"]
        extras: r_GetGameList = pages[1]
        extras.pop("gameList")
        extras.pagination.page = 0
        return r_GetGameList({"gameList": gameList}, skipChecking=True) | extras

class GetHomeSummary(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetHomeSummary", returns=r_GetHomeSummary, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetHomeSummary:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetHomeSummary]:
        return super().perform_async(retries, delay, **kwargs)

class GetSeriesList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetSeriesList", returns=r_GetSeriesList, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetSeriesList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetSeriesList]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetSeriesList]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetSeriesList:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        seriesList = []
        for p in pages.values():
            seriesList += p["seriesList"]
        extras: dict = pages[1]
        extras.pop("seriesList")
        extras.pop("pagination")
        return {"seriesList": seriesList} | extras

class GetSeriesSettings(GetRequest):
    ... #TODO: complete

class GetGameLevelSummary(GetRequest, BasePaginatedRequest):
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameRecordHistory", returns=r_GetGameLevelSummary, _api=_api, page=page, **param_construct)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameLevelSummary:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameLevelSummary]:
        return super().perform_async(retries, delay, **kwargs)

class GetGuideList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGuideList", returns=r_GetGuideList, gameId=gameId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGuideList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGuideList]:
        return super().perform_async(retries, delay, **kwargs)

class GetGuide(GetRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetGuide", returns=r_GetGuide, id=id, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGuide:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGuide]:
        return super().perform_async(retries, delay, **kwargs)

class GetNewsList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetNewsList", returns=r_GetNewsList, gameId=gameId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetNewsList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetNewsList]:
        return super().perform_async(retries, delay, **kwargs)

class GetNews(GetRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetNews", returns=r_GetNews, id=id, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetNews:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetNews]:
        return super().perform_async(retries, delay, **kwargs)

class GetResourceList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetResourceList", returns=r_GetResourceList, gameId=gameId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetResourceList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetResourceList]:
        return super().perform_async(retries, delay, **kwargs)

class GetStreamList(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetStreamList", returns=r_GetStreamList, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetStreamList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetStreamList]:
        return super().perform_async(retries, delay, **kwargs)

class GetThreadList(GetRequest):
    def __init__(self, forumId: str, **params) -> None:
        super().__init__("GetThreadList", returns=r_GetThreadList, forumId=forumId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetThreadList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetThreadList]:
        return super().perform_async(retries, delay, **kwargs)

class GetChallenge(GetRequest):
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallenge", returns=r_GetChallenge, id=id, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetChallenge:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetChallenge]:
        return super().perform_async(retries, delay, **kwargs)

class GetChallengeLeaderboard(GetRequest, BasePaginatedRequest):
    def __init__(self, challengeId, **params) -> None:
        super().__init__("GetChallengeLeaderboard", returns=r_GetChallengeLeaderboard, challengeId=challengeId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetChallengeLeaderboard:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetChallengeLeaderboard]:
        return super().perform_async(retries, delay, **kwargs)

class GetChallengeRun(GetRequest):
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallengeRun", returns=r_GetChallengeRun, id=id, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetChallengeRun:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetChallengeRun]:
        return super().perform_async(retries, delay, **kwargs)

# The below are POSTed by the site, but also accept GET so are placed here to separate from endpoints requiring auth.
class GetUserLeaderboard(GetRequest):
    def __init__(self, userId: str, **params) -> None:
        super().__init__("GetUserLeaderboard", returns=r_GetUserLeaderboard, userId=userId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetUserLeaderboard:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetUserLeaderboard]:
        return super().perform_async(retries, delay, **kwargs)

class GetCommentList(GetRequest, BasePaginatedRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentList", returns=r_GetCommentList, itemId=itemId, itemType=itemType, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetCommentList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetCommentList]:
        return super().perform_async(retries, delay, **kwargs)

class GetThread(GetRequest , BasePaginatedRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetThread", returns=r_GetThread, id=id, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetThread:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetThread]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetThread]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetThread:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        commentList = []
        for p in pages.values():
            commentList += p["commentList"]
        extras: dict = pages[1]
        extras.pop("commentList")
        extras.pop("pagination")
        return {"commentList": commentList} | extras

class GetForumList(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetForumList", returns=r_GetForumList, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetForumList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetForumList]:
        return super().perform_async(retries, delay, **kwargs)

"""
POST requests may require auth
"""

# Session
class PutAuthLogin(PostRequest):
    def __init__(self, name: str, password: str, token: str = None, **params) -> None:
        super().__init__("PutAuthLogin", name=name, password=password, token=token, **params)

class PutAuthLogout(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthLogout", **params)

class PutAuthSignup(PostRequest): #TODO Finish
    ... # Probably not responsible to disclose easily...

class GetSession(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetSession", **params)

class PutSessionPing(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutSessionPing", **params)

# Supermod actions
class GetAuditLogList(PostRequest, BasePaginatedRequest):
    """WARN: not currently depaginated due to lack of testing availaibility.
    
    To protect against future updates before v1.0, use `._perform_all_raw()`"""
    def __init__(self, gameId: str = None, seriesId: str = None, eventType: eventType = eventType.NONE, page: int = 1, **params) -> None:
        if gameId is None and seriesId is None: raise SrcpyException("GetAuditLogList requires gameId or seriesId")
        super().__init__("GetAuditLogList", gameId=gameId, seriesId=seriesId, eventType=eventType, page=page, **params)
    
    def _combine_results(self, pages: dict):
        #TODO: Method stub
        return super()._combine_results(pages)

# Mod actions
class GetGameSettings(PostRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameSettings", gameId=gameId, **params)

class PutGameSettings(PostRequest):
    def __init__(self, gameId: str, settings: dict, **params) -> None:
        super().__init__("PutGameSettings", gameId=gameId, settings=settings, **params)

# Run verification
class GetModerationGames(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetModerationGames", **params)

class GetModerationRuns(PostRequest, BasePaginatedRequest):
    def __init__(self, gameId: str, limit: int = 100, page: int = 1, **params) -> None:
        super().__init__("GetModerationRuns", gameId=gameId, limit=limit, page=page, **params)
    
    def _combine_results(self, pages: dict):
        #TODO: is this all really necessary?
        games = [pages[1]["games"][0]]
        categories, levels, platforms, players, regions, runs, users, values, variables = ([] for i in range(9))
        for page in pages.values():
            for c in (c for c in page["categories"] if c not in categories): categories.append(c)
            for l in (l for l in page["levels"] if l not in levels): levels.append(l)
            for p in (p for p in page["platforms"] if p not in platforms): platforms.append(p)
            for p in (p for p in page["players"] if p not in players): players.append(p)
            for r in (r for r in page["regions"] if r not in regions): regions.append(r)
            for u in (u for u in page["users"] if u not in users): users.append(u)
            for v in (v for v in page["values"] if v not in values): values.append(v)
            for v in (v for v in page["variables"] if v not in variables): variables.append(v)
            runs += page["runs"]
        return {"categories": categories, "games": games, "levels": levels, "platforms": platforms, "players": players,
                "regions": regions, "runs": runs, "users": users, "values": values, "variables": variables}

class PutRunAssignee(PostRequest):
    def __init__(self, assigneeId: str, runId: str, **params) -> None:
        super().__init__("PutRunAssignee", assigneeId=assigneeId, runId=runId, **params)

class PutRunVerification(PostRequest):
    def __init__(self, runId: str, verified: int, **params) -> None:
        super().__init__("PutRunVerification", runId=runId, verified=verified, **params)

# Run management
class GetRunSettings(PostRequest):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRunSettings", runId=runId, **params)

class PutRunSettings(PostRequest):
    def __init__(self, csrfToken: str, settings: dict, **params) -> None:
        """Sets a run's settings. Note that the runId is contained in `settings`."""
        super().__init__("PutRunSettings", csrfToken=csrfToken, settings=settings, **params)

# User inbox actions
class GetConversations(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetConversations", **params)

class GetConversationMessages(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetConversationMessages", **params)

# User notifications
class GetNotifications(PostRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetNotifications", **params)

    def _combine_results(self, pages: dict):
        notifications = []
        for p in pages.values():
            notifications += p["notifications"]
        extras: dict = pages[1]
        extras.pop("notifications")
        extras.pop("pagination")
        return {"notifications": notifications} | extras

# User settings
class GetUserSettings(PostRequest):
    """Gets a user's settings. Note that unless you are a site mod, you can only get your own settings."""
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSettings", userUrl=userUrl, **params)

class PutUserSettings(PostRequest):
    def __init__(self, userUrl: str, settings: dict, **params) -> None:
        super().__init__("PutUserSettings", userUrl=userUrl, settings=settings, **params)

# Comment Actions
class GetCommentable(PostRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentable", itemId=itemId, itemType=itemType, **params)

class PutComment(PostRequest):
    def __init__(self, itemId: str, itemType: int, text: str, **params) -> None:
        super().__init__("PutComment", itemId=itemId, itemType=itemType, text=text, **params)

#TODO: test params
class PutCommentableSettings(PostRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("PutCommentableSettings", itemId=itemId, itemType=itemType, **params)

# Thread Actions
class GetThreadReadStatus(PostRequest):
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__("GetThreadReadStatus", threadIds=threadIds, **params)

class PutThreadRead(PostRequest):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadRead", threadId=threadId, **params)

# Forum actions
class GetForumReadStatus(PostRequest):
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__("GetForumReadStatus", forumIds=forumIds, **params)

# Theme actions
class GetThemeSettings(PostRequest):
    def __init__(self, **params) -> None:
        """Provide either userId or gameId"""
        super().__init__("GetThemeSettings", **params)

# To Be Sorted
class GetTickets(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetTickets", **params) #TODO: needs param testing

class GetUserBlocks(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetUserBlocks", **params)

class GetUserSupporterData(PostRequest):
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSupporterData", userUrl=userUrl, **params)

class PutConversation(PostRequest):
    def __init__(self, csrfToken: str, recipientIds: list[str], text: str, **params) -> None:
        super().__init__("PutConversation", csrfToken=csrfToken, recipientIds=recipientIds, text=text, **params)

class PutConversationMessage(PostRequest):
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__("PutConversationMessage", csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

class PutGame(PostRequest): #TODO: needs param testing
    def __init__(self, name: str, releaseDate: int, gameTypeIds: list[gameType], seriesId: str, **params) -> None:
        super().__init__("PutGame", name=name, releaseDate=releaseDate, gameTypeIds=gameTypeIds, seriesId=seriesId, **params)

class PutGameBoostGrant(PostRequest): #TODO: test type of `anonymous`
    def __init__(self, gameId: str, anonymous: bool, **params) -> None:
        super().__init__("PutGameBoostGrant", gameId=gameId, anonymous=anonymous, **params)

class PutGameModerator(PostRequest): #TODO: level enum type
    def __init__(self, gameId: str, userId: str, level: int, **params) -> None:
        super().__init__("PutGameModerator", gameId=gameId, userId=userId, level=level, **params)

class PutGameModeratorDelete(PostRequest): #TODO: test `level` necessity & enum type
    def __init__(self, gameId: str, userId: str, level: int, **params) -> None:
        super().__init__("PutGameModeratorDelete", gameId=gameId, userId=userId, level=level, **params)

class PutSeriesGame(PostRequest): #TODO: reminder on who can do this & what this does lol
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGame", seriesId=seriesId, gameId=gameId, **params)

class PutSeriesGameDelete(PostRequest):
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGameDelete", seriesId=seriesId, gameId=gameId, **params)

class PutTicket(PostRequest): #TODO: test parameter types
    def __init__(self, metadata, type, **params) -> None:
        super().__init__("PutTicket", metadata=metadata, type=type, **params)

class PutUserSocialConnection(PostRequest):
    def __init__(self, userId: str, networkId: NetworkId, value: str, **params) -> None:
        super().__init__("PutUserSocialConnection", userId=userId, networkId=networkId, value=value, **params)

class PutUserSocialConnectionDelete(PostRequest):
    def __init__(self, userId: str, networkId: NetworkId, **params) -> None:
        super().__init__("PutUserSocialConnectionDelete", userId=userId, networkId=networkId, **params)

class PutUserUpdatePassword(PostRequest):
    def __init__(self, userUrl: str, oldPassword: str, newPassword: str, **params) -> None:
        super().__init__("PutUserUpdatePassword", userUrl=userUrl, oldPassword=oldPassword, newPassword=newPassword, **params)

class PutCommentDelete(PostRequest):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentDelete", commentId=commentId, **params)

class PutCommentRestore(PostRequest):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentRestore", commentId=commentId, **params)

class PutThread(PostRequest):
    def __init__(self, forumId: str, name: str, body: str, **params) -> None:
        super().__init__("PutThread", forumId=forumId, name=name, body=body, **params)

class PutThreadLocked(PostRequest):
    def __init__(self, threadId: str, locked: bool, **params) -> None:
        super().__init__("PutThreadLocked", threadId=threadId, locked=locked, **params)

class PutThreadSticky(PostRequest):
    def __init__(self, threadId: str, sticky: bool, **params) -> None:
        super().__init__("PutThreadSticky", threadId=threadId, sticky=sticky, **params)

class PutThreadDelete(PostRequest):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadDelete", threadId=threadId, **params)