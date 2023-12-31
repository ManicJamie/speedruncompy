from .endpoints import *
from .api import SpeedrunComPy
from .exceptions import *

import pytest, os, logging, json, asyncio

"""
    NB: you may not be able to perform some of these tests depending on account permissions.
    SESSID should belong to a game moderator, LOW_SESSID should belong to a generic (but logged in) user with 2fa off.

    Commits to ManicJamie/speedruncompy must not alter the given gameid, categoryid etc.
    Hornet_Bot is NOT a supermod of any game; therefore supermod tests will be skipped in prod! Please test locally.

    Please carefully test any functionality requiring supermod endpoints.

    Also note that testing is omitted for POST actions that add data to the site; this is to avoid spamming the site with data. 
    Be careful when modifying these endpoints.
"""

if "HORNET_PHPSESSID" in os.environ: # Github action setup
    SESSID = os.environ["HORNET_PHPSESSID"]
else:
    from secret import SESSID

if "LOW_PHPSESSID" in os.environ: # Account that is logged in, but does not have permission to perform moderator actions
    LOW_SESSID = os.environ["LOW_PHPSESSID"]
else:
    from secret import LOW_SESSID

if "LOW_USERNAME" in os.environ and "LOW_PASSWORD" in os.environ:
    LOW_USERNAME = os.environ["LOW_USERNAME"]
    LOW_PASSWORD = os.environ["LOW_PASSWORD"]
else:
    from secret import LOW_USERNAME, LOW_PASSWORD

IS_SUPERMOD = False # Set to True to activate full test suite including supermod endpoints

game_id = "76rqmld8" # Hollow Knight
category_id = "02q8o4p2" # Any%
run_id = "" # Must be owned by logged in user; this one is owned by Hornet_Bot
comment_list_source = "y8k99ndy" # Must have multiple pages of comments & match itemType below
comment_list_type = itemType.RUN
thread_id = "mbkmj"

logging.getLogger().setLevel(logging.DEBUG)

def log_result(result: dict):
    logging.debug(json.dumps(result))

