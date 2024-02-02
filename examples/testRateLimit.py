import src
from src import exceptions
from time import time

from secret import SESSID

src.api.set_default_PHPSESSID(SESSID)

session = src.GetSession().perform()

i = 0
r = 0
start = time()
for page in range(1,15):
    runs = src.GetModerationRuns(gameId="76rqmld8", limit=100, page = page).perform()
    print(str(runs)[:100])
     
    for run in runs["runs"]:
        i += 1
        while True:
            try:
                print(f"{i} {int(time()-start)}s {str(src.GetRunSettings(run['id']).perform(delay=60, retries=1))[:180]}")
                break
            except exceptions.RateLimitExceeded as e:
                r += 1
                print(f"{r} {int(time()-start)}s Rate limit exceeded! {e}")