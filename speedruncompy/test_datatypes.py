import asyncio
import os
from random import randint, sample
from .datatypes import *
from . import datatypes
from .endpoints import *

import pytest, logging

logging.getLogger().setLevel(logging.DEBUG)

game_id = "76rqmld8" # Hollow Knight
category_id = "02q8o4p2" # Any%
challenge_id = "42ymr396" # Ghostrunner 2

# All tests are done with strict type conformance to catch errors early
# In downstream this is default False, and warnings are given instead of errors.
# See `test_Missing_Fields_Loose` for behaviour without STRICT.
datatypes.STRICT_TYPE_CONFORMANCE = True

class TestDatatypes():
    @pytest.fixture()
    def loose_type_conformance(self):
        datatypes.STRICT_TYPE_CONFORMANCE = False
        yield
        datatypes.STRICT_TYPE_CONFORMANCE = True

    def test_Datatype_conformance(self):
        """General dictlike conformance."""
        dt_raw = {"some": "data", "that's": True}
        different = {"some": "data", "that's": False}
        dt = Datatype(dt_raw)
        assert dt["some"] == dt_raw["some"] # Dict access conformance
        with pytest.raises(KeyError): dt["a"]
        assert dt == dt_raw # Equivalence
        assert not (dt == different)
        assert not (dt != dt_raw) # Nonequivalence
        assert dt != different
        
        assert dt.some == "data" # Attribute get
        dt.some = "different data" # Attribute set
        assert dt.some == "different data"
        assert dt["some"] == "different data"
        dt["some"] = "data" # Dictlike set
        assert dt["some"] == "data"
        assert dt.some == "data"

    def test_Missing_Fields_Loose(self, caplog: pytest.LogCaptureFixture, loose_type_conformance: None):
        """Missing fields should raise a warning"""
        with caplog.at_level(logging.WARNING):
            var_value_raw = {"variableId": "v"} # Missing valueId
            vv = VariableValue(var_value_raw)
            assert vv == var_value_raw # Construction still worked
        assert "Datatype VariableValue constructed missing mandatory fields ['valueId']" in caplog.text

    def test_Missing_Fields(self):
        """Missing fields should raise an error in Strict mode"""
        var_value_raw = {"variableId": "v"} # Missing valueId
        with pytest.raises(IncompleteDatatype):
            VariableValue(var_value_raw) # Construction fails due to strictness

    raw_run_settings = {"runId": "a", "gameId": "b", "categoryId": "c",
            "playerNames": ["p"],
            "time": {"hour": 0, "minute": 1, "second": 2, "millisecond": 3},
            "platformId": "p", "emulator": False,
            "video": "url", "comment": "comment", "date": 11111,
            "values": [{"variableId": "38dopp1l", "valueId": "4lxogy4l"},
                {"variableId": "onvkzmlm", "valueId": "gq7o3rnl"}]}
    
    def test_RunSettings(self, caplog: pytest.LogCaptureFixture):
        raw = self.raw_run_settings.copy()
        settings = RunSettings(raw) # Does not fail w/ strict typechecking, as missing field timeWithLoads is opt

        assert settings.timeWithLoads is None # Missing attribute defaults to None
        with pytest.raises(AttributeError, match="'RunSettings' object has no attribute 'aaaa'"):
            settings.aaaa # Nonexistant attribute still raises AttributeError
        
        assert isinstance(settings.values[0], VariableValue)

