import speedruncompy
from speedruncompy.exceptions import *

from secret import SESSID

speedruncompy.auth.loginSessID(SESSID)

try:
    speedruncompy.GetSearch(query=True).perform()
except BadRequest as e:
    print(e)