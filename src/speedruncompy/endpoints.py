from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunComPy, _log
from .exceptions import SrcpyException
from .enums import *
from .responses import *
import asyncio

SUPPRESS_WARNINGS = False

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

class GetGameLeaderboard2(GetRequest[r_GetGameLeaderboard2], BasePaginatedRequest[r_GetGameLeaderboard2]):
    """The default leaderboard view.
    
    Note that by default runs without video are excluded; provide `video = 0` to include them."""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLeaderboard2", returns=r_GetGameLeaderboard2, _api=_api,
                         page=page, **param_construct)

    def _combine_results(self, pages: dict[int, r_GetGameLeaderboard2]) -> r_GetGameLeaderboard2:
        runList = []
        for p in pages.values():
            runList += p["runList"]
        extras: r_GetGameLeaderboard2 = pages[1]
        extras.pop("runList")
        extras.pagination.page = 0
        return extras | {"runList": runList}

class GetGameLeaderboard(GetRequest[r_GetGameLeaderboard], BasePaginatedRequest[r_GetGameLeaderboard]):
    """WARN: This is NOT the view used by SRC! It may be removed at any time!

    This view is included as it is special & returns a bunch of extra information that may be useful."""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLeaderboard", returns=r_GetGameLeaderboard, _api=_api, page=page, **param_construct)
    
    async def _perform_all_async_raw(self, retries=5, delay=1) -> dict[int, r_GetGameLeaderboard]:
        self.pages: dict[int, r_GetGameLeaderboard] = {}
        self.pages[1] = await self.perform_async(retries, delay, page=1)
        numpages = self.pages[1]["leaderboard"]["pagination"]["pages"]
        if numpages > 1:
            results = await asyncio.gather(*[self.perform_async(retries, delay, page=p) for p in range(2, numpages + 1)])
            self.pages.update({p + 2: result for p, result in enumerate(results)})
        return self.pages

    def _combine_results(self, pages: dict):
        runList = []
        for p in pages.values():
            runList += p["leaderboard"]["runs"]
        extras: Leaderboard = pages[1]["leaderboard"]
        extras.pop("runs")
        extras["pagination"]["page"] = 0
        return r_GetGameLeaderboard({"leaderboard": Leaderboard(extras | {"runs": runList})})

class GetGameData(GetRequest[r_GetGameData]):
    def __init__(self, gameId: str | None = None, gameUrl: str | None = None, **params) -> None:
        if gameId is None and gameUrl is None: raise SrcpyException("GetGameData requires gameId or gameUrl")
        super().__init__("GetGameData", returns=r_GetGameData, gameId=gameId, gameUrl=gameUrl, **params)

class GetGameSummary(GetRequest[r_GetGameSummary]):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameSummary", returns=r_GetGameSummary, gameId=gameId, **params)

class GetGameRecordHistory(GetRequest[r_GetGameRecordHistory]):
    """Get the record history of a category.
    
    #### Other parameters
    - `values[]: list[variableId, valueIds[]]`
    - `emulator: (bool?)` TODO: check
    - `obsolete: bool`"""
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameRecordHistory", returns=r_GetGameRecordHistory, _api=_api, page=page, **param_construct)

class GetSearch(GetRequest[r_GetSearch]):
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

class GetLatestLeaderboard(GetRequest[r_GetLatestLeaderboard]):
    def __init__(self, **params) -> None:
        super().__init__("GetLatestLeaderboard", returns=r_GetLatestLeaderboard, **params)

class GetRun(GetRequest[r_GetRun]):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRun", returns=r_GetRun, runId=runId, **params)

class GetUserPopoverData(GetRequest[r_GetUserPopoverData]):
    def __init__(self, userId, **params) -> None:
        super().__init__("GetUserPopoverData", returns=r_GetUserPopoverData, userId=userId, **params)

class GetArticleList(GetRequest[r_GetArticleList], BasePaginatedRequest[r_GetArticleList]):
    def __init__(self, **params) -> None:
        super().__init__("GetArticleList", returns=r_GetArticleList, **params)

    def _combine_results(self, pages: dict[int, r_GetArticleList]) -> r_GetArticleList:
        if not SUPPRESS_WARNINGS:
            _log.warning("GetArticleList depagination is currently untested, as fewer than 500 pages exist on the site.")
        articleList = []
        for p in pages.values():
            articleList += p["articleList"]
        extras: r_GetArticleList = pages[1]
        extras.pop("articleList")
        extras.pagination.page = 0
        return extras | {"articleList": articleList}

