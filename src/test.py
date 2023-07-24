from api import *
from endpoints import *

print("WARN: This tool should only be used for testing purposes")

params = {
    "params": {
        "gameID": "76rqmld8",
        "categoryID": "zdn80q9d",
        "verified": 0
    },
    "page": 1
    }

r = BaseRequest("GetGameLeaderboard2",params, method="GET").perform()
print(r)
