from speedruncompy.endpoints import *
from speedruncompy.api import SpeedrunComPy, _default
from speedruncompy.exceptions import *
from speedruncompy import config as srccfg
from utils import check_datatype_coverage, check_pages

import pytest, os, logging, asyncio

"""
    NB: you may not be able to perform some of these tests depending on account permissions.
    SESSID should belong to a game moderator, LOW_SESSID should belong to a generic (but logged in) user with 2fa off.

    Commits to ManicJamie/speedruncompy must not alter the given gameid, categoryid etc.
    Hornet_Bot is NOT a supermod of any game; therefore supermod tests will be skipped in prod! Please test locally.

    Please carefully test any functionality requiring supermod endpoints.

    Also note that testing is omitted for POST actions that add data to the site; this is to avoid spamming the site with data.
    Be careful when modifying these endpoints.
"""

if "HORNET_PHPSESSID" in os.environ:  # Github action setup
    SESSID = os.environ["HORNET_PHPSESSID"]
else:
    from secret import SESSID

if "LOW_PHPSESSID" in os.environ:  # Account that is logged in, but does not have permission to perform moderator actions
    LOW_SESSID = os.environ["LOW_PHPSESSID"]
else:
    from secret import LOW_SESSID

if "LOW_USERNAME" in os.environ and "LOW_PASSWORD" in os.environ:
    LOW_USERNAME = os.environ["LOW_USERNAME"]
    LOW_PASSWORD = os.environ["LOW_PASSWORD"]
else:
    # from secret import LOW_USERNAME, LOW_PASSWORD
    ...

if "IS_SUPERMOD" in os.environ:
    IS_SUPERMOD = bool(os.environ["IS_SUPERMOD"])
else:
    IS_SUPERMOD = False  # Set to True to activate full test suite including supermod endpoints

game_id = "76rqmld8"  # Hollow Knight
game_url = "hollowknight"
category_id = "02q8o4p2"  # Any%
level_category = "wkpq608d"  # Hollow Knight "Level" category
run_id = "mrrg8k4m"  # ManicJamie's Hollow Knight: All Skills LP run
comment_list_source = "y8k99ndy"  # Must have multiple pages of comments & match itemType below
comment_list_type = ItemType.RUN
thread_id = "mbkmj"
user_id = "j4r6pwm8"  # ManicJamie (must have leaderboard)
user_url = "manicjamie"
forum_id = "gz5lqd21"  # Hollow Knight
guide_id = "ew8s2"  # Hollow Knight code of conduct
article_id = "jd5y09v2"
article_slug = "the-worlds-first-speedrunning-dog-at-agdq-2024"
challenge_id = "5e3eoymq"
challenge_run_id = "m9vk8gy3"

# Details required for private data; these are all accessible by Hornet_Bot
hornet_uid = "x76p3d6j"
hornet_url = "Hornet_Bot"
conversation_id = "4xEDO"  # ManicJamie <-> Hornet_Bot
series_id = "8nw2ygxn"  # Shrek Fangames
super_gameId = "pd0nlx21"  # ThirdParty_Testing

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.FileHandler("testing.log", "w"))

# All tests are done with strict type conformance to catch errors early
# In downstream this is default False, and warnings are given instead of errors.
# See `TestDatatypes.test_Missing_Fields_Loose` for behaviour without STRICT.
srccfg.COERCION = srccfg.CoercionLevel.STRICT

@pytest.fixture()
def loose_type_conformance():
    srccfg.COERCION = srccfg.CoercionLevel.ENABLED
    yield
    srccfg.COERCION = srccfg.CoercionLevel.STRICT

@pytest.fixture()
def disable_type_checking():
    srccfg.COERCION = srccfg.CoercionLevel.DISABLED
    yield
    srccfg.COERCION = srccfg.CoercionLevel.STRICT