class GetArticle(GetRequest[r_GetArticle]):
    def __init__(self, id: str | None = None, slug: str | None = None, **params) -> None:
        if id is None and slug is None: raise SrcpyException("GetArticle requires id or slug")
        super().__init__("GetArticle", returns=r_GetArticle, id=id, slug=slug, **params)

class GetGameList(GetRequest[r_GetGameList], BasePaginatedRequest[r_GetGameList]):
    def __init__(self, **params) -> None:
        super().__init__("GetGameList", returns=r_GetGameList, **params)
    
    def _combine_results(self, pages: dict[int, r_GetGameList]) -> r_GetGameList:
        gameList = []
        for p in pages.values():
            gameList += p["gameList"]
        extras: r_GetGameList = pages[1]
        extras.pop("gameList")
        extras.pagination.page = 0
        return extras | {"gameList": gameList}

class GetHomeSummary(GetRequest[r_GetHomeSummary]):
    def __init__(self, **params) -> None:
        super().__init__("GetHomeSummary", returns=r_GetHomeSummary, **params)

class GetSeriesList(GetRequest[r_GetSeriesList], BasePaginatedRequest[r_GetSeriesList]):
    def __init__(self, **params) -> None:
        super().__init__("GetSeriesList", returns=r_GetSeriesList, **params)

    def _combine_results(self, pages: dict[int, r_GetSeriesList]) -> r_GetSeriesList:
        seriesList = []
        for p in pages.values():
            seriesList += p["seriesList"]
        extras: r_GetSeriesList = pages[1]
        extras.pop("seriesList")
        extras["pagination"]["page"] = 0
        return extras | {"seriesList": seriesList}

class GetSeriesSummary(GetRequest[r_GetSeriesSummary]):
    def __init__(self, **params) -> None:
        super().__init__("GetSeriesSummary", returns=r_GetSeriesSummary, **params)

class GetGameLevelSummary(GetRequest[r_GetGameLevelSummary]):
    """Note: This can take a `page` param but does not split into pages?"""
    # TODO: check what's going on here
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameLevelSummary", returns=r_GetGameLevelSummary, _api=_api, page=page, **param_construct)

class GetGuideList(GetRequest[r_GetGuideList]):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGuideList", returns=r_GetGuideList, gameId=gameId, **params)

class GetGuide(GetRequest[r_GetGuide]):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetGuide", returns=r_GetGuide, id=id, **params)

class GetNewsList(GetRequest[r_GetNewsList]):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetNewsList", returns=r_GetNewsList, gameId=gameId, **params)

class GetNews(GetRequest[r_GetNews]):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetNews", returns=r_GetNews, id=id, **params)

class GetResourceList(GetRequest[r_GetResourceList]):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetResourceList", returns=r_GetResourceList, gameId=gameId, **params)

class GetStreamList(GetRequest[r_GetStreamList]):
    def __init__(self, **params) -> None:
        super().__init__("GetStreamList", returns=r_GetStreamList, **params)

class GetThreadList(GetRequest[r_GetThreadList]):
    def __init__(self, forumId: str, **params) -> None:
        super().__init__("GetThreadList", returns=r_GetThreadList, forumId=forumId, **params)

class GetChallenge(GetRequest[r_GetChallenge]):
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallenge", returns=r_GetChallenge, id=id, **params)

class GetChallengeLeaderboard(GetRequest[r_GetChallengeLeaderboard], BasePaginatedRequest[r_GetChallengeLeaderboard]):
    def __init__(self, challengeId, **params) -> None:
        super().__init__("GetChallengeLeaderboard", returns=r_GetChallengeLeaderboard, challengeId=challengeId, **params)

class GetChallengeRun(GetRequest[r_GetChallengeRun]):
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallengeRun", returns=r_GetChallengeRun, id=id, **params)

# The below are POSTed by the site, but also accept GET so are placed here to separate from endpoints requiring auth.
class GetUserLeaderboard(GetRequest[r_GetUserLeaderboard]):
    def __init__(self, userId: str, **params) -> None:
        super().__init__("GetUserLeaderboard", returns=r_GetUserLeaderboard, userId=userId, **params)

class GetCommentList(GetRequest[r_GetCommentList], BasePaginatedRequest[r_GetCommentList]):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentList", returns=r_GetCommentList, itemId=itemId, itemType=itemType, **params)
    
    def _combine_results(self, pages: dict[int, r_GetCommentList]) -> r_GetCommentList:
        # TODO: check likeList, userList for page separation
        commentList = []
        for p in pages.values():
            commentList += p["commentList"]
        extras = pages[1]
        extras.pop("commentList")
        return extras | {"commentList": commentList}

