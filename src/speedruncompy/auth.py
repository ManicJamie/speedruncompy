import logging
from .exceptions import AuthException, NotFound
from .api import SpeedrunClient, _default
from .endpoints import PutAuthLogin, PutAuthLogout, GetSession

log = logging.getLogger("speedruncompy.auth")

def login(username: str, pwd: str, _api: SpeedrunClient = _default, tokenEntry: bool = False):
    """Quick workflow to set sessid using username & pwd. Will prompt for 2FA if tokenEntry is True, otherwise will return False."""
    try:
        result = PutAuthLogin(username, pwd, _api=_api).perform()
    except NotFound:
        print("Password is incorrect!")
        return False
    if result.get("loggedIn", False):
        log.info("Logged in using username & password")
        return True
    if result.get("tokenChallengeSent", False):
        if tokenEntry:
            log.warning("2FA is enabled - Not logged in!")
            key = input("Enter 2FA token: ")
            result = PutAuthLogin(username, pwd, key, _api=_api).perform()
            if result.get("loggedIn", False):
                log.info("Logged in using 2fa")
                return True
            else:
                log.error("2FA code rejected! Not logged in")
        else:
            log.info("2FA code required, not logged in.")
    return False

def login_PHPSESSID(sessID: str, _api: SpeedrunClient = _default):
    """Login using PHPSESSID. Uses GetSession to check if session is logged in."""
    _api.PHPSESSID = sessID
    result = GetSession(_api=_api).perform()
    session = result["session"]
    if session is None or not session["signedIn"]:
        log.error("Provided PHPSESSID is not logged in - use speedruncompy.auth.login() instead")
        return False
    log.info(f"Logged in as {session['user']['name']} using PHPSESSID")
    return True

def logout(_api: SpeedrunClient = _default):
    PutAuthLogout(_api=_api).perform()
    return True

def get_CSRF(_api: SpeedrunClient = _default):
    """Get the csrfToken of the currently logged in user, required for some endpoints."""
    result = GetSession(_api=_api).perform()
    session = result["session"]
    if session is None or not session.get("signedIn", False):
        raise AuthException("Not logged in, cannot retrieve csrfToken")
    return session.get("csrfToken")
