from .api import BasePaginatedRequest, GetRequest, PostRequest, SpeedrunComPy
from .enums import *
from .responses import *
import asyncio

SUPPRESS_WARNINGS = False

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

class GetGameLeaderboard2(GetRequest[r_GetGameLeaderboard2], BasePaginatedRequest[r_GetGameLeaderboard2]):
    """The default leaderboard view.
    
    ### Mandatory:
    @gameId
    @categoryId
    @levelId: If `categoryId` refers to a level category.

    ### Optional:
    TODO

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
    """A secondary leaderboard view. WARNING: Not used on the site, may be removed at any time!

    ### Mandatory:
    - @gameId
    - @categoryId
    - @levelId: If `categoryId` refers to a level category.

    ### Optional:
    TODO
    """
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
    """ TODO
    
    ### Mandatory:
    #### One of:
    - @gameId
    - @gameUrl
    """
    def __init__(self, gameId: str | None = None, gameUrl: str | None = None, **params) -> None:
        super().__init__("GetGameData", returns=r_GetGameData, gameId=gameId, gameUrl=gameUrl, **params)

class GetGameSummary(GetRequest[r_GetGameSummary]):
    """ TODO
    
    ### Mandatory:
    #### One of:
    - @gameId
    - @gameUrl
    """
    def __init__(self, gameId: str | None = None, gameUrl: str | None = None, **params) -> None:
        super().__init__("GetGameSummary", returns=r_GetGameSummary, gameId=gameId, gameUrl=gameUrl, **params)

class GetGameRecordHistory(GetRequest[r_GetGameRecordHistory]):
    """Get the record history of a category.
    
    ### Mandatory:
    - @gameId
    - @categoryId

    ### Other:
    - @values: A list of VariableValues
    - @emulator: EmulatorFilter
    - @obsolete: ObsoleteFilter
    """
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        super().__init__("GetGameRecordHistory", returns=r_GetGameRecordHistory, _api=_api, page=page, **param_construct)

class GetSearch(GetRequest[r_GetSearch]):
    """Search for an object based on its name. May include multiple types to search for at once.

    ### Optional:
    - @limit: <= 500 = 500
    - @includeGames
    - @includeNews
    - @includePages
    - @includeSeries
    - @includeUsers
    - @includeChallenges
    """
    def __init__(self, query: str, **params) -> None:
        super().__init__("GetSearch", returns=r_GetSearch, query=query, **params)

class GetLatestLeaderboard(GetRequest[r_GetLatestLeaderboard]):
    """Gets most recent runs.

    ### Optional:
    - @gameId
    - @seriesId
    - @limit: <= 999 = 10
    """
    def __init__(self, **params) -> None:
        super().__init__("GetLatestLeaderboard", returns=r_GetLatestLeaderboard, **params)

class GetRun(GetRequest[r_GetRun]):
    """Gets all parameters pertinent to displaying a single run.
    
    ### Mandatory:
    - @runId
    """
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRun", returns=r_GetRun, runId=runId, **params)

class GetUserPopoverData(GetRequest[r_GetUserPopoverData]):
    """Gets data for user popovers. Includes `userSocialConnectionList`, `userStats` & `titleList`.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId, **params) -> None:
        super().__init__("GetUserPopoverData", returns=r_GetUserPopoverData, userId=userId, **params)