class GetThread(GetRequest[r_GetThread], BasePaginatedRequest[r_GetThread]):
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetThread", returns=r_GetThread, id=id, **params)

    def _combine_results(self, pages: dict[int, r_GetThread]) -> r_GetThread:
        commentList = []
        for p in pages.values():
            commentList += p["commentList"]
        extras = pages[1]
        extras.pop("commentList")
        extras["pagination"]["page"] = 0
        return extras | {"commentList": commentList}

class GetForumList(GetRequest[r_GetForumList]):
    def __init__(self, **params) -> None:
        super().__init__("GetForumList", returns=r_GetForumList, **params)


"""
POST requests may require auth
"""

# Session
class PutAuthLogin(PostRequest[r_PutAuthLogin]):
    def __init__(self, name: str, password: str, token: str | None = None, **params) -> None:
        super().__init__("PutAuthLogin", returns=r_PutAuthLogin, name=name, password=password, token=token, **params)

class PutAuthLogout(PostRequest[r_PutAuthLogout]):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthLogout", returns=r_PutAuthLogout, **params)

class PutAuthSignup(PostRequest[r_PutAuthSignup]):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthSignup", returns=r_PutAuthSignup, **params)

class GetSession(PostRequest[r_GetSession]):
    def __init__(self, **params) -> None:
        super().__init__("GetSession", returns=r_GetSession, **params)
    
class PutSessionPing(PostRequest[r_PutSessionPing]):
    def __init__(self, **params) -> None:
        super().__init__("PutSessionPing", returns=r_PutSessionPing, **params)

# Supermod actions
class GetAuditLogList(PostRequest[r_GetAuditLogList], BasePaginatedRequest[r_GetAuditLogList]):
    """WARN: not currently depaginated due to lack of testing availaibility.
    
    To protect against future updates before v1.0, use `._perform_all_raw()`"""
    def __init__(self, gameId: str | None = None, seriesId: str | None = None, eventType: EventType = EventType.NONE, page: int = 1, **params) -> None:
        if gameId is None and seriesId is None: raise SrcpyException("GetAuditLogList requires gameId or seriesId")
        super().__init__("GetAuditLogList", returns=r_GetAuditLogList, gameId=gameId, seriesId=seriesId, eventType=eventType, page=page, **params)
    
    def _combine_results(self, pages: dict):
        # TODO: Method stub
        return super()._combine_results(pages)

# Mod actions
class GetGameSettings(PostRequest[r_GetGameSettings]):
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameSettings", returns=r_GetGameSettings, gameId=gameId, **params)

class PutGameSettings(PostRequest[r_PutGameSettings]):
    def __init__(self, gameId: str, settings: dict, **params) -> None:
        super().__init__("PutGameSettings", returns=r_PutGameSettings, gameId=gameId, settings=settings, **params)

# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

# Run verification
class GetModerationGames(PostRequest[r_GetModerationGames]):
    def __init__(self, **params) -> None:
        super().__init__("GetModerationGames", returns=r_GetModerationGames, **params)

class GetModerationRuns(PostRequest[r_GetModerationRuns], BasePaginatedRequest[r_GetModerationRuns]):
    def __init__(self, gameId: str, limit: int = 100, page: int = 1, **params) -> None:
        super().__init__("GetModerationRuns", returns=r_GetModerationRuns, gameId=gameId, limit=limit, page=page, **params)
    
    def _combine_results(self, pages: dict):
        # TODO: is this all really necessary?
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

        extras: r_GetModerationRuns = pages[1]
        extras.pagination.page = 0
        return extras | r_GetModerationRuns({"categories": categories, "games": games, "levels": levels, "platforms": platforms, "players": players,
                                             "regions": regions, "runs": runs, "users": users, "values": values, "variables": variables},
                                            skipChecking=True)

class PutRunAssignee(PostRequest[r_PutRunAssignee]):
    def __init__(self, assigneeId: str, runId: str, **params) -> None:
        super().__init__("PutRunAssignee", returns=r_PutRunAssignee, assigneeId=assigneeId, runId=runId, **params)

class PutRunVerification(PostRequest[r_PutRunVerification]):
    def __init__(self, runId: str, verified: int, **params) -> None:
        super().__init__("PutRunVerification", returns=r_PutRunVerification, runId=runId, verified=verified, **params)

# Run management
class GetRunSettings(PostRequest[r_GetRunSettings]):
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRunSettings", returns=r_GetRunSettings, runId=runId, **params)

class PutRunSettings(PostRequest[r_PutRunSettings]):
    def __init__(self, csrfToken: str, settings: dict, **params) -> None:
        """Sets a run's settings. Note that the runId is contained in `settings`."""
        super().__init__("PutRunSettings", returns=r_PutRunSettings, csrfToken=csrfToken, settings=settings, **params)

