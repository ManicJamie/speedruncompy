from . import api
from .endpoints import PutAuthLogin, PutAuthLogout, GetSession

def login(username: str, pwd: str):
    """Quick workflow to set sessid using username & pwd. Will prompt for auth token if required."""
    result: dict = PutAuthLogin(username, pwd).perform()
    if result.get("loggedIn"):
        api._log.info("Logged in using username & password")
        return True
    if result.get("tokenChallengeSent"):
        api._log.warning("2FA is enabled - Not logged in!")
        key = input("Enter 2FA token: ")
        result: dict = PutAuthLogin(username, pwd, key).perform()
        if result.get("loggedIn"):
            api._log.info("Logged in using 2fa")
            return True
        else:
            api._log.error("2FA code rejected! Not logged in")
    return False

def loginSessID(sessID: str):
    """Login using PHPSESSID. Uses GetSession to check if session is logged in."""
    api.setSessId(sessID)
    result: dict = GetSession().perform()
    if not result.get("session").get("signedIn"):
        api._log.error("Provided PHPSESSID is not logged in - use speedruncompy.auth.login() instead")
        return False
    api._log.info("Logged in using PHPSESSID")
    return True

def logout():
    result = PutAuthLogout().perform()
    return True

def getCSRF():
    """Get the csrfToken of the currently logged in user, required for some endpoints."""
    result: dict = GetSession().perform()
    if not result.get("session").get("signedIn"):
        api._log.error("Not logged in - cannot get CSRF")
        return None
    return result.get("csrfToken")