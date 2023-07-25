from api import *
from endpoints import *
import logging, json

USER_NAME = ""
PASSWORD = ""

_log = logging.getLogger("speedruncompyTest")

_log.addHandler(logging.FileHandler("test.log", mode="w"))
_log.addHandler(logging.StreamHandler())
_log.setLevel(logging.DEBUG)

def test_endpoint(request: BaseRequest):
    _log.info(type(request).__name__)
    response = request.perform()
    _log.info(json.dumps(response))
    return response

test_endpoint(GetGameLeaderboard2("76rqmld8", "zdn80q9d", verified=0, page=1))

test_endpoint(GetGameData("76rqmld8"))

test_endpoint(GetGameRecordHistory(gameId="76rqmld8", categoryId="02q8o4p2", verified=1))

test_endpoint(GetSearch("Hollow Knight", includeGames=True))

if USER_NAME == "" or USER_NAME is None:
    _log.warning("No auth details set; terminating test early")
    exit()

test_endpoint(PutAuthLogin(USER_NAME, PASSWORD))

test_endpoint(GetSession())

test_endpoint(PutAuthLogout())

test_endpoint(GetSession())

test_endpoint(PutAuthLogin(USER_NAME, PASSWORD))