# User inbox actions
class GetConversations(PostRequest[r_GetConversations]):
    def __init__(self, **params) -> None:
        super().__init__("GetConversations", returns=r_GetConversations, **params)

class GetConversationMessages(PostRequest[r_GetConversationMessages]):
    def __init__(self, conversationId, **params) -> None:
        super().__init__("GetConversationMessages", returns=r_GetConversationMessages, conversationId=conversationId, **params)

# User notifications
class GetNotifications(PostRequest[r_GetNotifications], BasePaginatedRequest[r_GetNotifications]):
    def __init__(self, **params) -> None:
        super().__init__("GetNotifications", returns=r_GetNotifications, **params)

    def _combine_results(self, pages: dict[int, r_GetNotifications]) -> r_GetNotifications:
        notifications = []
        for p in pages.values():
            notifications += p["notifications"]
        extras = pages[1]
        extras.pop("notifications")
        extras.pop("pagination")
        return extras | {"notifications": notifications}

# User settings
class GetUserSettings(PostRequest[r_GetUserSettings]):
    """Gets a user's settings. Note that unless you are a site mod, you can only get your own settings."""
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSettings", returns=r_GetUserSettings, userUrl=userUrl, **params)

class PutUserSettings(PostRequest[r_PutUserSettings]):
    def __init__(self, userUrl: str, settings: dict, **params) -> None:
        super().__init__("PutUserSettings", returns=r_PutUserSettings, userUrl=userUrl, settings=settings, **params)

class PutUserUpdateFeaturedRun(PostRequest[r_PutUserUpdateFeaturedRun]):
    def __init__(self, userUrl: str, fullRunId: str | None = None, **params) -> None:
        super().__init__("PutUserUpdateFeaturedRun", returns=r_PutUserUpdateFeaturedRun, userUrl=userUrl, fullRunId=fullRunId, **params)

# Comment Actions
class GetCommentable(PostRequest[r_GetCommentable]):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentable", returns=r_GetCommentable, itemId=itemId, itemType=itemType, **params)

class PutComment(PostRequest[r_PutComment]):
    def __init__(self, itemId: str, itemType: ItemType, text: str, **params) -> None:
        super().__init__("PutComment", returns=r_PutComment, itemId=itemId, itemType=itemType, text=text, **params)

# TODO: test params
class PutCommentableSettings(PostRequest[r_PutCommentableSettings]):
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("PutCommentableSettings", returns=r_PutCommentableSettings, itemId=itemId, itemType=itemType, **params)

# Thread Actions
class GetThreadReadStatus(PostRequest[r_GetThreadReadStatus]):
    """NB: when called without auth will return an empty list"""
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__("GetThreadReadStatus", returns=r_GetThreadReadStatus, threadIds=threadIds, **params)

class PutThreadRead(PostRequest[r_PutThreadRead]):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadRead", returns=r_PutThreadRead, threadId=threadId, **params)

# Forum actions
class GetForumReadStatus(PostRequest[r_GetForumReadStatus]):
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__("GetForumReadStatus", returns=r_GetForumReadStatus, forumIds=forumIds, **params)

# Theme actions
class GetThemeSettings(PostRequest[r_GetThemeSettings]):
    def __init__(self, **params) -> None:
        """Provide either userId or gameId"""
        super().__init__("GetThemeSettings", returns=r_GetThemeSettings, **params)

# To Be Sorted
class GetTickets(PostRequest[r_GetTickets], BasePaginatedRequest[r_GetTickets]):
    """WARN: Not currently depaginated, use _perform_all_raw!"""
    def __init__(self, **params) -> None:
        super().__init__("GetTickets", returns=r_GetTickets, **params)  # TODO: needs param testing
    
    def _combine_results(self, pages: dict):
        """TODO: method stub"""
        return super()._combine_results(pages)

class GetSeriesSettings(PostRequest[r_GetSeriesSettings]):
    def __init__(self, seriesId: str, **params) -> None:
        super().__init__("GetSeriesSettings", returns=r_GetSeriesSettings, seriesId=seriesId, **params)

class GetUserBlocks(PostRequest[r_GetUserBlocks]):
    def __init__(self, **params) -> None:
        super().__init__("GetUserBlocks", returns=r_GetUserBlocks, **params)

class GetUserSupporterData(PostRequest[r_GetUserSupporterData]):
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSupporterData", returns=r_GetUserSupporterData, userUrl=userUrl, **params)

