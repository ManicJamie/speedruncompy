import asyncio
import os
from random import randint, sample

from pydantic import ValidationError

from speedruncompy.datatypes import *
from speedruncompy import config as srccfg
from speedruncompy.endpoints import *
from speedruncompy.exceptions import IncompleteDatatype, IncompleteEnum

from utils import check_model_coverage

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

srccfg.strict_mode = True

class DemoModel(SpeedrunModel):
    name: str

@pytest.fixture()
def non_strict():
    srccfg.strict_mode = False
    yield
    srccfg.strict_mode = True


class TestModels():
    async def test_convenience_dicts(self):
        runs = [
            Run(id="a", gameId="a", categoryId="a", time=1, emulator=False, verified=Verified.VERIFIED, date=100, hasSplits=False, playerIds=["a"], valueIds=["a"], videoState=VideoState.UNKNOWN),
            Run(id="b", gameId="b", categoryId="b", time=1, emulator=False, verified=Verified.VERIFIED, date=100, hasSplits=False, playerIds=["b"], valueIds=["b"], videoState=VideoState.UNKNOWN),
            Run(id="c", gameId="c", categoryId="c", time=1, emulator=False, verified=Verified.VERIFIED, date=100, hasSplits=False, playerIds=["c"], valueIds=["c"], videoState=VideoState.UNKNOWN),
        ]
        response = r_GetGameLeaderboard2(runList=runs, playerList=[], platformList=[], pagination=Pagination(count=1, page=1, pages=1, per=1))
        
        assert "a" in response._runDict and "b" in response._runDict and "c" in response._runDict, "_runDict not constructed!"
    
    async def test_convenience_paginated(self):
        pages = {
            1: r_GetGameLeaderboard2(runList=[
                Run(id="a", gameId="a", categoryId="a", time=1, emulator=False, verified=Verified.VERIFIED, date=100, hasSplits=False, playerIds=["a"], valueIds=["a"], videoState=VideoState.UNKNOWN)],
                playerList=[], platformList=[], pagination=Pagination(count=1, page=1, pages=1, per=1)),
            2: r_GetGameLeaderboard2(runList=[
                Run(id="b", gameId="b", categoryId="b", time=1, emulator=False, verified=Verified.VERIFIED, date=100, hasSplits=False, playerIds=["b"], valueIds=["b"], videoState=VideoState.UNKNOWN)],
                playerList=[], platformList=[], pagination=Pagination(count=1, page=1, pages=1, per=1)),
        }
        
        combined: r_GetGameLeaderboard2 = BasePaginatedRequest._combine_pages(pages.values())
        
        assert "a" in combined._runDict and "b" in combined._runDict
        assert len(combined.runList) == 2
    
    async def test_model_missing_fields(self):
        dump = r'{"id":"zgje3ljz","gameId":"76rqmld8"}'
        with pytest.raises(ValidationError):
            Run.model_validate_json(dump)
    
    async def test_model_extra_fields(self):
        varVal = VarValue(variableId="a", valueId="b")
        varVal2 = VarValue.model_validate({"variableId": "a", "valueId": "b", "c": "c"})
        
        assert varVal2.__pydantic_extra__ is not None
        assert "c" in varVal2.__pydantic_extra__
        assert varVal != varVal2
        
        # Test suite checking; no extra fields = pass, extra fields = complain
        check_model_coverage(varVal)
        with pytest.raises(Exception):
            check_model_coverage(varVal2)


@pytest.mark.skipif(SKIP_HEAVY_TESTS, reason="SKIP_HEAVY_TESTS == True")
class TestDatatypes_Integration_Heavy():
    """
    Heavy testing meant to be semi-exhaustive, that will most likely hit rate limits on repeat runs.

    Call list:
    GetGameList: all pages (<100) + 1 random page
    GetGameData: 200
    GetGameLeaderboard2: 200
    """
    # @pytest_asyncio.fixture(scope="session")
    # async def all_games(self) -> r_GetGameList:
    #     """All pages of GetGameList"""
    #     return await GetGameList().perform_all_async()

    # @pytest_asyncio.fixture(scope="session")
    # async def small_game_subset(self) -> list[str]:
    #     """List of 250 random game IDs"""
    #     return sample([g["id"] for g in (await GetGameList(page=randint(1, 50)).perform_async()).gameList], 200)  # type: ignore

    # @pytest_asyncio.fixture(scope="session")
    # async def small_game_subset_data(self, small_game_subset) -> list[r_GetGameSummary]:
    #     """GetGameData for 200 random games"""
    #     return await asyncio.gather(*[GetGameSummary(gameId=g).perform_async() for g in small_game_subset], return_exceptions=False)
    
    # @pytest.fixture(scope="session")
    # async def small_game_subset_categories(self, small_game_subset_data: list[r_GetGameSummary]) -> list[tuple[r_GetGameSummary, str]]:
    #     """1 category per game based on largest runCount, for a total of <=200 games (games with no runs excluded)"""
    #     overall = []
    #     for g in small_game_subset_data:
    #         if len(g.stats.) == 0: continue
    #         top = max(g.runCounts, key=lambda x: x.count)
    #         if top.count == 0: continue
    #         overall.append((g, top.categoryId))
    #     return overall
    
    # @pytest_asyncio.fixture(scope="session")
    # async def small_game_subset_leaderboards(self, small_game_subset_categories: list[tuple[r_GetGameData, str]]) -> list[r_GetGameLeaderboard2]:
    #     """1 leaderboard per game, 1 page per board (to avoid rate limit on an average > 2 boards per game)"""
    #     return await asyncio.gather(*[GetGameLeaderboard2(gameId=g.game.id, categoryId=c).perform_async() for g, c in small_game_subset_categories])

    # def test_Runs(self, small_game_subset_leaderboards: list[r_GetGameLeaderboard2]):
    #     for board in small_game_subset_leaderboards:
    #         for run in board.runList:
    #             check_model_coverage(run)
    
    # def test_Challenge_Runs(self):
    #     source = GetChallengeLeaderboard(challenge_id).perform()
    #     if len(source.challengeRunList) == 0: return
    #     for run in source.challengeRunList:
    #         check_model_coverage(run)
    
    # def test_Game(self, all_games: r_GetGameList):
    #     games = all_games.gameList
    #     for game in games:
    #         check_model_coverage(game)
    
    # def test_Category(self, small_game_subset_data: list[r_GetGameData]):
    #     for g in small_game_subset_data:
    #         for cat in g.categories:
    #             check_model_coverage(cat)
    
    # def test_Level(self, small_game_subset_data: list[r_GetGameData]):
    #     for g in small_game_subset_data:
    #         for lev in g.levels:
    #             check_model_coverage(lev)

    # def test_Platform(self, small_game_subset_data: list[r_GetGameData]):
    #     for g in small_game_subset_data:
    #         for plat in g.platforms:
    #             check_model_coverage(plat)

    # def test_Player(self, small_game_subset_leaderboards: list[r_GetGameLeaderboard2]):
    #     for board in small_game_subset_leaderboards:
    #         for player in board.playerList:
    #             check_model_coverage(player)

    # def test_User(self):
    #     source = GetChallengeLeaderboard(challenge_id).perform()
    #     for user in source.userList:
    #         check_model_coverage(user)
