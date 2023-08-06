from src import auth

from secret import USER_NAME, PASSWORD, SESSID

auth.loginSessID(SESSID)

csrf = auth.getCSRF()

auth.logout()