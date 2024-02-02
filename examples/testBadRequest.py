import src
from src.exceptions import *

from secret import SESSID

src.auth.login_PHPSESSID(SESSID)

try:
    src.GetSearch(query=True).perform()
except BadRequest as e:
    print(e)

try:
    # Test srcpy's own poor argument catching (at construction, not at request time!)
    src.GetAuditLogList().perform()
except TypeError as e:
    print(e)

src.GetAuditLogList().perform()