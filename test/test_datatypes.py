import asyncio
import os
from random import randint, sample

from speedruncompy.datatypes import *
from speedruncompy import config as srccfg
from speedruncompy.endpoints import *
from speedruncompy.exceptions import IncompleteDatatype, IncompleteEnum

from utils import check_datatype_coverage

import pytest, pytest_asyncio, logging

logging.getLogger().setLevel(logging.DEBUG)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SKIP_HEAVY_TESTS = bool(os.environ.get("SKIP_HEAVY_TESTS", True))

game_id = "76rqmld8"  # Hollow Knight
category_id = "02q8o4p2"  # Any%
challenge_id = "42ymr396"  # Ghostrunner 2

# All tests are done with strict type conformance to catch errors early
# In downstream this is default False, and warnings are given instead of errors.
# See `TestDatatypes.test_Missing_Fields_Loose` for behaviour without STRICT.
srccfg.COERCION = 1

@pytest.fixture()
def loose_type_conformance():
    srccfg.COERCION = 0
    yield
    srccfg.COERCION = 1

@pytest.fixture()
def disable_type_checking():
    srccfg.COERCION = -1
    yield
    srccfg.COERCION = 1

class TestDatatypes():
    def test_Datatype_conformance(self):
        """General dictlike conformance."""
        dt_raw = {"some": "data", "that's": True}
        different = {"some": "data", "that's": False}
        dt = Datatype(dt_raw)
        assert dt["some"] == dt_raw["some"]  # Dict access conformance
        with pytest.raises(KeyError): dt["a"]
        assert dt == dt_raw  # Equivalence
        assert not (dt == different)
        assert not (dt != dt_raw)  # Nonequivalence
        assert dt != different
        
        assert dt.some == "data"  # Attribute get
        dt.some = "different data"  # Attribute set # type: ignore
        assert dt.some == "different data"
        assert dt["some"] == "different data"
        dt["some"] = "data"  # Dictlike set
        assert dt["some"] == "data"
        assert dt.some == "data"
        extra = {"new": "kvp"}
        dt |= extra
        assert "some" in dt
        assert "that's" in dt
        assert "new" in dt

    def test_Missing_Fields_Loose(self, caplog: pytest.LogCaptureFixture, loose_type_conformance: None):
        """Missing fields should raise a warning"""
        with caplog.at_level(logging.WARNING):
            var_value_raw = {"variableId": "v"}  # Missing valueId
            vv = VarValue(var_value_raw)
            assert vv == var_value_raw  # Construction still worked
        assert "Datatype VarValue constructed missing mandatory fields ['valueId']" in caplog.text

    def test_Missing_Fields(self):
        """Missing fields should raise an error in Strict mode"""
        var_value_raw = {"variableId": "v"}  # Missing valueId
        with pytest.raises(IncompleteDatatype):
            VarValue(var_value_raw)  # Construction fails due to strictness

    raw_run_settings = {"runId": "a", "gameId": "b", "categoryId": "c",
                        "playerNames": ["p"],
                        "time": {"hour": 0, "minute": 1, "second": 2, "millisecond": 3},
                        "platformId": "p", "emulator": False,
                        "video": "url", "comment": "comment", "date": 11111,
                        "values": [{"variableId": "38dopp1l", "valueId": "4lxogy4l"},
                                   {"variableId": "onvkzmlm", "valueId": "gq7o3rnl"}]}
    
    def test_RunSettings(self, caplog: pytest.LogCaptureFixture):
        raw = self.raw_run_settings.copy()
        settings = RunSettings(raw)  # Does not fail w/ strict typechecking, as missing field timeWithLoads is opt

        assert settings.timeWithLoads is None  # Missing attribute defaults to None
        with pytest.raises(AttributeError, match="'RunSettings' object has no attribute 'aaaa'"):
            settings.aaaa  # Nonexistant attribute still raises AttributeError
        
        assert isinstance(settings.values[0], VarValue)
    
    def test_NullableFields(self):
        class TestDT(Datatype):
            test: int | None
        
        TestDT({"test": None})  # Test construction does not error
    
    def test_OptFields(self):
        class TestDT(Datatype):
            test: OptField[int]
        
        TestDT({})  # Test construction does not error