class GetTitleList(GetRequest[r_GetTitleList]):
    """Gets a list of all titles available on the site.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetTitleList", returns=r_GetTitleList, **params)

class GetTitle(GetRequest[r_GetTitle]):
    """Gets a specific title.
    
    ### Mandatory:
    - @titleId
    """
    def __init__(self, titleId, **params) -> None:
        super().__init__("GetTitle", returns=r_GetTitle, titleId=titleId, **params)

class GetArticleList(GetRequest[r_GetArticleList], BasePaginatedRequest[r_GetArticleList]):
    """Gets a list of articles on the site.
    
    ### Optional:
    - @limit: <= 500 = 500. Number of elements per page.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetArticleList", returns=r_GetArticleList, **params)

    def _combine_results(self, pages: dict[int, r_GetArticleList]) -> r_GetArticleList:
        articleList: list[Article] = []
        gameDict: dict[str, Game] = {}
        userDict: dict[str, User] = {}
        for p in pages.values():
            articleList += p["articleList"]
            gameDict |= {x["id"]: x for x in p["gameList"]}
            userDict |= {x["id"]: x for x in p["userList"]}
        extras: r_GetArticleList = pages[1]
        extras.pop("articleList")
        extras.pop("gameList")
        extras.pop("userList")
        extras.pagination.page = 0
        return extras | {"articleList": articleList, "gameList": list(gameDict.values()), "userList": list(userDict.values())}

class GetArticle(GetRequest[r_GetArticle]):
    """Gets a specific article from the site.
    
    ### Mandatory:
    #### One of:
    - @id
    - @slug
    """
    def __init__(self, id: str | None = None, slug: str | None = None, **params) -> None:
        super().__init__("GetArticle", returns=r_GetArticle, id=id, slug=slug, **params)

class GetGameList(GetRequest[r_GetGameList], BasePaginatedRequest[r_GetGameList]):
    """Gets a list of all games on the site.
    
    ### Optional:
    - @limit: <= 200 = 500 (!)"""
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
    """Gets information for the home page. Often empty.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetHomeSummary", returns=r_GetHomeSummary, **params)

class GetSeriesList(GetRequest[r_GetSeriesList], BasePaginatedRequest[r_GetSeriesList]):
    """Gets a list of series on the site.

    ### Optional:
    - @limit: <= 500 = 500
    """
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
    """Gets most information pertinent to a series.
    
    ### Mandatory:
    #### One of:
    - @seriesId
    - @seriesUrl
    """
    def __init__(self, seriesId: str | None = None, seriesUrl: str | None = None, **params) -> None:
        super().__init__("GetSeriesSummary", returns=r_GetSeriesSummary, seriesId=seriesId, seriesUrl=seriesUrl, **params)

class GetGameLevelSummary(GetRequest[r_GetGameLevelSummary]):
    """Note: This can take a `page` param but does not split into pages?"""
    # TODO: check what's going on here
    def __init__(self, gameId: str, categoryId: str, _api: SpeedrunComPy | None = None, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId} | params}
        super().__init__("GetGameLevelSummary", returns=r_GetGameLevelSummary, _api=_api, page=page, **param_construct)

class GetGuideList(GetRequest[r_GetGuideList]):
    """Gets all guides on a game.

    ### Mandatory
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGuideList", returns=r_GetGuideList, gameId=gameId, **params)

class GetGuide(GetRequest[r_GetGuide]):
    """Get a specific guide by id.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetGuide", returns=r_GetGuide, id=id, **params)

class GetNewsList(GetRequest[r_GetNewsList]):
    """Get a list of game news articles.
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetNewsList", returns=r_GetNewsList, gameId=gameId, **params)

class GetNews(GetRequest[r_GetNews]):
    """Get a game news article.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id: str, **params) -> None:
        super().__init__("GetNews", returns=r_GetNews, id=id, **params)

class GetResourceList(GetRequest[r_GetResourceList]):
    """Get a list of a game's resources.
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetResourceList", returns=r_GetResourceList, gameId=gameId, **params)

class GetStreamList(GetRequest[r_GetStreamList]):
    """TODO: documentation
    """
    def __init__(self, **params) -> None:
        super().__init__("GetStreamList", returns=r_GetStreamList, **params)

class GetThreadList(GetRequest[r_GetThreadList]):
    """Get threads on a forum.
    
    ### Mandatory:
    - @forumId
    """
    def __init__(self, forumId: str, **params) -> None:
        super().__init__("GetThreadList", returns=r_GetThreadList, forumId=forumId, **params)

