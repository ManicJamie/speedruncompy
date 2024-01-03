from speedruncompy.endpoints import *
from speedruncompy import *
from speedruncompy.exceptions import APIException
from speedruncompy.api import BasePaginatedRequest
import logging, json

from secret import SESSID

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(logging.StreamHandler())
_log = logging.getLogger("speedruncompyTest")

_log.addHandler(logging.FileHandler("testPaginated.log", mode="w"))
_log.addHandler(logging.StreamHandler())

def test_endpoint(request: BasePaginatedRequest):
    _log.info(type(request).__name__)
    try:
        response = request.perform_all()
        _log.info(json.dumps(response))
        return response
    except APIException as e:
        _log.error("API Error!", exc_info=e)
        return e

auth.login_PHPSESSID(SESSID)

"""
data = test_endpoint(GetGameLeaderboard2("76rqmld8", "02q8o4p2", verified=1, obsolete= obsoleteFilter.SHOWN))
player_dict = {player["id"]:player for player in data["playerList"]}
for run in data["runList"]:
    if run["playerIds"][0] not in player_dict:
        _log.error(f"{run['playerIds'][0]} not in playerList")
"""
# test_endpoint(GetAuditLogList("76rqmld8")) # Requires supermod
data = test_endpoint(GetModerationRuns("76rqmld8", verified=0, limit=10)) # Requires verifier
data2 = GetModerationRuns("76rqmld8", verified=0, limit=100).perform()
_log.info(json.dumps(data2))
data2.pop("pagination")
if data2 != data:
    _log.error("Not equal!")
    for k, v in data2.items():
        if len(v) != len(data[k]):
            _log.error(f"List {k} doesn't match!")
#data = test_endpoint(GetNotifications())
#data = test_endpoint(GetThread(id="hl23s"))

