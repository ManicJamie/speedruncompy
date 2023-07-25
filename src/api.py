import requests, base64, json
from exceptions import *
import logging

API_URI = "https://www.speedrun.com/api/v2/"
phpSESSID = ""
authed = False
LANG = "en"
ACCEPT = "application/json"
_log = logging.getLogger("speedruncompy")

def doRequest(endpoint: str, params: dict = {}, method = "GET"):
    _header = {"Accept-Language": LANG}
    _cookies = {"PHPSESSID" : phpSESSID}
    # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
    # We will do the same in case param support is retracted.
    paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
    _r = base64.urlsafe_b64encode(paramsjson).replace(b"=", b"")
    return requests.request(method, url=f"{API_URI}{endpoint}", headers=_header, cookies=_cookies, params={"_r": _r})

class BaseRequest():
    def __init__(self, endpoint, method : str, **params) -> None:
        self.endpoint = endpoint
        self.params = params
        self.method = method

    def perform(self):
        self.response = doRequest(self.endpoint, self.params, self.method)
        if self.response.status_code != 200: 
            raise APIException(self.response.status_code, self.response.content)
        return json.loads(self.response.content)

class GetRequest(BaseRequest):
    def __init__(self, endpoint, **params) -> None:
        super().__init__(endpoint, "GET", **params)

class PostRequest(BaseRequest):
    def __init__(self, endpoint, params = {}) -> None:
        super().__init__(endpoint, "POST", params=params)

class LoginRequest(PostRequest):
    def perform(self):
        r = doRequest(self.endpoint, self.params, self.method)
        if r.status_code != 200: raise APIException(r.status_code, r.content)
        return json.loads(r.content)

class AuthedRequest(PostRequest):
    pass