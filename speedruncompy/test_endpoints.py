from speedruncompy.endpoints import *
from speedruncompy.api import SpeedrunComPy
from speedruncompy.exceptions import *

import pytest, os, logging, json

if "HORNET_PHPSESSID" in os.environ: # Github action setup
    SESSID = os.environ["HORNET_PHPSESSID"]
else:
    from secret import SESSID

game_id = "76rqmld8" # Hollow Knight
category_id = "02q8o4p2" # Any%
run_id = "" # Must be owned by logged in user; this one is owned by Hornet_Bot

logging.getLogger().setLevel(logging.DEBUG)

def log_result(result: dict):
    logging.debug(json.dumps(result))

class TestGetRequests():
    api = SpeedrunComPy("Test")
    api.cookie_jar.update({"PHPSESSID": SESSID})

    def test_DefaultAPI_separation(self):
        """Ensure separation between default api instance and the declared api instance"""
        session = GetSession().perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] == False

        session = GetSession(_api=self.api).perform()
        assert "signedIn" in session["session"]
        assert session["session"]["signedIn"] == True

    def test_GetGameLeaderboard2(self):
        result = GetGameLeaderboard2(_api=self.api, gameId=game_id, categoryId=category_id).perform()
        log_result(result)
        assert "runList" in result
        assert len(result["runList"]) > 0    
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

class TestPostRequests():
    api = SpeedrunComPy("Test")
    api.cookie_jar.update({"PHPSESSID": SESSID})

    def test_GetSession(self):
        result = GetSession(_api=self.api).perform()
        log_result(result)
        assert result["session"]["signedIn"]
    
    def test_GetSession_unauthed(self):
        result = GetSession().perform()
        log_result(result)
        assert not result["session"]["signedIn"]