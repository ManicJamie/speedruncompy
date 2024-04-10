from typing import Any, Coroutine
from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunComPy, _log
from .exceptions import SrcpyException
from .enums import *
from .responses import *
from .datatypes import Datatype, LenientDatatype
import asyncio

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
        return extras | {"runList": runList}

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
    
    async def _perform_all_async_raw(self, retries=5, delay=1) -> dict[int, dict]:
        self.pages: dict[int, Datatype] = {}
        self.pages[1] = await self.perform_async(retries, delay, page=1)
        numpages = self.pages[1]["leaderboard"]["pagination"]["pages"]
        if numpages > 1:
            results = await asyncio.gather(*[self.perform_async(retries, delay, page=p) for p in range(2, numpages + 1)])
            self.pages.update({p + 2:result for p, result in enumerate(results)})
        return self.pages

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["leaderboard"]["runs"]
        extras: Leaderboard = pages[1]["leaderboard"]
        extras.pop("runs")
        extras["pagination"]["page"] = 0
        return r_GetGameLeaderboard({"leaderboard": Leaderboard(extras | {"runs": runList})})

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
        return extras | {"articleList": articleList}

class GetArticle(GetRequest):
    def __init__(self, id: str = None, slug: str = None, **params) -> None:
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
        return extras | {"gameList": gameList}

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
        extras: r_GetSeriesList = pages[1]
        extras.pop("seriesList")
        extras["pagination"]["page"] = 0
        return extras | {"seriesList": seriesList}

class GetGameLevelSummary(GetRequest):
    """Note: This can take a `page` param but does not split into pages?"""
    #TODO: check what's going on here
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLevelSummary", returns=r_GetGameLevelSummary, _api=_api, page=page, **param_construct)
    
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
    
    def perform_all(self, retries=5, delay=1) -> r_GetCommentList:
        return super().perform_all(retries, delay)
    
    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetCommentList]:
        return super().perform_all_async(retries, delay)
    
    def _combine_results(self, pages: dict):
        #TODO: check likeList, userList for page separation
        commentList = []
        for p in pages.values():
            commentList += p["commentList"]
        extras: dict = pages[1]
        extras.pop("commentList")
        return extras | {"commentList": commentList}

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
        extras["pagination"]["page"] = 0
        return extras | {"commentList": commentList}

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
        super().__init__("PutAuthLogin", returns=r_PutAuthLogin, name=name, password=password, token=token, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutAuthLogin:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutAuthLogin]:
        return super().perform_async(retries, delay, **kwargs)

