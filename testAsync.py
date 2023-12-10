import asyncio
import json
from speedruncompy.endpoints import *
import logging

_log = logging.getLogger("speedruncompyTest")

_log.addHandler(logging.FileHandler("test.log", mode="w"))
_log.addHandler(logging.StreamHandler())
_log.setLevel(logging.DEBUG)

def log_result(dict):
    _log.info(json.dumps(dict))

async def main():
    # Basic
    result = await GetRun("ydj255jy").perform_async()
    log_result(result)

    # POST
    result = await GetForumList().perform_async()
    log_result(result)

    # Paginated
    result = await GetGameLeaderboard2("76rqmld8", "02q8o4p2").perform_all_async()
    log_result(result)


asyncio.run(main())