class GetChallenge(GetRequest[r_GetChallenge]):
    """Get a specific Challenge.
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallenge", returns=r_GetChallenge, id=id, **params)

class GetChallengeLeaderboard(GetRequest[r_GetChallengeLeaderboard], BasePaginatedRequest[r_GetChallengeLeaderboard]):
    """Get runs from a Challenge board.

    ### Mandatory:
    - @challengeId
    """
    def __init__(self, challengeId, **params) -> None:
        super().__init__("GetChallengeLeaderboard", returns=r_GetChallengeLeaderboard, challengeId=challengeId, **params)

class GetChallengeGlobalRankingList(GetRequest[r_GetChallengeGlobalRankingList]):
    """Get a sitewide leaderboard for users who have won the most in Challenges.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetChallengeGlobalRankingList", returns=r_GetChallengeGlobalRankingList, **params)

class GetChallengeRun(GetRequest[r_GetChallengeRun]):
    """Get a specific Challenge run (not the same as a normal run!)
    
    ### Mandatory:
    - @id
    """
    def __init__(self, id, **params) -> None:
        super().__init__("GetChallengeRun", returns=r_GetChallengeRun, id=id, **params)

# The below are POSTed by the site, but also accept GET so are placed here to separate from endpoints requiring auth.
class GetUserLeaderboard(GetRequest[r_GetUserLeaderboard]):
    """Get a user's runs for display on their profile.
    
    ### Mandatory:
    - @userId
    """
    def __init__(self, userId: str, **params) -> None:
        super().__init__("GetUserLeaderboard", returns=r_GetUserLeaderboard, userId=userId, **params)

class GetCommentList(GetRequest[r_GetCommentList], BasePaginatedRequest[r_GetCommentList]):
    """Get a list of comments on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType: ItemType of the above `itemId`
    """
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
    """Get a specific thread.
    
    ### Mandatory:
    - @id
    """
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
    """Get a list of site-wide forums. When logged in, may include forums of followed games.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetForumList", returns=r_GetForumList, **params)


"""
POST requests may require auth
"""

# Session
class PutAuthLogin(PostRequest[r_PutAuthLogin]):
    """Logs in. If 2FA is enabled, first provide `name` & `password`, then check `tokenChallengeSent` and repeat w/ token.
    Provide `_api` to authorise a specific API instance, otherwise the default instance will be used.
    
    ### Mandatory:
    - @name
    - @password
    - @token: On second attempt if 2FA is enabled.
    """
    def __init__(self, name: str, password: str, token: str | None = None, **params) -> None:
        super().__init__("PutAuthLogin", returns=r_PutAuthLogin, name=name, password=password, token=token, **params)

class PutAuthLogout(PostRequest[r_Empty]):
    """Logs out.
    Provide `_api` to log out a specific API instance, otherwise the default instance will be used.
    """
    def __init__(self, **params) -> None:
        super().__init__("PutAuthLogout", returns=r_Empty, **params)

class PutAuthSignup(PostRequest[r_PutAuthSignup]):
    """Creates & logs in to a new account.
    
    Parameters undocumented.
    """
    def __init__(self, **params) -> None:
        super().__init__("PutAuthSignup", returns=r_PutAuthSignup, **params)

class GetSession(PostRequest[r_GetSession]):
    """Gets information about the current user's session.
    Includes `csrfToken`, required for some endpoints.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetSession", returns=r_GetSession, **params)
    
class PutSessionPing(PostRequest[r_PutSessionPing]):
    """Tells SRC to renew your session. Some other endpoints will renew your session.
    May be required to keep your session alive without re-login.
    """
    def __init__(self, **params) -> None:
        super().__init__("PutSessionPing", returns=r_PutSessionPing, **params)

