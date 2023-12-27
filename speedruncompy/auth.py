import logging
from .exceptions import AuthException
from .api import SpeedrunComPy, _default
from .endpoints import PutAuthLogin, PutAuthLogout, GetSession

log = logging.getLogger("speedruncompy.auth")

def login(username: str, pwd: str, _api: SpeedrunComPy = None):
    """Quick workflow to set sessid using username & pwd. Will prompt for auth token if required."""
    result: dict = PutAuthLogin(username, pwd, _api).perform()
    if result.get("loggedIn"):
        log.info("Logged in using username & password")
        return True
    if result.get("tokenChallengeSent"):
        log.warning("2FA is enabled - Not logged in!")
        key = input("Enter 2FA token: ")
        result: dict = PutAuthLogin(username, pwd, key, _api).perform()
        if result.get("loggedIn"):
            log.info("Logged in using 2fa")
            return True
        else:
            log.error("2FA code rejected! Not logged in")
    return False

def login_PHPSESSID(sessID: str, _api: SpeedrunComPy = _default):
    """Login using PHPSESSID. Uses GetSession to check if session is logged in."""
    _api.set_phpsessid(sessID)
    result: dict = GetSession(_api=_api).perform()
    if not result["session"].get("signedIn"):
        log.error("Provided PHPSESSID is not logged in - use speedruncompy.auth.login() instead")
        return False
    log.info(f"Logged in as {result['session']['user']['name']} using PHPSESSID")
    return True

def logout(_api: SpeedrunComPy = _default):
    PutAuthLogout(_api=_api).perform()
    return True

def get_CSRF(_api: SpeedrunComPy = _default):
    """Get the csrfToken of the currently logged in user, required for some endpoints."""
    result: dict[str, dict] = GetSession(_api=_api).perform()
    if not result["session"].get("signedIn", False):
        raise AuthException("Not logged in, cannot retrieve csrfToken")
    return result["session"].get("csrfToken")