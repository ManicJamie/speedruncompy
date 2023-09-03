import base64, json
from .exceptions import *
import logging
from requests import Response, get, post
from requests.cookies import RequestsCookieJar
from time import sleep
from typing import Callable, Any, Optional

API_URI = "https://www.speedrun.com/api/v2/"
LANG = "en"
ACCEPT = "application/json"
DEFAULT_USER_AGENT = "speedruncompy/"

_log = logging.getLogger("speedruncompy")

class SpeedrunComPy():
    """Api class. Holds a unique PHPSESSID and user_agent, as well as its own logger."""
    def __init__(self, user_agent = None) -> None:
        self.cookie_jar = RequestsCookieJar()
        self.user_agent = user_agent
        if user_agent is None:
            self._log = _log
        else:
            self._log = _log.getChild(user_agent)
    
    def do_get(self, endpoint: str, params: dict = {}):
        _header = {"Accept-Language": LANG, "Accept": ACCEPT, "User-Agent": f"{DEFAULT_USER_AGENT}{self.user_agent}"}
        # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
        # We will do the same in case param support is retracted.
        paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
        _r = base64.urlsafe_b64encode(paramsjson).replace(b"=", b"")
        self._log.debug(f"GET {API_URI}{endpoint} w/ params {paramsjson}")
        return get(url=f"{API_URI}{endpoint}", headers=_header, params={"_r": _r})

    def do_post(self, endpoint:str, params: dict = {}, _setCookie=True):
        _header = {"Accept-Language": LANG, "Accept": ACCEPT, "User-Agent": f"{DEFAULT_USER_AGENT}{self.user_agent}"}
        self._log.debug(f"POST {API_URI}{endpoint} w/ params {params}")
        response = post(url=f"{API_URI}{endpoint}", headers=_header, cookies=self.cookie_jar, json=params)
        if _setCookie and response.cookies:
            self.cookie_jar.update(response.cookies)
        return response

_default = SpeedrunComPy()

def set_PHPSESSID(phpsessionid):
    _default.cookie_jar.update({"PHPSESSID": phpsessionid})

class BaseRequest():
    def __init__(self, method: Callable[[str, dict[str, Any]], Response], endpoint, **params):
        self.method = method
        self.endpoint = endpoint
        self.params = params
    
    def update_params(self, **kwargs):
        """Updates parameters using values set in kwargs"""
        self.params.update(kwargs)

    def perform(self, retries=5, delay=1) -> dict:
        self.response = self.method(self.endpoint, self.params)

        if (self.response.status_code >= 500 and self.response.status_code <= 599) or self.response.status_code == 408:
            if retries > 0:
                _log.error(f"SRC returned error {self.response.status_code} {self.response.content}. Retrying with delay {delay}:")
                for attempt in range(0, retries+1):
                    self.response = self.method(self.endpoint, self.params)
                    if not (self.response.status_code >= 500 and self.response.status_code <= 599) or self.response.status_code == 408: 
                        break
                    _log.error(f"Retry {attempt} returned error {self.response.status_code} {self.response.content}")
                    sleep(delay)                      
                else:
                    if self.response.status_code == 408: raise RequestTimeout(self)
                    else: raise ServerException(self)

        if self.response.status_code == 400: raise BadRequest(self)
        if self.response.status_code == 401: raise Unauthorized(self)
        if self.response.status_code == 403: raise Forbidden(self)
        if self.response.status_code == 404: raise NotFound(self)
        if self.response.status_code == 405: raise MethodNotAllowed(self)
        if self.response.status_code == 408: raise RequestTimeout(self)
        if self.response.status_code == 429: raise RateLimitExceeded(self)

        if (self.response.status_code >= 500 and self.response.status_code <= 599): raise ServerException(self)

        if self.response.status_code < 200 or self.response.status_code > 299:
            _log.error(f"Unknown response error returned from SRC! {self.response.status_code} {self.response.content}")
            raise APIException(self)

        return json.loads(self.response.content)
    
class BasePaginatedRequest(BaseRequest):
    def __init__(self, method: Callable[[str, dict[str, Any]], Response], endpoint, **params):
        self.pages = {}
        super().__init__(method, endpoint, **params)

    def perform_all(self, retries=5, delay=1) -> dict:
        """Get all pages and return a dict of {pageNo : pageData}. Subclasses may merge this into a combined result."""
        return self._perform_all_raw(retries, delay)
    
    def _perform_all_raw(self, retries=5, delay=1):
        """Get all pages and return a dict of {pageNo : pageData}."""
        self.params.update(page=1)
        while True:
            page = self.params["page"]
            data = self._perform_page(retries=retries, delay=delay) # this post-increments page
            self.pages[page] = data
            if page >= data.get("pagination", {}).get("pages", 1): 
                return self.pages
    
    def _perform_page(self, retries=5, delay=1) -> Optional[dict]:
        """Get the current page & advance counter to next page. Returns None if beyond the final page."""
        if "page" not in self.params: self.params["page"] = 1

        data = self.perform(retries, delay)
        if data["pagination"]["page"] != self.params["page"]:
            return None # Gone past the last page, don't give result
        
        self.params.update(page=(self.params.get("page", 0) + 1)) # advance page
        return data

class GetRequest(BaseRequest):
    def __init__(self, endpoint, _api:SpeedrunComPy=_default, **params) -> None:
        super().__init__(method=_api.do_get, endpoint=endpoint, **params)

class PostRequest(BaseRequest):
    def __init__(self, endpoint, _api:SpeedrunComPy=_default, **params) -> None:
            super().__init__(method=_api.do_post, endpoint=endpoint, **params)
