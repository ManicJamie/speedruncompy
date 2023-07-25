import requests, base64, json
from exceptions import *
import logging

API_URI = "https://www.speedrun.com/api/v2/"
LANG = "en"
ACCEPT = "application/json"

cookie = {}

_log = logging.getLogger("speedruncompy")

def setSessId(phpsessionid):
    global cookie
    cookie = {"PHPSESSID": phpsessionid}

def doGet(endpoint: str, params: dict = {}):
    _header = {"Accept-Language": LANG, "Accept": ACCEPT}
    # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
    # We will do the same in case param support is retracted.
    paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
    _r = base64.urlsafe_b64encode(paramsjson).replace(b"=", b"")
    return requests.get(url=f"{API_URI}{endpoint}", headers=_header, params={"_r": _r})

def doPost(endpoint:str, params: dict = {}, _setCookie=True):
    global cookie
    _header = {"Accept-Language": LANG, "Accept": ACCEPT}
    response = requests.post(url=f"{API_URI}{endpoint}", headers=_header, cookies=cookie, json=params)
    if _setCookie and response.cookies:
        cookie = response.cookies
    return response

class BaseRequest():
    def perform(self):
        pass

class GetRequest(BaseRequest):
    def __init__(self, endpoint, **params) -> None:
        self.endpoint = endpoint
        self.params = params

    def perform(self):
        self.response = doGet(self.endpoint, self.params)
        if self.response.status_code != 200: 
            raise APIException(self.response.status_code, self.response.content)
        return json.loads(self.response.content)

class PostRequest(BaseRequest):
    def __init__(self, endpoint, **params) -> None:
        self.endpoint = endpoint
        self.params = params

    def perform(self):
        self.response = doPost(self.endpoint, params=self.params)
        if self.response.status_code != 200:
            raise APIException(self.response.status_code, self.response.content)
        return json.loads(self.response.content)