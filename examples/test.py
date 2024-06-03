import speedruncompy as src
from speedruncompy.api import *
from speedruncompy.endpoints import *
import logging, json
from speedruncompy.datatypes.enums import *

from secret import USER_NAME, PASSWORD, SESSID, CSRF

_log = logging.getLogger("speedruncompyTest")

_log.addHandler(logging.FileHandler("test.log", mode="w"))
_log.addHandler(logging.StreamHandler())
_log.setLevel(logging.DEBUG)

def test_endpoint(request: BaseRequest):
    _log.info(type(request).__name__)
    try:
        response = request.perform()
        _log.info(json.dumps(response))
        return response
    except APIException as e:
        _log.error("API Error!", exc_info=e)
        return e

test_endpoint(GetGameLeaderboard2("76rqmld8", "02q8o4p2", verified=1, page=15))

test_endpoint(GetGameData("76rqmld8"))
"""
test_endpoint(GetGameRecordHistory(gameId="76rqmld8", categoryId="02q8o4p2", verified=1))
"""
test_endpoint(GetSearch("Celeste", includeGames=True))

if USER_NAME == "" and SESSID == "":
    _log.warning("No auth details set; terminating test early")
    exit()

"""
# Logout test (for use with non-2fa accounts)
test_endpoint(PutAuthLogin(USER_NAME, PASSWORD))

test_endpoint(GetSession())

test_endpoint(PutAuthLogout())

test_endpoint(GetSession())

test_endpoint(PutAuthLogin(USER_NAME, PASSWORD))
print(api.cookie)
"""

test_endpoint(GetSession())

if SESSID is None:
    test_endpoint(PutAuthLogin(USER_NAME, PASSWORD))
    token = input("Enter token:")
    test_endpoint(PutAuthLogin(USER_NAME, PASSWORD, token))
else:
    set_default_PHPSESSID(SESSID)

session = test_endpoint(GetSession())
csrf = session["session"]["csrfToken"]

test_endpoint(GetModerationRuns(gameId="76rqmld8", limit=100, page=1, verified=0))

#test_endpoint(GetModerationGames())
"""
run_settings = test_endpoint(GetRunSettings("y2gko66z"))["settings"]

run_settings["comment"] = "test!"

test_endpoint(PutRunSettings(run_settings, csrfToken=csrf))

#test_endpoint(PutRunVerification("y2gko66z", 1, reason="Test Accept"))

test_endpoint(GetRunSettings("y2gko66z"))
"""
"""
output = test_endpoint(GetUserSettings(userUrl="manicjamie"))

test_endpoint(PutUserSettings("manicjamie", output["settings"]))
"""
"""
test_endpoint(PutSessionPing())

test_endpoint(GetLatestLeaderboard(gameId="76rqmld8", limit=999))

test_endpoint(GetThread(id="7p1bg"))

#test_endpoint(GetThreadReadStatus())

test_endpoint(GetCommentList(itemId="mr80v32y", itemType=2))

test_endpoint(GetForumList())

test_endpoint(GetConversationMessages(conversationId="Fb7Ay"))

test_endpoint(GetSearch(query=USER_NAME, includeUsers=True))

test_endpoint(GetUserSettings(USER_NAME))

test_endpoint(GetNotifications())
"""
test_endpoint(GetRunSettings("yvp75n6y"))