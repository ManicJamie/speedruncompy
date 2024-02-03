import speedruncompy
from speedruncompy.exceptions import *

from secret import SESSID

speedruncompy.auth.login_PHPSESSID(SESSID)

try:
    speedruncompy.GetSearch(query=True).perform()
except BadRequest as e:
    print(e)

try:
    # Test srcpy's own poor argument catching (at construction, not at request time!)
    speedruncompy.GetAuditLogList().perform()
except TypeError as e:
    print(e)

speedruncompy.GetAuditLogList().perform()