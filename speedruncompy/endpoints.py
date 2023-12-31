from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunComPy, _log
from .exceptions import SrcpyException
from .enums import *

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
        super().__init__("GetGameLeaderboard2", _api=_api, page=page, **param_construct)

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["runList"]
        extras: dict = pages[1]
        extras.pop("runList")
        extras.pop("pagination")
        return {"runList": runList} | extras

class GetGameLeaderboard(GetRequest, BasePaginatedRequest):
    """WARN: This is NOT the view used by SRC! It may be removed at any time!

    This view is included as it is special & returns a bunch of extra information that may be useful."""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLeaderboard", _api=_api, page=page, **param_construct)

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["runs"]
        extras: dict = pages[1]
        extras.pop("runs")
        extras.pop("pagination")
        return {"runs": runList} | extras

class GetGameData(GetRequest):
    def __init__(self, gameId: str = None, gameUrl: str = None, **params) -> None:
        if gameId is None and gameUrl is None: raise SrcpyException("GetGameData requires gameId or gameUrl")
        super().__init__("GetGameData", gameId=gameId, gameUrl=gameUrl, **params)

class GetGameSummary(GetRequest):
    def __init__(self, gameId:str, **params) -> None:
        super().__init__("GetGameSummary", gameId=gameId, **params)

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
        super().__init__("GetGameRecordHistory", _api=_api, page=page, **param_construct)

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
        super().__init__("GetSearch", query=query, **params)

class GetLatestLeaderboard(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetLatestLeaderboard", **params)

class GetRun(GetRequest):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRun", runId=runId, **params)

class GetUserPopoverData(GetRequest):
    def __init__(self, userId, **params) -> None:
        super().__init__("GetUserPopoverData", userId=userId, **params)

class GetArticleList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetArticleList", **params)

    def _combine_results(self, pages: dict):
        """WARN: untested as currently fewer than 500 pages exist on the site"""
        if not SUPPRESS_WARNINGS:
            _log.warning("GetArticleList depagination is currently untested, as fewer than 500 pages exist on the site.")
        articleList = []
        for p in pages.values():
            articleList += p["articleList"]
        extras: dict = pages[1]
        extras.pop("articleList")
        extras.pop("pagination")
        return {"articleList": articleList} | extras

class GetArticle(GetRequest):
    def __init__(self, id = None, slug = None, **params) -> None:
        if id is None and slug is None: raise SrcpyException("GetArticle requires id or slug")
        super().__init__("GetArticle", id=id, slug=slug, **params)

class GetGameList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetGameList", **params)
    
    def _combine_results(self, pages: dict):
        gameList = []
        for p in pages.values():
            gameList += p["gameList"]
        extras: dict = pages[1]
        extras.pop("gameList")
        extras.pop("pagination")
        return {"gameList": gameList} | extras

class GetHomeSummary(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetHomeSummary", **params)

class GetSeriesList(GetRequest, BasePaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetSeriesList", **params)

    def _combine_results(self, pages: dict):
        seriesList = []
        for p in pages.values():
            seriesList += p["seriesList"]
        extras: dict = pages[1]
        extras.pop("seriesList")
        extras.pop("pagination")
        return {"seriesList": seriesList} | extras

class GetGameLevelSummary(GetRequest, BasePaginatedRequest):
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameRecordHistory", _api=_api, page=page, **param_construct)

class GetGuideList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGuideList", gameId=gameId, **params)

class GetGuide(GetRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetGuide", id=id, **params)

class GetNewsList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetNewsList", gameId=gameId, **params)

class GetNews(GetRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetNews", id=id, **params)

class GetResourceList(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetResourceList", gameId=gameId, **params)

class GetStreamList(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetStreamList", **params)

class GetThreadList(GetRequest):
    def __init__(self, forumId: str, **params) -> None:
        super().__init__("GetThreadList", forumId=forumId, **params)

# The below are POSTed by the site, but also accept GET so are placed here to separate from endpoints requiring auth.
class GetUserLeaderboard(GetRequest):
    def __init__(self, userId: str, **params) -> None:
        super().__init__("GetUserLeaderboard", userId=userId, **params)

class GetCommentList(GetRequest, BasePaginatedRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentList", itemId=itemId, itemType=itemType, **params)

class GetThread(GetRequest , BasePaginatedRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetThread", id=id, **params)

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
        super().__init__("GetForumList", **params)

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