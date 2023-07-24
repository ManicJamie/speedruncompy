from api import *
from endpoints import *

print("WARN: This tool should only be used for testing purposes")

params = {
    "gameId" : "76rqmld8"
    }

r = BaseRequest("GetModerationRuns",params, method="PUT").perform()
print(r)
