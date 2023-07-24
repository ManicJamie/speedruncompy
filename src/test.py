from api import *
from endpoints import *

print("WARN: This tool should only be used for testing purposes")

params = {
    "gameId": "o1ymwk1q"
    }

r = BaseRequest("GetGameData",params, method="GET").perform()
print(r)