class PutAuthLogout(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthLogout", returns=r_PutAuthLogout, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutAuthLogout:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutAuthLogout]:
        return super().perform_async(retries, delay, **kwargs)

class PutAuthSignup(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthSignup", returns=r_PutAuthSignup, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutAuthSignup:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutAuthSignup]:
        return super().perform_async(retries, delay, **kwargs)

class GetSession(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetSession", returns=r_GetSession, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetSession:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetSession]:
        return super().perform_async(retries, delay, **kwargs)
    
class PutSessionPing(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutSessionPing", returns=r_PutSessionPing **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutSessionPing:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutSessionPing]:
        return super().perform_async(retries, delay, **kwargs)

# Supermod actions
class GetAuditLogList(PostRequest, BasePaginatedRequest):
    """WARN: not currently depaginated due to lack of testing availaibility.
    
    To protect against future updates before v1.0, use `._perform_all_raw()`"""
    def __init__(self, gameId: str = None, seriesId: str = None, eventType: eventType = eventType.NONE, page: int = 1, **params) -> None:
        if gameId is None and seriesId is None: raise SrcpyException("GetAuditLogList requires gameId or seriesId")
        super().__init__("GetAuditLogList", returns=r_GetAuditLogList, gameId=gameId, seriesId=seriesId, eventType=eventType, page=page, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetAuditLogList:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetAuditLogList]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetAuditLogList]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetAuditLogList:
        return super().perform_all(retries, delay)
    
    def _combine_results(self, pages: dict):
        #TODO: Method stub
        return super()._combine_results(pages)

# Mod actions
class GetGameSettings(PostRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameSettings", returns=r_GetGameSettings, gameId=gameId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetGameSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetGameSettings]:
        return super().perform_async(retries, delay, **kwargs)

class PutGameSettings(PostRequest):
    def __init__(self, gameId: str, settings: dict, **params) -> None:
        super().__init__("PutGameSettings", returns=r_PutGameSettings, gameId=gameId, settings=settings, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutGameSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutGameSettings]:
        return super().perform_async(retries, delay, **kwargs)

#TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO 

# Run verification
class GetModerationGames(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetModerationGames", returns=r_GetModerationGames, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetModerationGames:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetModerationGames]:
        return super().perform_async(retries, delay, **kwargs)

class GetModerationRuns(PostRequest, BasePaginatedRequest):
    def __init__(self, gameId: str, limit: int = 100, page: int = 1, **params) -> None:
        super().__init__("GetModerationRuns", returns=r_GetModerationRuns, gameId=gameId, limit=limit, page=page, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetModerationRuns:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetModerationRuns]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetModerationRuns]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetModerationRuns:
        return super().perform_all(retries, delay)
    
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
        super().__init__("PutRunAssignee", returns=r_PutRunAssignee, assigneeId=assigneeId, runId=runId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutRunAssignee:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutRunAssignee]:
        return super().perform_async(retries, delay, **kwargs)

class PutRunVerification(PostRequest):
    def __init__(self, runId: str, verified: int, **params) -> None:
        super().__init__("PutRunVerification", returns=r_PutRunVerification, runId=runId, verified=verified, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutRunVerification:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutRunVerification]:
        return super().perform_async(retries, delay, **kwargs)

# Run management
class GetRunSettings(PostRequest):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRunSettings", returns=r_GetRunSettings, runId=runId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetRunSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetRunSettings]:
        return super().perform_async(retries, delay, **kwargs)

class PutRunSettings(PostRequest):
    def __init__(self, csrfToken: str, settings: dict, **params) -> None:
        """Sets a run's settings. Note that the runId is contained in `settings`."""
        super().__init__("PutRunSettings", returns=r_PutRunSettings, csrfToken=csrfToken, settings=settings, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutRunSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutRunSettings]:
        return super().perform_async(retries, delay, **kwargs)

# User inbox actions
class GetConversations(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetConversations", returns=r_GetConversations, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetConversations:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetConversations]:
        return super().perform_async(retries, delay, **kwargs)

class GetConversationMessages(PostRequest):
    def __init__(self, conversationId, **params) -> None:
        super().__init__("GetConversationMessages", returns=r_GetConversationMessages, conversationId=conversationId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetConversationMessages:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetConversationMessages]:
        return super().perform_async(retries, delay, **kwargs)

# User notifications
class GetNotifications(PostRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetNotifications", returns=r_GetNotifications, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetNotifications:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetNotifications]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetNotifications]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetNotifications:
        return super().perform_all(retries, delay)

    def _combine_results(self, pages: dict):
        notifications = []
        for p in pages.values():
            notifications += p["notifications"]
        extras: dict = pages[1]
        extras.pop("notifications")
        extras.pop("pagination")
        return extras | {"notifications": notifications}

# User settings
class GetUserSettings(PostRequest):
    """Gets a user's settings. Note that unless you are a site mod, you can only get your own settings."""
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSettings", returns=r_GetUserSettings, userUrl=userUrl, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetUserSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetUserSettings]:
        return super().perform_async(retries, delay, **kwargs)

class PutUserSettings(PostRequest):
    def __init__(self, userUrl: str, settings: dict, **params) -> None:
        super().__init__("PutUserSettings", returns=r_PutUserSettings, userUrl=userUrl, settings=settings, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutUserSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutUserSettings]:
        return super().perform_async(retries, delay, **kwargs)

# Comment Actions
class GetCommentable(PostRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentable", returns=r_GetCommentable, itemId=itemId, itemType=itemType, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetCommentable:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetCommentable]:
        return super().perform_async(retries, delay, **kwargs)

class PutComment(PostRequest):
    def __init__(self, itemId: str, itemType: int, text: str, **params) -> None:
        super().__init__("PutComment", returns=r_PutComment, itemId=itemId, itemType=itemType, text=text, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_PutComment:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutComment]:
        return super().perform_async(retries, delay, **kwargs)

#TODO: test params
class PutCommentableSettings(PostRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("PutCommentableSettings", returns=r_PutCommentableSettings, itemId=itemId, itemType=itemType, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_PutCommentableSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutCommentableSettings]:
        return super().perform_async(retries, delay, **kwargs)

# Thread Actions
class GetThreadReadStatus(PostRequest):
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__("GetThreadReadStatus", returns=r_GetThreadReadStatus, threadIds=threadIds, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetThreadReadStatus:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetThreadReadStatus]:
        return super().perform_async(retries, delay, **kwargs)

class PutThreadRead(PostRequest):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadRead", returns=r_PutThreadRead, threadId=threadId, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_PutThreadRead:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutThreadRead]:
        return super().perform_async(retries, delay, **kwargs)

# Forum actions
class GetForumReadStatus(PostRequest):
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__("GetForumReadStatus", returns=r_GetForumReadStatus, forumIds=forumIds, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetForumReadStatus:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetForumReadStatus]:
        return super().perform_async(retries, delay, **kwargs)

# Theme actions
class GetThemeSettings(PostRequest):
    def __init__(self, **params) -> None:
        """Provide either userId or gameId"""
        super().__init__("GetThemeSettings", returns=r_GetThemeSettings, **params)

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetThemeSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetThemeSettings]:
        return super().perform_async(retries, delay, **kwargs)

# To Be Sorted
class GetTickets(PostRequest, BasePaginatedRequest):
    """WARN: Not currently depaginated, use _perform_all_raw!"""
    def __init__(self, **params) -> None:
        super().__init__("GetTickets", returns=r_GetTickets, **params) #TODO: needs param testing

    def perform(self, retries=5, delay=1, **kwargs) -> r_GetTickets:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetTickets]:
        return super().perform_async(retries, delay, **kwargs)

    def perform_all_async(self, retries=5, delay=1) -> Coroutine[Any, Any, r_GetTickets]:
        return super().perform_all_async(retries, delay)
    
    def perform_all(self, retries=5, delay=1) -> r_GetTickets:
        return super().perform_all(retries, delay)
    
    def _combine_results(self, pages: dict):
        """TODO: method stub"""
        return super()._combine_results(pages)

class GetSeriesSettings(PostRequest):
    def __init__(self, seriesId: str, **params) -> None:
        super().__init__("GetSeriesSettings", returns=r_GetSeriesSettings, seriesId=seriesId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetSeriesSettings:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetSeriesSettings]:
        return super().perform_async(retries, delay, **kwargs)

class GetUserBlocks(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetUserBlocks", returns=r_GetUserBlocks, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetUserBlocks:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetUserBlocks]:
        return super().perform_async(retries, delay, **kwargs)

class GetUserSupporterData(PostRequest):
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSupporterData", returns=r_GetUserSupporterData, userUrl=userUrl, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_GetUserSupporterData:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_GetUserSupporterData]:
        return super().perform_async(retries, delay, **kwargs)

class PutConversation(PostRequest):
    def __init__(self, csrfToken: str, recipientIds: list[str], text: str, **params) -> None:
        super().__init__("PutConversation", returns=r_PutConversation, csrfToken=csrfToken, recipientIds=recipientIds, text=text, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutConversation:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutConversation]:
        return super().perform_async(retries, delay, **kwargs)

class PutConversationMessage(PostRequest):
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__("PutConversationMessage", returns=r_PutConversationMessage, csrfToken=csrfToken, conversationId=conversationId, text=text, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutConversationMessage:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutConversationMessage]:
        return super().perform_async(retries, delay, **kwargs)

class PutGame(PostRequest): #TODO: needs param testing
    def __init__(self, name: str, releaseDate: int, gameTypeIds: list[gameType], seriesId: str, **params) -> None:
        super().__init__("PutGame", returns=r_PutGame, name=name, releaseDate=releaseDate, gameTypeIds=gameTypeIds, seriesId=seriesId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutGame:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutGame]:
        return super().perform_async(retries, delay, **kwargs)

class PutGameBoostGrant(PostRequest): #TODO: test type of `anonymous`
    def __init__(self, gameId: str, anonymous: bool, **params) -> None:
        super().__init__("PutGameBoostGrant", returns=r_PutGameBoostGrant, gameId=gameId, anonymous=anonymous, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutGameBoostGrant:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutGameBoostGrant]:
        return super().perform_async(retries, delay, **kwargs)

class PutGameModerator(PostRequest): #TODO: level enum type
    def __init__(self, gameId: str, userId: str, level: int, **params) -> None:
        super().__init__("PutGameModerator", returns=r_PutGameModerator, gameId=gameId, userId=userId, level=level, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutGameModerator:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutGameModerator]:
        return super().perform_async(retries, delay, **kwargs)

class PutGameModeratorDelete(PostRequest): #TODO: test `level` necessity & enum type
    def __init__(self, gameId: str, userId: str, level: int, **params) -> None:
        super().__init__("PutGameModeratorDelete", returns=r_PutGameModeratorDelete, gameId=gameId, userId=userId, level=level, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutGameModeratorDelete:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutGameModeratorDelete]:
        return super().perform_async(retries, delay, **kwargs)

class PutSeriesGame(PostRequest): #TODO: reminder on who can do this & what this does lol
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGame", returns=r_PutSeriesGame, seriesId=seriesId, gameId=gameId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutSeriesGame:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutSeriesGame]:
        return super().perform_async(retries, delay, **kwargs)

class PutSeriesGameDelete(PostRequest):
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGameDelete", returns=r_PutSeriesGameDelete, seriesId=seriesId, gameId=gameId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutSeriesGameDelete:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutSeriesGameDelete]:
        return super().perform_async(retries, delay, **kwargs)

class PutTicket(PostRequest): #TODO: test parameter types
    def __init__(self, metadata, type, **params) -> None:
        super().__init__("PutTicket", returns=r_PutTicket, metadata=metadata, type=type, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutTicket:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutTicket]:
        return super().perform_async(retries, delay, **kwargs)

class PutUserSocialConnection(PostRequest):
    def __init__(self, userId: str, networkId: NetworkId, value: str, **params) -> None:
        super().__init__("PutUserSocialConnection", returns=r_PutUserSocialConnection, userId=userId, networkId=networkId, value=value, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutUserSocialConnection:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutUserSocialConnection]:
        return super().perform_async(retries, delay, **kwargs)

class PutUserSocialConnectionDelete(PostRequest):
    def __init__(self, userId: str, networkId: NetworkId, **params) -> None:
        super().__init__("PutUserSocialConnectionDelete", returns=r_PutUserSocialConnectionDelete, userId=userId, networkId=networkId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutUserSocialConnectionDelete:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutUserSocialConnectionDelete]:
        return super().perform_async(retries, delay, **kwargs)

class PutUserUpdatePassword(PostRequest):
    def __init__(self, userUrl: str, oldPassword: str, newPassword: str, **params) -> None:
        super().__init__("PutUserUpdatePassword", returns=r_PutUserUpdatePassword, userUrl=userUrl, oldPassword=oldPassword, newPassword=newPassword, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutUserUpdatePassword:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutUserUpdatePassword]:
        return super().perform_async(retries, delay, **kwargs)

class PutCommentDelete(PostRequest):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentDelete", returns=r_PutCommentDelete, commentId=commentId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutCommentDelete:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutCommentDelete]:
        return super().perform_async(retries, delay, **kwargs)

class PutCommentRestore(PostRequest):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentRestore", returns=r_PutCommentRestore, commentId=commentId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutCommentRestore:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutCommentRestore]:
        return super().perform_async(retries, delay, **kwargs)

class PutThread(PostRequest):
    def __init__(self, forumId: str, name: str, body: str, **params) -> None:
        super().__init__("PutThread", returns=r_PutThread, forumId=forumId, name=name, body=body, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutThread:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutThread]:
        return super().perform_async(retries, delay, **kwargs)

class PutThreadLocked(PostRequest):
    def __init__(self, threadId: str, locked: bool, **params) -> None:
        super().__init__("PutThreadLocked", returns=r_PutThreadLocked, threadId=threadId, locked=locked, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutThreadLocked:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutThreadLocked]:
        return super().perform_async(retries, delay, **kwargs)

class PutThreadSticky(PostRequest):
    def __init__(self, threadId: str, sticky: bool, **params) -> None:
        super().__init__("PutThreadSticky", returns=r_PutThreadSticky, threadId=threadId, sticky=sticky, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutThreadSticky:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutThreadSticky]:
        return super().perform_async(retries, delay, **kwargs)

class PutThreadDelete(PostRequest):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadDelete", returns=r_PutThreadDelete, threadId=threadId, **params)
    
    def perform(self, retries=5, delay=1, **kwargs) -> r_PutThreadDelete:
        return super().perform(retries, delay, **kwargs)
    
    def perform_async(self, retries=5, delay=1, **kwargs) -> Coroutine[Any, Any, r_PutThreadDelete]:
        return super().perform_async(retries, delay, **kwargs)
