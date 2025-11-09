# Speedrun.com API V2 wrapper

A WIP Python wrapper for Speedrun.com's new backend API.

WIP documentation for the API can be found in [speedruncom-apiv2-docs](https://github.com/ManicJamie/speedruncom-apiv2-docs)

## Why use APIv2?

Speedrun.com's official API (aka APIv1) is not actively maintained, and both misses a large number of modern features (including various social connections on user profiles) and several unaddressed issues hinder its usage;

- pagination breaks at 10,000 items on all endpoints
- some endpoints are completely broken (notably run verification)
- some endpoints are in a degraded state (/leaderboards position)

APIv2 does struggle with some tasks APIv1 excels at; in particular grabbing all runs from a game at once is not currently possible with APIv2, instead requiring iterating through every leaderboard.

APIv2 also has no promise of stability; it can and will change without warning. This library attempts to stay up-to-date, but you may need to periodically check for updates.

## Usage

`pip install speedruncompy`, then `import speedruncompy`.

### Asynchronous

Speedruncompy is async-first, being built around `aiohttp`.
```python
from speedruncompy import GetGameLeaderboard2
import asyncio

async def async_demo():
    get_game_leaderboard = GetGameLeaderboard2(gameId="a", categoryId="b")

    leaderboard = await get_game_leaderboard.perform() # Await a single request

    leaderboard_full = await get_game_leaderboard.perform_all() # Await all pages - this awaits page 1, then awaits all other pages simultaneously.

asyncio.run(async_demo())
```

### Synchronous

If you just need some responses for a script, you can use the synchronous API:
```python
from speedruncompy import GetGameLeaderboard2

leaderboard = GetGameLeaderboard2(gameId="a", categoryId="b").perform_sync() # Perform a single request

# Paginated endpoints also have helper methods to get & merge all pages available.
leaderboard_full = GetGameLeaderboard2(gameId="", categoryId="").perform_all_sync() # Perform a request for all pages available.
```

## Helper dictionaries ("condensers")

Many endpoints return a set of lists of objects. Most of these objects contain an `id` parameter which is referred to by other objects; for example, `Run.playerIds` contains a list of the player IDs present in a run.

Speedruncompy provides convenience properties to access objects by these IDs;
```python
from speedruncompy import GetGameLeaderboard2

leaderboard = GetGameLeaderboard2(gameId="a", categoryId="b").perform_all_sync()

runner_id = leaderboard.runList[0].playerList[0]
player_name = leaderboard._playerDict[runner_id].name
```

## Client

Speedruncompy stores authorisation cookies on a `SpeedrunClient` object. This can be passed to any request as a keyword parameter `_client`.

Speedrun.com authorises APIv2 requests with the cookie `PHPSESSID`. `PutAuthLogin` sets this ID on a successful login, but you can also set it directly:

```python
from speedruncompy import SpeedrunClient, GetSession
import asyncio

token = ""  # Should be stored as part of the environment variables, not directly in code!

async def client_demo():
    client = SpeedrunClient(PHPSESSID=token)
    # or:
    client.PHPSESSID = token

    response = await GetSession(_client=client).perform()
    assert response.session.signedIn
```

### Default client

Requests with no client specified use a default global client - you can access this at `speedruncompy.api._default`.

```python
import speedruncompy
from speedruncompy import GetSession

token = ""

speedruncompy.api._default.PHPSESSID = token

# No _client passed, uses _default
session_response = GetSession().perform_sync()
assert session_response.session.signedIn
```

### Sessions

If you want to perform many requests in quick succession, it is often better to keep the HTTP session open until you have completed all your requests. `SpeedrunClients` offer an asynchronous context manager for this purpose:

```python
from speedruncompy import SpeedrunClient, GetGameSummary
import asyncio

game_ids = ["a", "b", "c"]

async def session_demo():
    client = SpeedrunClient()

    async with client:
        requests = [GetGameSummary(gameId=g) for g in game_ids]
        all_summaries = asyncio.gather(*[r.perform() for r in requests])
```

## Omissions

Admin-only endpoints will not be added due to lack of testability and usability. These include:

- GetUserList
- GetChallengesList
- GetAdminStatusSummary
- GetTicketQueueCounts
- GetTicketStatusCounts
- PutGameDelete  - _Will be added once users can delete games again_