# Supermod actions
class GetAuditLogList(PostRequest[r_GetAuditLogList], BasePaginatedRequest[r_GetAuditLogList]):
    """Gets a game, series or user's audit log.
    WARN: not currently depaginated due to lack of testing availability.
    
    ### Mandatory:
    - @eventType: Type to filter by (default "")
    - @page
    #### One of:
    - @gameId
    - @seriesId
    - @userId: Every change that has happened to this user
    - @actorId: Every change this user has made (Admin only)
    """
    def __init__(self, gameId: str | None = None, seriesId: str | None = None, userId: str | None = None, actorId: str | None = None,
                 eventType: EventType = EventType.NONE, page: int = 1, **params) -> None:
        super().__init__("GetAuditLogList", returns=r_GetAuditLogList, gameId=gameId, seriesId=seriesId,
                         userId=userId, actorId=actorId, eventType=eventType, page=page, **params)
    
    def _combine_results(self, pages: dict):
        # TODO: Method stub
        return super()._combine_results(pages)

# Mod actions
class GetGameSettings(PostRequest[r_GetGameSettings]):
    """Get a game's settings. Must be at least a verifier(?) on the game. #  TODO: check
    
    ### Mandatory:
    - @gameId
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetGameSettings", returns=r_GetGameSettings, gameId=gameId, **params)

class PutGameSettings(PostRequest[r_PutGameSettings]):
    """Set a game's settings. Must be at least a moderator on the game.

    ### Mandatory:
    - @gameId: Must be provided even though `settings` contains `id`.
    - @settings
    """
    def __init__(self, gameId: str, settings: GameSettings, **params) -> None:
        super().__init__("PutGameSettings", returns=r_PutGameSettings, gameId=gameId, settings=settings, **params)

class PutVariable(PostRequest[r_Empty]):
    """Add a new variable to a game. TODO: check if values / defaultValue are required.
    
    ### Mandatory:
    - @gameId
    - @variable: Constructed `Variable` object. `defaultValue` must be equal to the id on `values`
    - @values: List of constructed `Value` objects. One of these `id`s must match `defaultValue`"""
    def __init__(self, gameId: str, variable: Variable, values: list[Value], **params) -> None:
        super().__init__("PutVariable", returns=r_Empty, gameId=gameId, variable=variable, values=values, **params)

class PutVariableUpdate(PostRequest[r_Empty]):
    """Add a new variable to a game. TODO: check if values / defaultValue are required.
    
    ### Mandatory:
    - @gameId
    - @variableId: ID of the variable to be replaced
    - @variable: Constructed `Variable` object.
    - @values: List of constructed `Value` objects."""
    def __init__(self, gameId: str, variableId: str, variable: Variable, values: list[Value], **params) -> None:
        super().__init__("PutVariable", returns=r_Empty, gameId=gameId, variableId=variableId, variable=variable, values=values, **params)

class PutVariableApplyDefault(PostRequest[r_Ok]):
    """Set the default value on a variable.
    
    ### Mandatory:
    - @gameId
    - @variableId
    """
    def __init__(self, gameId: str, variableId: str, **params) -> None:
        super().__init__("PutVariable", returns=r_Ok, gameId=gameId, variableId=variableId, **params)

# Run verification
class GetModerationGames(PostRequest[r_GetModerationGames]):
    """Get moderation games & stats for the logged in user.
        WARN: does not error when not logged in, instead the response fields will be None.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetModerationGames", returns=r_GetModerationGames, **params)

class GetModerationRuns(PostRequest[r_GetModerationRuns], BasePaginatedRequest[r_GetModerationRuns]):
    """Get data for runs waiting in the moderation queue for a game.

    ### Mandatory:
    - @gameId

    ### Optional:
    - @limit:
    """
    def __init__(self, gameId: str, **params) -> None:
        super().__init__("GetModerationRuns", returns=r_GetModerationRuns, gameId=gameId, **params)
    
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
    """Assigns a verifier to a run."""
    def __init__(self, assigneeId: str, runId: str, **params) -> None:
        super().__init__("PutRunAssignee", returns=r_PutRunAssignee, assigneeId=assigneeId, runId=runId, **params)