@pytest.mark.skipif(SKIP_HEAVY_TESTS, reason="SKIP_HEAVY_TESTS == True")
class TestDatatypes_Integration_Heavy():
    """
    Heavy testing meant to be semi-exhaustive, that will most likely hit rate limits on repeat runs.

    Call list:
    GetGameList: all pages (<100) + 1 random page
    GetGameData: 200
    GetGameLeaderboard2: 200
    """
    @pytest_asyncio.fixture(scope="session")
    async def all_games(self) -> r_GetGameList:
        """All pages of GetGameList"""
        return await GetGameList().perform_all_async()

    @pytest_asyncio.fixture(scope="session")
    async def small_game_subset(self) -> list[str]:
        """List of 250 random game IDs"""
        return sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async()).gameList], 200)  # type: ignore

    @pytest_asyncio.fixture(scope="session")
    async def small_game_subset_data(self, small_game_subset) -> list[r_GetGameData]:
        """GetGameData for 200 random games"""
        return await asyncio.gather(*[GetGameData(gameId=g).perform_async() for g in small_game_subset], return_exceptions=False)
    
    @pytest.fixture(scope="session")
    async def small_game_subset_categories(self, small_game_subset_data: list[r_GetGameData]) -> list[tuple[r_GetGameData, str]]:
        """1 category per game based on largest runCount, for a total of <=200 games (games with no runs excluded)"""
        overall = []
        for g in small_game_subset_data:
            if len(g.runCounts) == 0: continue
            top = max(g.runCounts, key=lambda x: x.count)
            if top.count == 0: continue
            overall.append((g, top.categoryId))
        return overall
    
    @pytest_asyncio.fixture(scope="session")
    async def small_game_subset_leaderboards(self, small_game_subset_categories: list[tuple[r_GetGameData, str]]) -> list[r_GetGameLeaderboard2]:
        """1 leaderboard per game, 1 page per board (to avoid rate limit on an average > 2 boards per game)"""
        return await asyncio.gather(*[GetGameLeaderboard2(gameId=g.game.id, categoryId=c).perform_async() for g, c in small_game_subset_categories])

    def test_Runs(self, small_game_subset_leaderboards: list[r_GetGameLeaderboard2]):
        for board in small_game_subset_leaderboards:
            for run in board.runList:
                check_datatype_coverage(run)
    
    def test_Challenge_Runs(self):
        source = GetChallengeLeaderboard(challenge_id).perform()
        if len(source.challengeRunList) == 0: return
        for run in source.challengeRunList:
            check_datatype_coverage(run)
    
    def test_Game(self, all_games: r_GetGameList):
        games = all_games.gameList
        for game in games:
            check_datatype_coverage(game)
    
    def test_Category(self, small_game_subset_data: list[r_GetGameData]):
        for g in small_game_subset_data:
            for cat in g.categories:
                check_datatype_coverage(cat)
    
    def test_Level(self, small_game_subset_data: list[r_GetGameData]):
        for g in small_game_subset_data:
            for lev in g.levels:
                check_datatype_coverage(lev)

    def test_Platform(self, small_game_subset_data: list[r_GetGameData]):
        for g in small_game_subset_data:
            for plat in g.platforms:
                check_datatype_coverage(plat)

    def test_Player(self, small_game_subset_leaderboards: list[r_GetGameLeaderboard2]):
        for board in small_game_subset_leaderboards:
            for player in board.playerList:
                check_datatype_coverage(player)

    def test_User(self):
        source = GetChallengeLeaderboard(challenge_id).perform()
        for user in source.userList:
            check_datatype_coverage(user)