class PutConversation(PostRequest[r_PutConversation]):
    def __init__(self, csrfToken: str, recipientIds: list[str], text: str, **params) -> None:
        super().__init__("PutConversation", returns=r_PutConversation, csrfToken=csrfToken, recipientIds=recipientIds, text=text, **params)

class PutConversationMessage(PostRequest[r_PutConversationMessage]):
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__("PutConversationMessage", returns=r_PutConversationMessage, csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

class PutGame(PostRequest[r_PutGame]):  # TODO: needs param testing
    def __init__(self, name: str, releaseDate: int, gameTypeIds: list[GameType], seriesId: str, **params) -> None:
        super().__init__("PutGame", returns=r_PutGame, name=name, releaseDate=releaseDate, gameTypeIds=gameTypeIds, seriesId=seriesId, **params)

class PutGameBoostGrant(PostRequest[r_PutGameBoostGrant]):  # TODO: test type of `anonymous`
    def __init__(self, gameId: str, anonymous: bool, **params) -> None:
        super().__init__("PutGameBoostGrant", returns=r_PutGameBoostGrant, gameId=gameId, anonymous=anonymous, **params)

class PutGameModerator(PostRequest[r_PutGameModerator]):  # TODO: level enum type
    def __init__(self, gameId: str, userId: str, level: int, **params) -> None:
        super().__init__("PutGameModerator", returns=r_PutGameModerator, gameId=gameId, userId=userId, level=level, **params)

class PutGameModeratorDelete(PostRequest[r_PutGameModeratorDelete]):  # TODO: test `level` necessity & enum type
    def __init__(self, gameId: str, userId: str, level: GamePowerLevel, **params) -> None:
        super().__init__("PutGameModeratorDelete", returns=r_PutGameModeratorDelete, gameId=gameId, userId=userId, level=level, **params)

class PutSeriesGame(PostRequest[r_PutSeriesGame]):  # TODO: reminder on who can do this & what this does lol
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGame", returns=r_PutSeriesGame, seriesId=seriesId, gameId=gameId, **params)

class PutSeriesGameDelete(PostRequest[r_PutSeriesGameDelete]):
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGameDelete", returns=r_PutSeriesGameDelete, seriesId=seriesId, gameId=gameId, **params)

class PutTicket(PostRequest[r_PutTicket]):  # TODO: test parameter types
    def __init__(self, metadata, type, **params) -> None:
        super().__init__("PutTicket", returns=r_PutTicket, metadata=metadata, type=type, **params)

class PutUserSocialConnection(PostRequest[r_PutUserSocialConnection]):
    def __init__(self, userId: str, networkId: NetworkId, value: str, **params) -> None:
        super().__init__("PutUserSocialConnection", returns=r_PutUserSocialConnection, userId=userId, networkId=networkId, value=value, **params)

class PutUserSocialConnectionDelete(PostRequest[r_PutUserSocialConnectionDelete]):
    def __init__(self, userId: str, networkId: NetworkId, **params) -> None:
        super().__init__("PutUserSocialConnectionDelete", returns=r_PutUserSocialConnectionDelete, userId=userId, networkId=networkId, **params)

class PutUserUpdatePassword(PostRequest[r_PutUserUpdatePassword]):
    def __init__(self, userUrl: str, oldPassword: str, newPassword: str, **params) -> None:
        super().__init__("PutUserUpdatePassword", returns=r_PutUserUpdatePassword, userUrl=userUrl, oldPassword=oldPassword, newPassword=newPassword, **params)

class PutCommentDelete(PostRequest[r_PutCommentDelete]):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentDelete", returns=r_PutCommentDelete, commentId=commentId, **params)

class PutCommentRestore(PostRequest[r_PutCommentRestore]):
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentRestore", returns=r_PutCommentRestore, commentId=commentId, **params)

class PutThread(PostRequest[r_PutThread]):
    def __init__(self, forumId: str, name: str, body: str, **params) -> None:
        super().__init__("PutThread", returns=r_PutThread, forumId=forumId, name=name, body=body, **params)

class PutThreadLocked(PostRequest[r_PutThreadLocked]):
    def __init__(self, threadId: str, locked: bool, **params) -> None:
        super().__init__("PutThreadLocked", returns=r_PutThreadLocked, threadId=threadId, locked=locked, **params)

class PutThreadSticky(PostRequest[r_PutThreadSticky]):
    def __init__(self, threadId: str, sticky: bool, **params) -> None:
        super().__init__("PutThreadSticky", returns=r_PutThreadSticky, threadId=threadId, sticky=sticky, **params)

class PutThreadDelete(PostRequest[r_PutThreadDelete]):
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadDelete", returns=r_PutThreadDelete, threadId=threadId, **params)