class PutRunVerification(PostRequest[r_PutRunVerification]):
    """Assigns a verification level `Verified` to a run.
    
    ### Mandatory:
    - @runId
    - @verified: `Verified.PENDING`, `Verified.VERIFIED`, `Verified.REJECTED`
    """
    def __init__(self, runId: str, verified: Verified, **params) -> None:
        super().__init__("PutRunVerification", returns=r_PutRunVerification, runId=runId, verified=verified, **params)

# Run management
class GetRunSettings(PostRequest[r_GetRunSettings]):
    """Gets a run's settings
    """
    def __init__(self, runId: str, **params) -> None:
        super().__init__("GetRunSettings", returns=r_GetRunSettings, runId=runId, **params)

class PutRunSettings(PostRequest[r_PutRunSettings]):
    """Sets a run's settings OR submit a new run if `settings.runId` is None.
    
    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @settings: Existing run settings if `runId is not None`, otherwise new run's settings.
    """
    def __init__(self, csrfToken: str, settings: RunSettings, **params) -> None:
        """Sets a run's settings. Note that the runId is contained in `settings`."""
        super().__init__("PutRunSettings", returns=r_PutRunSettings, csrfToken=csrfToken, settings=settings, **params)

# User inbox actions
class GetConversations(PostRequest[r_GetConversations]):
    """Gets conversations the user is involved in.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetConversations", returns=r_GetConversations, **params)

class GetConversationMessages(PostRequest[r_GetConversationMessages]):
    """Gets messages from a given conversation.
    
    ### Mandatory:
    - @conversationId
    """
    def __init__(self, conversationId, **params) -> None:
        super().__init__("GetConversationMessages", returns=r_GetConversationMessages, conversationId=conversationId, **params)

class PutConversation(PostRequest[r_PutConversation]):
    """Creates a new conversation. May include several users.
    
    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @recipientIds: A list of other users to add to the conversation.
    - @text: Content of the initial message. (?) #  TODO: check it's not a title.
    """
    def __init__(self, csrfToken: str, recipientIds: list[str], text: str, **params) -> None:
        super().__init__("PutConversation", returns=r_PutConversation, csrfToken=csrfToken, recipientIds=recipientIds, text=text, **params)

class PutConversationMessage(PostRequest[r_PutConversationMessage]):
    """Sends a message to a conversation.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    - @text
    """
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__("PutConversationMessage", returns=r_PutConversationMessage, csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

class PutConversationLeave(PostRequest[Datatype]):  # TODO: document response
    """Leaves a conversation. # TODO: check when this can be done.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    """
    def __init__(self, csrfToken: str, conversationId: str, **params) -> None:
        super().__init__("PutConversationLeave", returns=Datatype, csrfToken=csrfToken, conversationId=conversationId, **params)

class PutConversationReport(PostRequest[Datatype]):  # TODO: document response
    """Reports a conversation.

    ### Mandatory:
    - @csrfToken: May be retrieved by `GetSession`.
    - @conversationId
    - @text: Content of the report (?)  # TODO: Document
    """
    def __init__(self, csrfToken: str, conversationId: str, text: str, **params) -> None:
        super().__init__("PutConversationReport", returns=Datatype, csrfToken=csrfToken, conversationId=conversationId, text=text, **params)

# User notifications
class GetNotifications(PostRequest[r_GetNotifications], BasePaginatedRequest[r_GetNotifications]):
    """Gets the user's notifications.
    """
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
    """Gets a user's settings.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are a site moderator.
    """
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSettings", returns=r_GetUserSettings, userUrl=userUrl, **params)

class PutUserSettings(PostRequest[r_PutUserSettings]):
    """Sets a user's settings.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are a site moderator.
    - @settings
    """
    def __init__(self, userUrl: str, settings: UserSettings, **params) -> None:
        super().__init__("PutUserSettings", returns=r_PutUserSettings, userUrl=userUrl, settings=settings, **params)

