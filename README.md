# Speedrun.com v2 API wrapper

A WIP python wrapper for speedrun.com's new backend API.

WIP documentation for the API can be found in [speedruncom-apiv2-docs](https://github.com/ManicJamie/speedruncom-apiv2-docs)

## Usage
`pip install speedruncompy`, then `import speedruncompy`.

`speedruncompy.endpoints` contains all endpoints, and currently includes `datatypes`, `enums` & `responses`. Login flow in `speedruncompy.auth`. Other notable fields include `enums` and `exceptions`.

Example:
```python
from speedruncompy.endpoints import GetGameLeaderboard2
from speedruncompy.enums import Verified

leaderboard = GetGameLeaderboard2(gameId="", categoryId="").perform() # Perform a single request (defaulting to page 1 where paginated)
leaderboard_full = GetGameLeaderboard2(gameId="", categoryId="").perform_all() # Perform a request for all pages available.

for run in leaderboard_full.runList:
    if run.verified == Verified.VERIFIED:
        print(run.description if run.description is not None else "No description!")
```

## Authorisation
Note that this uses the API in the same way as https://speedrun.com. The v2 API does not currently accept the Bearer token the v1 API can use - but v2 is also not half-broken, and contains most of the new features SRC has added over the years.

When working with auth, it is recommended to construct your own `SpeedrunComPy` object rather than use the default:
```python
from speedruncompy.endpoints import GetGameLeaderboard2
from speedruncompy.api import SpeedrunComPy
import speedruncompy.api as srcapi

my_api = SpeedrunComPy("my_app_name")
my_api.PHPSESSID = "secret PHPSESSID"  # You should store this separately!

# srcapi._default.PHPSESSID = "secret PHPSESSID"  # Would affect all calls 
                                                  # that don't pass _api

session = GetSession(_api=my_api).perform()  # Custom client given to endpoints by _api.
if session.session.signedIn == True:
    print("I'm signed in!")
```

To authorise you must either complete a standard login flow (see [auth](./src/speedruncompy/auth.py)) or use the `PHPSESSID` of a session you logged in on browser. You can provide this object to endpoints as `_api`, and you can set `apiInstance.PHPSESSID` manually.

Note that sessions _may_ expire unexpectedly. Periodically calling `PutSessionPing` may help, but for long-lived applications you should have additional monitoring. If you need it, you may need to set up automatic login using `PutAuthLogin`, with potential email inbox monitoring for 2FA.

## Why use V2?
v1 is not actively maintained, and both misses a large number of modern features (including various social connections on user profiles) and has various issues clouding its use;
- pagination breaks at 10,000 items on all endpoints
- some endpoints are completely broken (notably run verification)
- some endpoints are in a degraded state (/leaderboards position)

However, V2 is poor for some specific tasks; since it can only fetch one category at a time, indexing all runs in a game (or site-wide) is slow. Rate limits are also less simple, undocumented & vary between endpoints.

## Omissions
Admin-only endpoints will not be added due to lack of testability and usability. These include:
- GetAdminStatusSummary
- GetTicketQueueCounts
- GetTicketStatusCounts
- PutGameDelete

## Goals
Future versions will aim to assist further in development;
- Complete datatype coverage & testing to detect regressions & SRC-side additions
- Convenience properties potentially exploiting cached data?