import base64, json
from .exceptions import *
import logging
import asyncio, aiohttp
from time import sleep
from typing import Awaitable, Callable, Any, Optional

API_URI = "https://www.speedrun.com/api/v2/"
LANG = "en"
ACCEPT = "application/json"
DEFAULT_USER_AGENT = "speedruncompy/"

_log = logging.getLogger("speedruncompy")

class SpeedrunComPy():
    """Api class. Holds a unique PHPSESSID and user_agent, as well as its own logger."""
    def __init__(self, user_agent = None) -> None:
        self.cookie_jar = {}
        self.user_agent = user_agent
        if user_agent is None:
            self._log = _log
        else:
            self._log = _log.getChild(user_agent)
    
    def set_phpsessid(self, phpsessid):
        self.cookie_jar.update({"PHPSESSID": phpsessid})

    async def do_get(self, endpoint: str, params: dict = {}) -> tuple[bytes, int]:
        _header = {"Accept-Language": LANG, "Accept": ACCEPT, "User-Agent": f"{DEFAULT_USER_AGENT}{self.user_agent}"}
        # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
        # We will do the same in case param support is retracted.
        paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
        _r = base64.urlsafe_b64encode(paramsjson).replace(b"=", b"").decode()
        self._log.debug(f"async GET {API_URI}{endpoint} w/ params {paramsjson}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{API_URI}{endpoint}", headers=_header, params={"_r": _r}) as response:
                return (await response.read(), response.status)
        
    async def do_post(self, endpoint:str, params: dict = {}, _setCookie=True) -> tuple[bytes, int]:
        _header = {"Accept-Language": LANG, "Accept": ACCEPT, "User-Agent": f"{DEFAULT_USER_AGENT}{self.user_agent}"}
        self._log.debug(f"async POST {API_URI}{endpoint} w/ params {params}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{API_URI}{endpoint}", headers=_header,
                                    cookies=self.cookie_jar, json=params) as response:
                if _setCookie and response.cookies:
                    self.cookie_jar.update(response.cookies)
                return (await response.read(), response.status) 

_default = SpeedrunComPy()

def set_default_PHPSESSID(phpsessionid):
    _default.cookie_jar.update({"PHPSESSID": phpsessionid})

class BaseRequest():
    def __init__(self, 
                 method: Callable[[str, dict[str, Any]], Awaitable[tuple[bytes, int]]],
                 endpoint: str, 
                 **params):
        self.method = method
        self.endpoint = endpoint
        self.params = params
    
    def update_params(self, **kwargs):
        """Updates parameters using values set in kwargs"""
        self.params.update(kwargs)

    def perform(self, retries=5, delay=1, **kwargs) -> dict:
        try:
            return asyncio.run(self.perform_async(retries, delay, **kwargs))
        except RuntimeError as e:
            raise AIOException("Synchronous interface called from asynchronous context - use `await perform_async` instead.") from None
    
    async def perform_async(self, retries=5, delay=1, **kwargs) -> dict:
        self.response = await self.method(self.endpoint, self.params | kwargs)
        content = self.response[0]
        status = self.response[1]

        if (status >= 500 and status <= 599) or status == 408:
            if retries > 0:
                _log.error(f"SRC returned error {status} {content}. Retrying with delay {delay}:")
                for attempt in range(0, retries+1):
                    self.response = await self.method(self.endpoint, self.params)
                    content = self.response[0]
                    status = self.response[1]
                    if not (status >= 500 and status <= 599) or status == 408: 
                        break
                    _log.error(f"Retry {attempt} returned error {status} {content}")
                    await asyncio.sleep(delay)
                else:
                    if status == 408: raise RequestTimeout(self)
                    else: raise ServerException(self)
        
        if status == 400: raise BadRequest(self)
        if status == 401: raise Unauthorized(self)
        if status == 403: raise Forbidden(self)
        if status == 404: raise NotFound(self)
        if status == 405: raise MethodNotAllowed(self)
        if status == 408: raise RequestTimeout(self)
        if status == 429: raise RateLimitExceeded(self)

        if (status >= 500 and status <= 599): raise ServerException(self)

        if status < 200 or status > 299:
            _log.error(f"Unknown response error returned from SRC! {status} {self.response[0]}")
            raise APIException(self)

        return json.loads(content.decode())

class BasePaginatedRequest(BaseRequest):
    def _combine_results(self, pages: dict):
        _log.warning(f"""perform_all or perform_all_async on {type(self).__name__} is NOT yet implemented!
                     
                     Use _perform_all_raw() or _perform_all_async_raw() to protect against future updates.""")
        return pages

    def perform_all(self, retries=5, delay=1) -> dict:
        """Returns a combined dict of all pages. `pagination` is removed."""
        pages = self._perform_all_raw(retries, delay)
        return self._combine_results(pages)
    
    def _perform_all_raw(self, retries=5, delay=1):
        """Get all pages and return a dict of {pageNo : pageData}."""
        try:
            return asyncio.run(self._perform_all_async_raw(retries, delay))
        except RuntimeError as e:
            raise AIOException("Synchronous interface called from asynchronous context - use `await perform_async` instead.") from None
    
    async def perform_all_async(self, retries=5, delay=1) -> dict:
        """Returns a combined dict of all pages. `pagination` is removed."""
        pages = await self._perform_all_async_raw(retries, delay)
        return self._combine_results(pages)
    
    async def _perform_all_async_raw(self, retries=5, delay=1):
        """Get all pages and return a dict of {pageNo : pageData}."""
        self.pages = {}
        self.pages[1] = await self.perform_async(retries, delay, page=1)
        numpages = self.pages[1]["pagination"]["pages"]
        if numpages > 1:
            results = await asyncio.gather(*[self.perform_async(retries, delay, page=p) for p in range(2, numpages + 1)])
            self.pages.update({p + 2:result for p, result in enumerate(results)})
        return self.pages

class GetRequest(BaseRequest):
    def __init__(self, endpoint, _api:SpeedrunComPy=None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_get, endpoint=endpoint, **params)

class PostRequest(BaseRequest):
    def __init__(self, endpoint, _api:SpeedrunComPy=None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_post, endpoint=endpoint, **params)