class PutUserUpdateFeaturedRun(PostRequest[r_PutUserUpdateFeaturedRun]):
    """Sets the run featured on a user's profile.
    
    ### Mandatory:
    - @userUrl: must be your own unless you are a site moderator.
    - @fullRunId: If omitted, clears the featured run.
    """
    def __init__(self, userUrl: str, fullRunId: str | None = None, **params) -> None:  # TODO: check if levelId is different
        super().__init__("PutUserUpdateFeaturedRun", returns=r_PutUserUpdateFeaturedRun, userUrl=userUrl, fullRunId=fullRunId, **params)

# Comment Actions
class GetCommentable(PostRequest[r_GetCommentable]):
    """Checks the comment permissions on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType
    """
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("GetCommentable", returns=r_GetCommentable, itemId=itemId, itemType=itemType, **params)

class PutComment(PostRequest[r_PutComment]):
    """Posts a comment on an item.
    
    ### Mandatory:
    - @itemId
    - @itemType
    - @text
    """
    def __init__(self, itemId: str, itemType: ItemType, text: str, **params) -> None:
        super().__init__("PutComment", returns=r_PutComment, itemId=itemId, itemType=itemType, text=text, **params)

class PutCommentableSettings(PostRequest[r_PutCommentableSettings]):
    """Updates commentable settings on an item.

    ### Mandatory:
    - @itemId
    - @itemType
    - other # TODO
    """
    def __init__(self, itemId: str, itemType: int, **params) -> None:
        super().__init__("PutCommentableSettings", returns=r_PutCommentableSettings, itemId=itemId, itemType=itemType, **params)

# Thread Actions
class GetThreadReadStatus(PostRequest[r_GetThreadReadStatus]):
    """Gets whether a set of threads have been read by the user.
    
    ### Mandatory:
    - @threadIds: list of IDs
    """
    def __init__(self, threadIds: list[str], **params) -> None:
        super().__init__("GetThreadReadStatus", returns=r_GetThreadReadStatus, threadIds=threadIds, **params)

class PutThreadRead(PostRequest[r_PutThreadRead]):
    """Sets a thread as read by the user.

    ### Mandatory:
    - @threadId
    """
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadRead", returns=r_PutThreadRead, threadId=threadId, **params)

# Forum actions
class GetForumReadStatus(PostRequest[r_GetForumReadStatus]):
    """Gets whether a set of forums have been read by the user.

    ### Mandatory:
    - @forumIds: list of IDs
    """
    def __init__(self, forumIds: list[str], **params) -> None:
        super().__init__("GetForumReadStatus", returns=r_GetForumReadStatus, forumIds=forumIds, **params)

# Theme actions
class GetThemeSettings(PostRequest[r_GetThemeSettings]):
    """Gets a user, game or series' theme.  # TODO: check noargs & series

    ### Mandatory:
    #### One of:
    - @userId
    - @gameId
    - @seriesId
    """
    def __init__(self, **params) -> None:
        super().__init__("GetThemeSettings", returns=r_GetThemeSettings, **params)

# To Be Sorted
class PutAdvertiseContact(PostRequest[r_Empty]):
    """Sends a request for contact to SRC for collaboration.
    
    ### Mandatory:
    - @name
    - @company
    - @email
    - @message
    """
    def __init__(self, name: str, company: str, email: str, message: str, **params) -> None:
        super().__init__("PutAdvertiseContact", returns=r_Empty,
                         name=name, company=company, email=email, message=message, **params)

class GetTickets(PostRequest[r_GetTickets], BasePaginatedRequest[r_GetTickets]):
    """Gets tickets submitted by the user.
    """
    def __init__(self, **params) -> None:
        super().__init__("GetTickets", returns=r_GetTickets, **params)  # TODO: needs param testing
    
    def _combine_results(self, pages: dict):
        """TODO: method stub"""
        return super()._combine_results(pages)

