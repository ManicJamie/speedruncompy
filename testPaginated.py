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
        response = request.performAll()
        _log.info(json.dumps(response))
        return response
    except APIException as e:
        _log.error("API Error!", exc_info=e)
        return e

auth.loginSessID(SESSID)

test_endpoint(GetGameLeaderboard2("76rqmld8", "02q8o4p2", verified=1))
# test_endpoint(GetAuditLogList("76rqmld8")) # Requires supermod
test_endpoint(GetModerationRuns("76rqmld8", verified=0)) # Requires verifier
test_endpoint(GetNotifications())
test_endpoint(GetThread(id="hl23s"))