class TestGetRequests():
    api = SpeedrunComPy("Test")
    api.cookie_jar.update({"PHPSESSID": SESSID})

    def test_GetGameLeaderboard2(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform()
        log_result(result)
        assert "runList" in result
        assert len(result["runList"]) > 0
    
    def test_GetAsync(self):
        result = asyncio.run(GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform_async())
        standard_result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform()
        assert result == standard_result
    
    def test_PaginatedAsync(self):
        result = asyncio.run(GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_async_raw())
        standard_result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_raw()
        assert result == standard_result
    
    def test_GetGameLeaderboard2_paginated(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform_all()
        log_result(result)
        assert "runList" in result
        assert len(result["runList"]) > 0

    def test_GetGameLeaderboard2_paginated_raw(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id)._perform_all_raw()
        log_result(result)
        assert 1 in result
        assert "runList" in result[1]
        assert len(result[1]["runList"]) > 0
    
    def test_GetGameData_id(self):
        result = GetGameData(_api=self.api, gameId=game_id).perform()
        log_result(result)
        assert "game" in result
        assert result["game"]["id"] == game_id

    def test_GetGameData_url(self):
        result = GetGameData(_api=self.api, gameUrl="hollowknight").perform()
        log_result(result)
        assert "game" in result
        assert result["game"]["id"] == game_id
    
    def test_GetGameData_badreq(self):
        with pytest.raises(BadRequest) as e: # The ID not being found does NOT 404, but 400s. Good website
            GetGameData(_api=self.api, gameId="a").perform()
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGameSummary(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGameLevelSummary(self):
        ...
    
    def test_GetSearch(self):
        result = GetSearch("Hollow Knight", includeGames=True).perform()
        log_result(result)
        assert "gameList" in result
        assert len(result["gameList"]) > 0
    
    def test_GetLatestLeaderboard(self):
        result = GetLatestLeaderboard().perform()
        log_result(result)
        assert "runs" in result
        assert len(result["runs"]) > 0

    def test_GetCommentList(self):
        result = GetCommentList(comment_list_source, comment_list_type).perform()
        log_result(result)
        assert "commentList" in result
        assert len(result["commentList"]) > 0
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetCommentList_paginated_raw(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetCommentList_paginated(self):
        ...

    def test_GetThread(self):
        result = GetThread(thread_id).perform()
        log_result(result)
        assert "thread" in result
        assert "commentList" in result
        assert len(result["commentList"]) > 0
        assert "pagination" in result
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetThread_paginated_raw(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetThread_paginated(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetUserLeaderboard(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetForumList(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGuideList(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGuide(self):
        ...
    

class TestPostRequests():
    api = SpeedrunComPy("Test")
    api.cookie_jar.update({"PHPSESSID": SESSID})

    low_api = SpeedrunComPy("Test_LOWAUTH")
    low_api.cookie_jar.update({"PHPSESSID": LOW_SESSID})

    def test_DefaultAPI_separation(self):
        """Ensure separation between default api instance and the declared api instance"""
        session = GetSession().perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] == False

        session = GetSession(_api=self.api).perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] == True

    @pytest.mark.skip(reason="Test stub")
    def test_Authflow(self):
        """Check auth module (using lowauth account)"""
    
    @pytest.mark.skip(reason="Test stub")
    def test_Authflow_raw(self):
        """Check auth endpoints (using lowauth account)"""

    def test_GetSession(self):
        result = GetSession(_api=self.api).perform()
        log_result(result)
        assert result["session"]["signedIn"]
    
    def test_GetSession_unauthed(self):
        result = GetSession().perform()
        log_result(result)
        assert not result["session"]["signedIn"]

    @pytest.mark.skipif(not IS_SUPERMOD, reason = "Insufficient auth to complete test")
    @pytest.mark.skip(reason="Test stub")
    def test_GetAuditLogList(self):
        result = GetAuditLogList(_api=self.api, gameId=game_id).perform()
        log_result(result)
        ... # TODO: Finish test
    
    @pytest.mark.skipif(not IS_SUPERMOD, reason = "Insufficient auth to complete test")
    @pytest.mark.skip(reason="Test stub")
    def test_GetAuditLogList_paginated_raw(self):
        result = GetAuditLogList(_api=self.api, gameId=game_id)._perform_all_raw()
        log_result(result)
        ... # TODO: Finish test
    
    def test_GetAuditLogList_unauthed(self):
        with pytest.raises(Unauthorized) as e:
            GetAuditLogList(gameId=game_id).perform()
    
    def test_GetAuditLogList_lowperms(self):
        with pytest.raises(Unauthorized) as e: # This *should* return `Forbidden`, but SRC doesn't.
            GetAuditLogList(_api=self.low_api, gameId=game_id).perform()

    @pytest.mark.skip(reason="Test stub")
    def test_GetCommentable(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetConversationMessages(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetConversationMessages_unauthed(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetConversationMessages_lowperms(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetConversations(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetConversations_unauthed(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetForumReadStatus(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetForumReadStatus_unauthed(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGameSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetGameSettings_unauthed(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetModerationGames(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetModerationRuns(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetModerationRuns_paginated(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetModerationRuns_paginated_raw(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetNotifcations(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetNotifications_unauthed(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetRunSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetSeriesSettings(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetThemeSettings(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_GetThreadReadStatus(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetTickets(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetUserBlocks(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetUserSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_GetUserSupporterData(self):
        ...
    
    @pytest.mark.skip(reason="Unreasonable to test this endpoint as it would create spam.")
    def test_PutAuthSignup(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_PutComment(self):
        ...
    
    @pytest.mark.skip(reason="Test Stub")
    def test_PutCommentableSettings(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_PutConversation(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutConversationMessage(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_PutGame(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameBoostGrant(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameModerator(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameModeratorDelete(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutGameSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunAssignee(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutRunVerification(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutSeriesGame(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_PutSeriesGameDelete(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutSessionPing(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutThreadRead(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutTicket(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSettings(self):
        ...
    
    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSocialConnections(self):
        ...

    @pytest.mark.skip(reason="Test stub")
    def test_PutUserSocialConnectionDelete(self):
        ...