@pytest.fixture(autouse=True)
def check_api_conformance():
    """The default API must never have a PHPSESSID."""
    assert len(_default.cookie_jar._cookies) == 0
    yield

def log_result(result: Datatype):
    logging.debug(result)
    if isinstance(result, Datatype):
        logging.debug(result.to_json())

class TestGeneric():
    api = SpeedrunComPy("Test")
    api.PHPSESSID = SESSID

    low_api = SpeedrunComPy("Test_LOWAUTH")
    low_api.PHPSESSID = LOW_SESSID

    def test_GetAsync(self):
        result = asyncio.run(GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform_async())
        standard_result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform()
        assert result == standard_result
    
    def test_PaginatedAsync(self):
        result = asyncio.run(GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_async_raw(max_pages=2))
        standard_result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_raw(max_pages=2)
        assert result == standard_result

    def test_AsyncSyncWarning(self):
        """Calls to the synchronous interface from an asynchronous context should raise an error and tell you to use async interface"""
        with pytest.raises(AIOException):
            async def main(): return GetGameLeaderboard2("76rqmld8", "02q8o4p2").perform_all(max_pages=5)
            asyncio.run(main())
    
    def test_DefaultAPI_separation(self):
        """Ensure separation between default api instance and the declared api instance"""
        session = GetSession().perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] is False, "Default API incorrectly signed in"

        session = GetSession(_api=self.api).perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] is True, "High-auth api not signed in"

    @pytest.mark.skip(reason="Test stub")
    def test_Authflow(self):
        """Check auth module (using lowauth account)"""
    
    @pytest.mark.skip(reason="Test stub")
    def test_Authflow_raw(self):
        """Check auth endpoints (using lowauth account)"""