@pytest.mark.skipif("SKIP_HEAVY_TESTS" in os.environ, reason="Skip on automated runs")
class TestDatatypes_Integration():
    async def test_Runs(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def getCat(g):
            data = await GetGameData(gameId=g).perform_async()
            if len(data["runCounts"]) == 0: return None
            if data["runCounts"][0]["count"] == 0: return None
            return (g, data["runCounts"][0]["categoryId"])
        
        game_cat = await asyncio.gather(*[getCat(x) for x in games])
        game_cat = [i for i in game_cat if i != None]

        async def checkBoard(g, c):
            source = await GetGameLeaderboard2(g, c).perform_async()
            runs = [Run(s) for s in source["runList"]]
            if len(runs) == 0 and len(source["runList"]) == 0: return
            assert runs == source["runList"] # This should be a given
            hints = Run.get_type_hints().keys()
            for (raw, run) in zip(source["runList"], runs):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkBoard(g, c) for g, c in game_cat])
    
    def test_Challenge_Runs(self):
        source = GetChallengeLeaderboard(challenge_id).perform()
        runs = [ChallengeRun(s) for s in source["challengeRunList"]]
        if len(runs) == 0 and len(source["challengeRunList"]) == 0: return
        assert runs == source["challengeRunList"] # This should be a given
        hints = ChallengeRun.get_type_hints().keys()
        for (raw, run) in zip(source["challengeRunList"], runs):
            for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
    
    def test_Game(self):
        source = GetGameList().perform_all()
        games = [Game(g) for g in source["gameList"]]
        assert games == source["gameList"] # This should be a given
        hints = Game.get_type_hints().keys()
        for (raw, game) in zip(source["gameList"], games):
            for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
    
    @pytest.mark.asyncio
    async def test_Category(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def checkGame(g):
            source = await GetGameData(gameId=g).perform_async()
            cats = [Category(c) for c in source["categories"]]
            hints = Category.get_type_hints().keys()
            for (raw, cat) in zip(source["categories"], cats):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkGame(g) for g in games])
    
    @pytest.mark.asyncio
    async def test_Level(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def checkGame(g):
            source = await GetGameData(gameId=g).perform_async()
            levels = [Level(c) for c in source["levels"]]
            hints = Level.get_type_hints().keys()
            for (raw, cat) in zip(source["levels"], levels):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkGame(g) for g in games])
    
    @pytest.mark.asyncio
    async def test_Platform(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def checkGame(g):
            source = await GetGameData(gameId=g).perform_async()
            levels = [Platform(c) for c in source["platforms"]]
            hints = Platform.get_type_hints().keys()
            for (raw, cat) in zip(source["platforms"], levels):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkGame(g) for g in games])

    @pytest.mark.asyncio
    async def test_Platform(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def checkGame(g):
            source = await GetGameData(gameId=g).perform_async()
            levels = [Platform(c) for c in source["platforms"]]
            hints = Platform.get_type_hints().keys()
            for (raw, cat) in zip(source["platforms"], levels):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkGame(g) for g in games])

    @pytest.mark.asyncio
    async def test_Player(self):
        games = sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async())["gameList"]], 50)

        async def getCat(g):
            data = await GetGameData(gameId=g).perform_async()
            if len(data["runCounts"]) == 0: return None
            if data["runCounts"][0]["count"] == 0: return None
            return (g, data["runCounts"][0]["categoryId"])
        
        game_cat = await asyncio.gather(*[getCat(x) for x in games])
        game_cat = [i for i in game_cat if i != None]

        async def checkBoard(g, c):
            source = await GetGameLeaderboard2(g, c).perform_async()
            players = [Player(s) for s in source["playerList"]]
            if len(players) == 0 and len(source["playerList"]) == 0: return
            assert players == source["playerList"] # This should be a given
            hints = Player.get_type_hints().keys()
            for (raw, run) in zip(source["playerList"], players):
                for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes
        
        await asyncio.gather(*[checkBoard(g, c) for g, c in game_cat])

    def test_User(self):
        source = GetChallengeLeaderboard(challenge_id).perform()
        users = [User(g) for g in source["userList"]]
        logging.info(f"Testing {len(users)} users")
        assert users == source["userList"] # This should be a given
        hints = User.get_type_hints().keys()
        for (raw, game) in zip(source["userList"], users):
            for key in raw: assert key in hints # Ensure that speedruncompy covers all attributes


    