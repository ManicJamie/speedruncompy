from speedruncompy import auth
from speedruncompy import GetSession

from secret import USER_NAME, PASSWORD, SESSID

auth.login_PHPSESSID("SESSID")

response = GetSession().perform()

csrf = auth.get_CSRF()

auth.logout()