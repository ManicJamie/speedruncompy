from api import *
from endpoints import *
import logging, json

logging.getLogger().addHandler(logging.FileHandler("test.log", mode="w"))
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)

logging.warning("This tool should only be used for testing purposes")

logging.info("GetGameLeaderboard2")
request = GetGameLeaderboard2("76rqmld8", "zdn80q9d", verified=0, page=1)
response = request.perform()
logging.info(json.dumps(response))

logging.info("GetGameData")
request = GetGameData("76rqmld8")
response = request.perform()
logging.info(json.dumps(response))

logging.info("GetGameRecordHistory")
request = GetGameRecordHistory(gameId="76rqmld8", categoryId="02q8o4p2", verified=1)
response = request.perform()
logging.info(json.dumps(response))

logging.info("GetSearch")
request = GetSearch("Hollow Knight", includeGames=True)
response = request.perform()
logging.info(json.dumps(response))