class TestGetRequests():
    api = SpeedrunComPy("Test")
    api.PHPSESSID = SESSID

    def test_GetGameLeaderboard(self):
        result = GetGameLeaderboard(gameId=game_id, categoryId=category_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameLeaderboard_paginated(self):
        result = GetGameLeaderboard(gameId=game_id, categoryId=category_id).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)

    def test_GetGameLeaderboard2(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id, page=1).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameLeaderboard2_paginated(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)

    def test_GetGameLeaderboard2_paginated_raw(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_raw()
        log_result(result)
        check_pages(result)
    
    def test_GetGameData_id(self):
        result = GetGameData(_api=self.api, gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)
        assert result.game.id == game_id
        assert result.game.url == game_url

    def test_GetGameData_url(self):
        result = GetGameData(_api=self.api, gameUrl="hollowknight").perform()
        log_result(result)
        check_datatype_coverage(result)
        assert result.game.id == game_id
        assert result.game.url == game_url
    
    def test_GetGameData_badreq(self):
        with pytest.raises(BadRequest):  # The ID not being found does NOT 404, but 400s. Good website
            GetGameData(_api=self.api, gameId="a").perform()
    
    def test_GetGameSummary(self):
        result = GetGameSummary(gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameLevelSummary(self):
        result = GetGameLevelSummary(gameId=game_id, categoryId=level_category).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameRecordHistory(self):
        result = GetGameRecordHistory(gameId=game_id, categoryId=level_category).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetSearch(self):
        #TODO: other search types
        result = GetSearch("Hollow Knight", includeGames=True).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetLatestLeaderboard(self):
        result = GetLatestLeaderboard().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetRun(self):
        result = GetRun(run_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetUserSummary(self):
        result = GetUserSummary(user_url).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetUserPopoverData(self):
        result = GetUserPopoverData(user_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetCommentList(self):
        result = GetCommentList(comment_list_source, comment_list_type).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetCommentList_paginated_raw(self):
        result = GetCommentList(comment_list_source, comment_list_type)._perform_all_raw()
        log_result(result)
        for p, page in result.items():
            check_datatype_coverage(page)

    def test_GetCommentList_paginated(self):
        result = GetCommentList(comment_list_source, comment_list_type).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)

    def test_GetThread(self):
        result = GetThread(thread_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetThread_paginated_raw(self):
        result = GetThread(thread_id)._perform_all_raw()
        log_result(result)
        check_pages(result)

    def test_GetThread_paginated(self):
        result = GetThread(thread_id).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetThread_nonexistent(self):
        with pytest.raises(NotFound):
            GetThread("10000000").perform()

    def test_GetUserLeaderboard(self):
        result = GetUserLeaderboard(userId=user_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetForumList(self):
        """TODO: account dependent!"""
        result = GetForumList().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGuideList(self):
        result = GetGuideList(gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetGuide(self):
        result = GetGuide(guide_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetChallenge(self):
        result = GetChallenge(_api=self.api, id="5e3eoymq").perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetTitleList(self):
        result = GetTitleList().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetTitle(self):
        result = GetTitle("m2p98y5x").perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetArticleList(self):
        result = GetArticleList(limit=50).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetArticle(self):
        result = GetArticle(id=article_id).perform()
        log_result(result)
        check_datatype_coverage(result)
        assert article_slug == result.article.slug

        slug_result = GetArticle(slug=article_slug).perform()
        log_result(slug_result)
        check_datatype_coverage(slug_result)
        assert article_id == slug_result.article.id
    
    def test_GetGameList(self):
        """NB: paginated testing in TestDatatypes_Integration_Heavy"""
        result = GetGameList().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetHomeSummary(self):
        result = GetHomeSummary().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetHomeSummary_authed(self):
        result = GetHomeSummary(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetSeriesList(self):
        result = GetSeriesList().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetNewsList(self):
        result = GetNewsList(gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetNews(self):
        result = GetNews(id="z34yzw38").perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetResourceList(self):
        result = GetResourceList(game_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetStreamList(self):
        result = GetStreamList().perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetStreamList_game(self):
        result = GetStreamList(gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetStreamList_series(self):
        result = GetStreamList(seriesId=series_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetThreadList(self):
        result = GetThreadList(forum_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetChallengeLeaderboard(self):
        result = GetChallengeLeaderboard(challengeId=challenge_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetChallengeRun(self):
        result = GetChallengeRun(challenge_run_id).perform()
        log_result(result)
        check_datatype_coverage(result)

class TestPostRequests():
    api = SpeedrunComPy("Test")
    api.PHPSESSID = SESSID

    low_api = SpeedrunComPy("Test_LOWAUTH")
    low_api.PHPSESSID = LOW_SESSID

    def test_GetSession(self):
        result = GetSession(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)
        assert result["session"]["signedIn"]
    
    def test_GetSession_unauthed(self):
        result = GetSession().perform()
        log_result(result)
        check_datatype_coverage(result)
        assert not result["session"]["signedIn"]

    @pytest.mark.skipif(not IS_SUPERMOD, reason="Insufficient auth to complete test")
    def test_GetAuditLogList(self):
        result = GetAuditLogList(_api=self.api, gameId=super_gameId).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skipif(not IS_SUPERMOD, reason="Insufficient auth to complete test")
    def test_GetAuditLogList_paginated_raw(self):
        result = GetAuditLogList(_api=self.api, gameId=super_gameId)._perform_all_raw()
        log_result(result)
        check_pages(result)
    
    @pytest.mark.skipif(not IS_SUPERMOD, reason="Insufficient auth to complete test")
    def test_GetAuditLogList_paginated(self):
        result = GetAuditLogList(_api=self.api, gameId=super_gameId).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetAuditLogList_unauthed(self):
        with pytest.raises(Unauthorized):
            GetAuditLogList(gameId=game_id).perform()
    
    def test_GetAuditLogList_lowperms(self):
        with pytest.raises(Unauthorized):  # This *should* return `Forbidden`, but SRC doesn't.
            GetAuditLogList(_api=self.low_api, gameId=game_id).perform()

    def test_GetCommentable(self):
        """POST, can be called unauthed for `commentable` but `permissions` will be unhelpful."""
        result = GetCommentable(itemId=comment_list_source, itemType=comment_list_type).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetConversationMessages(self):
        result = GetConversationMessages(_api=self.api, conversationId=conversation_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetConversationMessages_unauthed(self):
        with pytest.raises(Unauthorized):
            GetConversationMessages(conversationId=conversation_id).perform()

    def test_GetConversations(self):
        result = GetConversations(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetConversations_unauthed(self):
        with pytest.raises(Unauthorized):
            result = GetConversations().perform()
            log_result(result)

    def test_GetForumReadStatus(self):
        result = GetForumReadStatus(forumIds=[forum_id], _api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetForumReadStatus_unauthed(self):
        result = GetForumReadStatus(forumIds=[forum_id]).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameSettings(self):
        result = GetGameSettings(_api=self.api, gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetGameSettings_unauthed(self):
        with pytest.raises(Unauthorized):
            GetGameSettings(gameId=game_id).perform()
    
    def test_GetModerationGames(self):
        result = GetModerationGames(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetModerationGames_unauthed(self):
        result = GetModerationGames().perform()
        log_result(result)
        check_datatype_coverage(result)
        assert result.gameModerationStats is None
        assert result.games is None
    
    def test_GetModerationRuns(self):
        result = GetModerationRuns(_api=self.api, gameId=game_id, limit=20, page=1).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetModerationRuns_paginated(self):
        result = GetModerationRuns(_api=self.api, gameId=game_id, limit=20, page=1, verified=Verified.PENDING).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetModerationRuns_paginated_raw(self):
        result = GetModerationRuns(_api=self.api, gameId=game_id, limit=20, page=1, verified=Verified.PENDING)._perform_all_raw()
        log_result(result)
        check_pages(result)

    def test_GetModerationRuns_unauthed(self):
        with pytest.raises(Unauthorized):
            GetModerationRuns(gameId=game_id, limit=20, page=1, verified=Verified.PENDING).perform()
    
    def test_GetNotifications(self):
        result = GetNotifications(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetNotifications_paginated(self):
        result = GetNotifications(_api=self.api).perform_all(max_pages=5)
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetNotifications_paginated_raw(self):
        result = GetNotifications(_api=self.api)._perform_all_raw()
        log_result(result)
        check_pages(result)
    
    def test_GetNotifications_unauthed(self):
        with pytest.raises(Unauthorized):
            GetNotifications().perform()
    
    def test_GetRunSettings(self):
        result = GetRunSettings(_api=self.api, runId=run_id).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetRunSettings_unauthed(self):
        with pytest.raises(Unauthorized):
            GetRunSettings(runId=run_id).perform()
    
    def test_GetSeriesSettings(self):
        result = GetSeriesSettings(series_id, _api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetSeriesSettings_unauthed(self):
        with pytest.raises(Unauthorized):
            GetSeriesSettings(series_id).perform()

    def test_GetThemeSettings_user(self):
        result = GetThemeSettings(_api=self.api, userId=hornet_uid).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetThemeSettings_game(self):
        result = GetThemeSettings(_api=self.api, gameId=game_id).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetThemeSettings_game_unauthed(self):
        with pytest.raises(Unauthorized):
            GetThemeSettings(gameId=game_id).perform()

    def test_GetThreadReadStatus(self):
        result = GetThreadReadStatus(_api=self.api, threadIds=[thread_id]).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetThreadReadStatus_unauthed(self):
        result = GetThreadReadStatus(threadIds=[thread_id]).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetTickets(self):
        result = GetTickets(_api=self.api, requestorIds=[hornet_uid]).perform()
        log_result(result)
        check_datatype_coverage(result)

    #TODO: GetTickets depagination
    def test_GetUserBlocks(self):
        result = GetUserBlocks(_api=self.api).perform()
        log_result(result)
        check_datatype_coverage(result)
    
    def test_GetUserBlocks_unauthed(self):
        with pytest.raises(Unauthorized):
            GetUserBlocks().perform()
    
    def test_GetUserSettings(self):
        result = GetUserSettings(_api=self.api, userUrl=hornet_url).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetUserSettings_unauthed(self):
        with pytest.raises(Unauthorized):
            GetUserSettings(userUrl=user_url).perform()
    
    def test_GetUserSupporterData(self):
        result = GetUserSupporterData(_api=self.api, userUrl=hornet_url).perform()
        log_result(result)
        check_datatype_coverage(result)

    def test_GetUserSupporterData_unauthed(self):
        with pytest.raises(Unauthorized):
            GetUserSupporterData(userUrl=user_url).perform()

class TestPutRequests():
    """Requests that modify site data"""
    api = SpeedrunComPy("Test")
    api._set_PHPSESSID(SESSID)

    low_api = SpeedrunComPy("Test_LOWAUTH")
    low_api._set_PHPSESSID(LOW_SESSID)

    @pytest.fixture(scope="class")
    def testingGame(self):
        """Provides a game for testing."""
        gData = GetGameData(gameUrl="ThirdParty_Testing").perform()
        check_datatype_coverage(gData)
        yield gData
    
    @pytest.fixture(scope="class")
    def testingSeries(self):
        """Provides a series for testing"""
        sData = GetSeriesSummary(seriesUrl="shrek_fangames").perform()
        check_datatype_coverage(sData)
        yield sData

    @pytest.fixture(scope="class")
    def testingThread(self):
        """Provides a thread for testing"""
        threadPut = PutThread("9nwlwk4z", "Testing", "A test thread for speedruncompy.", _api=self.api).perform()
        yield threadPut.thread
        threadDelete = PutThreadDelete(_api=self.api, threadId=threadPut.thread.id).perform()
        with pytest.raises(NotFound): GetThread(threadPut.thread.id).perform()
        check_datatype_coverage(threadPut)
        check_datatype_coverage(threadDelete)

    def test_PutComment_Flow(self, testingThread: Thread):
        """Posts and then deletes a comment"""
        COMMENT_DESC = "Test comment."

        commentPut = PutComment(testingThread.id, ItemType.THREAD, COMMENT_DESC, _api=self.api).perform()
        check_datatype_coverage(commentPut)

        commentCheck = GetCommentList(testingThread.id, ItemType.THREAD).perform(autovary=True)
        check_datatype_coverage(commentCheck)
        comment = next(filter(lambda c: c.text == COMMENT_DESC, commentCheck.commentList))

        commentDelete = PutCommentDelete(comment.id, _api=self.api).perform()
        check_datatype_coverage(commentDelete)

        commentDelCheck = GetCommentList(testingThread.id, ItemType.THREAD).perform(autovary=True)
        check_datatype_coverage(commentDelCheck)
        with pytest.raises(StopIteration):
            next(filter(lambda c: c.text == COMMENT_DESC, commentDelCheck.commentList))

    @pytest.mark.skip(reason="Test stub")
    def test_PutConversation(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutConversationMessage(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameBoostGrant(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameModerator(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameModeratorDelete(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameSettings(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunAssignee(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunSettings(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunVerification(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutSeriesGame(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)

    @pytest.mark.skip(reason="Test stub")
    def test_PutSeriesGameDelete(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutSessionPing(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutThreadRead(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Unreasonable test, as would spam site staff")
    @pytest.mark.skip(reason="Test stub")
    def test_PutTicket(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSettings(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSocialConnections(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)

    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSocialConnectionDelete(self):
        result = ...
        log_result(result)
        check_datatype_coverage(result)
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetSeriesSettings(self):
        result = GetSeriesSettings("").perform()
        log_result(result)
        check_datatype_coverage(result)
