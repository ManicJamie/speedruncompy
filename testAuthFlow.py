from speedruncompy import auth
from speedruncompy import GetSession

from secret import USER_NAME, PASSWORD, SESSID

auth.loginSessID("SESSID")

response = GetSession().perform()

csrf = auth.getCSRF()

auth.logout()