class GetSeriesSettings(PostRequest[r_GetSeriesSettings]):
    """Gets settings of a series.

    ### Mandatory:
    - @seriesId
    """
    def __init__(self, seriesId: str, **params) -> None:
        super().__init__("GetSeriesSettings", returns=r_GetSeriesSettings, seriesId=seriesId, **params)

class GetUserBlocks(PostRequest[r_GetUserBlocks]):
    """Gets blocks relevant to a user. # TODO: check blockee/blocker
    """
    def __init__(self, **params) -> None:
        super().__init__("GetUserBlocks", returns=r_GetUserBlocks, **params)

class GetUserSupporterData(PostRequest[r_GetUserSupporterData]):
    """Gets supporter data for a user. # TODO: check auth

    ### Mandatory:
    - @userUrl
    """
    def __init__(self, userUrl: str, **params) -> None:
        super().__init__("GetUserSupporterData", returns=r_GetUserSupporterData, userUrl=userUrl, **params)

class PutGame(PostRequest[r_PutGame]):  # TODO: needs param testing
    """Add a new game.

    ### Mandatory:
    - @name
    - @releaseDate
    - @gameTypeIds
    #### Optional:
    - @seriesId
    """
    def __init__(self, name: str, releaseDate: int, gameTypeIds: list[GameType], seriesId: str, **params) -> None:
        super().__init__("PutGame", returns=r_PutGame, name=name, releaseDate=releaseDate, gameTypeIds=gameTypeIds, seriesId=seriesId, **params)

class PutGameBoostGrant(PostRequest[r_PutGameBoostGrant]):  # TODO: test type of `anonymous`
    """TODO
    
    ### Mandatory:
    - @gameId
    - @anonymous
    """
    def __init__(self, gameId: str, anonymous: bool, **params) -> None:
        super().__init__("PutGameBoostGrant", returns=r_PutGameBoostGrant, gameId=gameId, anonymous=anonymous, **params)

class PutGameModerator(PostRequest[r_PutGameModerator]):
    """Add a moderator to a game.
    
    ### Mandatory:
    - @gameId
    - @userId
    - @level: GamePowerLevel (-1 = verifier, 0 = mod, 1 = supermod)
    """
    def __init__(self, gameId: str, userId: str, level: GamePowerLevel, **params) -> None:
        super().__init__("PutGameModerator", returns=r_PutGameModerator, gameId=gameId, userId=userId, level=level, **params)

class PutGameModeratorDelete(PostRequest[r_PutGameModeratorDelete]):  # TODO: test `level` necessity & enum type
    """Remove a moderator from a game.
    
    ### Mandatory:
    - @gameId
    - @userId
    - @level: TODO check necessity
    """
    def __init__(self, gameId: str, userId: str, level: GamePowerLevel, **params) -> None:
        super().__init__("PutGameModeratorDelete", returns=r_PutGameModeratorDelete, gameId=gameId, userId=userId, level=level, **params)

class PutSeriesGame(PostRequest[r_PutSeriesGame]):
    """Add an existing game to a series.
    
    ### Mandatory:
    - @seriesId
    - @gameId
    """
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGame", returns=r_PutSeriesGame, seriesId=seriesId, gameId=gameId, **params)

class PutSeriesGameDelete(PostRequest[r_PutSeriesGameDelete]):
    """Remove a game from a series. Does not delete the game.
    
    ### Mandatory:
    - @seriesId
    - @gameId
    """
    def __init__(self, seriesId: str, gameId: str, **params) -> None:
        super().__init__("PutSeriesGameDelete", returns=r_PutSeriesGameDelete, seriesId=seriesId, gameId=gameId, **params)

class PutTicket(PostRequest[r_PutTicket]):
    """Submits support tickets.

    ### Mandatory:
    - @metadata: a JSON string of ticket data
    - @type: TicketType # TODO: check TicketType vs TicketQueue Type
    """
    def __init__(self, metadata: str, type: TicketType, **params) -> None:
        super().__init__("PutTicket", returns=r_PutTicket, metadata=metadata, type=type, **params)

