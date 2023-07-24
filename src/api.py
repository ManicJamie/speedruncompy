import requests, base64, json

apiURI = "https://www.speedrun.com/api/v2/"
phpSESSID = ""
LANG = "en"
ACCEPT = "application/json"

def doRequest(endpoint: str, params: dict = {}, method = "GET"):
    _header = {"Accept-Language": LANG}
    _cookies = {"PHPSESSID" : phpSESSID}
    # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
    # We will do the same in case param support is retracted.
    paramsjson = bytes(json.dumps(params, separators=(",", ":")), "utf-8")
    _r = base64.encodebytes(paramsjson).strip().removesuffix(b"==")
    return requests.request(method, url=f"{apiURI}{endpoint}", headers=_header, cookies=_cookies, params={"_r": _r})

class BaseRequest():
    def __init__(self, endpoint, params = {}, method = "GET") -> None:
        self.endpoint = endpoint
        self.params = params
        self.method = method

    def perform(self):
        doRequest(self.endpoint, self.params, self.method)