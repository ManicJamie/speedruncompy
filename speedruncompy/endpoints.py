from tkinter import PAGES
from .api import GetPaginatedRequest, GetRequest, PostPaginatedRequest, PostRequest
from .exceptions import SrcpyException
from .enums import *

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

class GetGameLeaderboard2(GetPaginatedRequest):
    def __init__(self, gameId: str, categoryId: str, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        if page is not None: 
            param_construct["page"] = page
        super().__init__("GetGameLeaderboard2", **param_construct)

class GetGameData(GetRequest):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameData", gameId=gameId, **params)

class GetGameRecordHistory(GetPaginatedRequest):
    """This takes a page field, but does not return a pagination object, and does not appear to be paginated."""
    def __init__(self, gameId: str, categoryId: str, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        if page is not None: 
            param_construct["page"] = page
        super().__init__("GetGameRecordHistory", **param_construct)

class GetSearch(GetRequest):
    def __init__(self, query: str, **params) -> None:
        super().__init__("GetSearch", query=query, **params)

class GetLatestLeaderboard(GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetLatestLeaderboard", **params)

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
class GetAuditLogList(PostRequest):
    def __init__(self, gameId: str = None, seriesId: str = None, eventType: eventType = eventType.NONE, page: int = 1, **params) -> None:
        if gameId is None and seriesId is None: raise SrcpyException("GetAuditLogList requires gameId or seriesId")
        super().__init__("GetAuditLogList", gameId=gameId, eventType=eventType, page=page, **params)

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

class GetModerationRuns(PostPaginatedRequest):
    def __init__(self, gameId: str, limit: int = 100, page: int = 1, **params) -> None:
        super().__init__("GetModerationRuns", gameId=gameId, limit=limit, page=page, **params)

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
class GetNotifications(PostPaginatedRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetNotifications", **params)

# User settings
class GetUserSettings(PostRequest):
    """Gets a user's settings. Note that unless you are a site mod, you can only get your own settings."""
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSettings", userUrl=userUrl, **params)

class PutUserSettings(PostRequest):
    def __init__(self, userUrl: str, settings: dict, **params) -> None:
        super().__init__("PutUserSettings", userUrl=userUrl, settings=settings, **params)

# Comment Actions
class GetCommentList(PostRequest):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentList", itemId=itemId, itemType=itemType, **params)

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
class GetThread(PostPaginatedRequest):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetThread", id=id, **params)

class GetThreadReadStatus(PostRequest):
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__("GetThreadReadStatus", threadIds=threadIds, **params)

class PutThreadRead(PostRequest):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadRead", threadId=threadId, **params)

# Forum actions
class GetForumList(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetForumList", **params)

class GetForumReadStatus(PostRequest):
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__("GetForumReadStatus", forumIds=forumIds, **params)

# Theme actions
class GetThemeSettings(PostRequest):
    def __init__(self, **params) -> None:
        """Provide either userId or gameId"""
        super().__init__("GetThemeSettings", **params)