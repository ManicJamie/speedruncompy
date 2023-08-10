import base64, json
from .exceptions import *
import logging
from requests import Response, get, post
from time import sleep
from typing import Callable, Any, Optional

API_URI = "https://www.speedrun.com/api/v2/"
LANG = "en"
ACCEPT = "application/json"

cookie = {}

_log = logging.getLogger("speedruncompy")

def setSessId(phpsessionid):
    global cookie
    cookie.update({"PHPSESSID": phpsessionid})

def doGet(endpoint: str, params: dict = {}):
    _header = {"Accept-Language": LANG, "Accept": ACCEPT}
    # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
    # We will do the same in case param support is retracted.
    paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
    _r = base64.urlsafe_b64encode(paramsjson).replace(b"=", b"")
    _log.debug(f"GET {API_URI}{endpoint} w/ params {paramsjson}")
    return get(url=f"{API_URI}{endpoint}", headers=_header, params={"_r": _r})

def doPost(endpoint:str, params: dict = {}, _setCookie=True):
    global cookie
    _header = {"Accept-Language": LANG, "Accept": ACCEPT}
    _log.debug(f"POST {API_URI}{endpoint} w/ params {params}")
    response = post(url=f"{API_URI}{endpoint}", headers=_header, cookies=cookie, json=params)
    if _setCookie and response.cookies:
        cookie = response.cookies
    return response

class BaseRequest():
    def __init__(self, method: Callable[[str, dict[str, Any]], Response], endpoint, **params):
        self.method = method
        self.endpoint = endpoint
        self.params = params
    
    def updateParams(self, **kwargs):
        """Updates parameters using values set in kwargs"""
        self.params.update(kwargs)

    def perform(self, retries=5, delay=1) -> dict:
        self.response = self.method(self.endpoint, self.params)

        if (self.response.status_code >= 500 and self.response.status_code <= 599) or self.response.status_code == 408:
            if retries > 0:
                _log.error(f"SRC returned error {self.response.status_code} {self.response.content}. Retrying with delay {delay}:")
                for attempt in range(attempt, retries+1):
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

        if self.response.status_code < 200 or self.response.status_code > 299:
            _log.error(f"Unknown response error returned from SRC! {self.response.status_code} {self.response.content}")
            raise APIException(self)

        return json.loads(self.response.content)
    
class BasePaginatedRequest(BaseRequest):
    def __init__(self, method: Callable[[str, dict[str, Any]], Response], endpoint, **params):
        self.pages = {}
        super().__init__(method, endpoint, **params)

    def performAll(self, retries=5, delay=1) -> dict:
        """Get all pages and return a dict of {pageNo : pageData}. Subclasses may merge this into a combined result."""
        self.params.update(page=1)
        while True:
            page = self.params["page"]
            data = self.performPage(retries=retries, delay=delay) # this post-increments page
            self.pages[page] = data
            if page >= data.get("pagination", {}).get("pages", 1): 
                return self.pages
    
    def performPage(self, retries=5, delay=1) -> Optional[dict]:
        """Get the current page & advance counter to next page. Returns None if beyond the final page."""
        if "page" not in self.params: self.params["page"] = 1

        data = self.perform(retries, delay)
        if data["pagination"]["page"] != self.params["page"]:
            return None # Gone past the last page, don't give result
        
        self.params.update(page=(self.params.get("page", 0) + 1)) # advance page
        return data

class GetRequest(BaseRequest):
    def __init__(self, endpoint, **params) -> None:
        super().__init__(method=doGet, endpoint=endpoint, **params)

class GetPaginatedRequest(GetRequest, BasePaginatedRequest):
    pass

class PostRequest(BaseRequest):
    def __init__(self, endpoint, **params) -> None:
        super().__init__(method=doPost, endpoint=endpoint, **params)

class PostPaginatedRequest(PostRequest, BasePaginatedRequest):
    pass