class PutTicketNote(PostRequest[r_Ok]):
    """Adds a note/message to a ticket. When `isMessage` is `false`, only admins can post or read the note.
    
    ### Mandatory:
    - @ticketId
    - @note
    - @isMessage: whether the note is a message to the user. `False` only permitted for admins.
    """
    def __init__(self, ticketId: str, note: str, isMessage: bool, **params) -> None:
        super().__init__("PutTicketNote", returns=r_Ok, ticketId=ticketId, note=note, isMessage=isMessage, **params)

class PutUserSocialConnection(PostRequest[r_PutUserSocialConnection]):  # TODO: verification?
    """Modifies a user's social connection.

    ### Mandatory:
    - @userId
    - @networkId: see `NetworkId`
    - @value
    """
    def __init__(self, userId: str, networkId: NetworkId, value: str, **params) -> None:
        super().__init__("PutUserSocialConnection", returns=r_PutUserSocialConnection, userId=userId, networkId=networkId, value=value, **params)

class PutUserSocialConnectionDelete(PostRequest[r_PutUserSocialConnectionDelete]):
    """Remove a user's social connection.
    
    ### Mandatory:
    - @userId
    - @networkId: see `NetworkId`
    """
    def __init__(self, userId: str, networkId: NetworkId, **params) -> None:
        super().__init__("PutUserSocialConnectionDelete", returns=r_PutUserSocialConnectionDelete, userId=userId, networkId=networkId, **params)

class PutUserUpdatePassword(PostRequest[r_PutUserUpdatePassword]):
    """Update a user's password.
    
    ### Mandatory:
    - @userUrl
    - @oldPassword
    - @newPassword
    """
    def __init__(self, userUrl: str, oldPassword: str, newPassword: str, **params) -> None:
        super().__init__("PutUserUpdatePassword", returns=r_PutUserUpdatePassword, userUrl=userUrl, oldPassword=oldPassword, newPassword=newPassword, **params)

class PutCommentDelete(PostRequest[r_PutCommentDelete]):
    """Delete a comment.

    ### Mandatory:
    - @commentId
    """
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentDelete", returns=r_PutCommentDelete, commentId=commentId, **params)

class PutCommentRestore(PostRequest[r_PutCommentRestore]):
    """Restore a deleted comment (?). #TODO check

    ### Mandatory:
    - @commentId
    """
    def __init__(self, commentId: str, **params) -> None:
        super().__init__("PutCommentRestore", returns=r_PutCommentRestore, commentId=commentId, **params)

class PutThread(PostRequest[r_PutThread]):
    """Create a new thread on a forum.

    ### Mandatory:
    - @forumId
    - @name
    - @body
    """
    def __init__(self, forumId: str, name: str, body: str, **params) -> None:
        super().__init__("PutThread", returns=r_PutThread, forumId=forumId, name=name, body=body, **params)

class PutThreadLocked(PostRequest[r_PutThreadLocked]):
    """Lock or unlock a thread.

    ### Mandatory:
    - @threadId
    - @locked
    """
    def __init__(self, threadId: str, locked: bool, **params) -> None:
        super().__init__("PutThreadLocked", returns=r_PutThreadLocked, threadId=threadId, locked=locked, **params)

class PutThreadSticky(PostRequest[r_PutThreadSticky]):
    """Sticky or un-sticky a thread.

    ### Mandatory:
    - @threadId
    - @sticky
    """
    def __init__(self, threadId: str, sticky: bool, **params) -> None:
        super().__init__("PutThreadSticky", returns=r_PutThreadSticky, threadId=threadId, sticky=sticky, **params)

class PutThreadDelete(PostRequest[r_PutThreadDelete]):
    """Delete a thread.

    ### Mandatory:
    - @threadId
    """
    def __init__(self, threadId: str, **params) -> None:
        super().__init__("PutThreadDelete", returns=r_PutThreadDelete, threadId=threadId, **params)
