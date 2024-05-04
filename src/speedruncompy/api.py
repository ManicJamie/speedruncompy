import base64, json
import logging
import asyncio, aiohttp
import random
from typing import Awaitable, Callable, Any, Generic, TypeVar

from yarl import URL
from copy import copy

from .datatypes import Datatype, srcpyJSONEncoder, LenientDatatype, Pagination
from .exceptions import *

API_URI = "https://www.speedrun.com/api/v2/"
LANG = "en"
ACCEPT = "application/json"
DEFAULT_USER_AGENT = "speedruncompy/"

_log = logging.getLogger("speedruncompy")


class SpeedrunComPy():
    """Api class. Holds a unique PHPSESSID and user_agent, as well as its own logger."""
    def __init__(self, user_agent: str | None = None) -> None:
        self.cookie_jar = aiohttp.CookieJar()
        self._header = {"Accept-Language": LANG, "Accept": ACCEPT, "User-Agent": f"{DEFAULT_USER_AGENT}{user_agent}"}
        if user_agent is None:
            self._log = _log
        else:
            self._log = _log.getChild(user_agent)

    def _get_PHPSESSID(self) -> str | None:
        cookie = self.cookie_jar.filter_cookies(URL("/")).get("PHPSESSID")
        return None if cookie is None else cookie.value

    def _set_PHPSESSID(self, phpsessid):
        self.cookie_jar.update_cookies({"PHPSESSID": phpsessid})
    
    PHPSESSID = property(_get_PHPSESSID, _set_PHPSESSID)
    """Login token. Set by `PutAuthLogin`, or you may set it manually to a logged in session."""

    @staticmethod
    def _encode_r(params: dict):
        """Encodes a parameter dict into url-base64 encoded min-json, ready for use as `_r` in a GET URL."""
        paramsjson = bytes(json.dumps(params, separators=(",", ":"), cls=srcpyJSONEncoder).strip(), "utf-8")
        return base64.urlsafe_b64encode(paramsjson).replace(b"=", b"").decode()

    async def do_get(self, endpoint: str, params: dict = {}) -> tuple[bytes, int]:
        # Params passed to the API by the site are json-base64 encoded, even though std params are supported.
        # We will do the same in case param support is retracted.
        self._log.debug(f"GET {endpoint} w/ params {params}")
        async with aiohttp.ClientSession(headers=self._header, cookie_jar=self.cookie_jar) as session:
            async with session.get(url=f"{API_URI}{endpoint}", params={"_r": self._encode_r(params)}) as response:
                return (await response.read(), response.status)
        
    async def do_post(self, endpoint: str, params: dict = {}, _setCookie=True) -> tuple[bytes, int]:
        # Construct a dummy jar if we wish to ignore Set_Cookie responses (only on PutAuthLogin and PutAuthSignup)
        if _setCookie: liveJar = self.cookie_jar
        else:
            liveJar = aiohttp.CookieJar()
            liveJar.update_cookies(self.cookie_jar._cookies)
        self._log.debug(f"POST {endpoint} w/ params {params}")
        async with aiohttp.ClientSession(json_serialize=lambda o: json.dumps(o, separators=(",", ":"), cls=srcpyJSONEncoder),
                                         headers=self._header, cookie_jar=liveJar) as session:
            async with session.post(url=f"{API_URI}{endpoint}", json=params) as response:
                return (await response.read(), response.status)


_default = SpeedrunComPy()


def set_default_PHPSESSID(phpsessionid):
    _default.PHPSESSID = phpsessionid


R = TypeVar('R', bound=Datatype)


class BaseRequest(Generic[R]):
    def __init__(self,
                 method: Callable[[str, dict[str, Any]], Awaitable[tuple[bytes, int]]],
                 endpoint: str,
                 returns: type[R],
                 **params):
        self.method = method
        self.endpoint = endpoint
        self.params = params
        self.return_type = returns
    
    def update_params(self, **kwargs):
        """Updates parameters using values set in kwargs"""
        self.params.update(kwargs)

    def perform(self, retries=5, delay=1, autovary=False, **kwargs) -> R:
        """Synchronously perform the request.
        
        NB: This uses its own event loop, so if using `asyncio` use `perform_async()` instead."""
        try:
            return asyncio.run(self.perform_async(retries, delay, autovary, **kwargs))
        except RuntimeError:
            raise AIOException("Synchronous interface called from asynchronous context - use `await perform_async` instead.") from None
    
    async def perform_async(self, retries=5, delay=1, autovary=False, **kwargs) -> R:
        """Asynchronously perform the request. Remember to `await` me!"""
        if autovary is True: kwargs |= {"vary": random.randint(1, 1000000000)}
        self.response = await self.method(self.endpoint, self.params | kwargs)
        content = self.response[0]
        status = self.response[1]

        if (status >= 500 and status <= 599) or status == 408:
            if retries > 0:
                _log.error(f"SRC returned error {status} {content!r}. Retrying with delay {delay}:")
                for attempt in range(0, retries + 1):
                    self.response = await self.method(self.endpoint, self.params)
                    content = self.response[0]
                    status = self.response[1]
                    if not (status >= 500 and status <= 599) or status == 408:
                        break
                    _log.error(f"Retry {attempt} returned error {status} {content!r}")
                    await asyncio.sleep(delay)
                else:
                    if status == 408: raise RequestTimeout(self)
                    else: raise ServerException(self)
        
        match status:
            case 400: raise BadRequest(self)
            case 401: raise Unauthorized(self)
            case 403: raise Forbidden(self)
            case 404: raise NotFound(self)
            case 405: raise MethodNotAllowed(self)
            case 408: raise RequestTimeout(self)
            case 429: raise RateLimitExceeded(self)

        if (status >= 500 and status <= 599): raise ServerException(self)

        if status < 200 or status > 299:
            _log.error(f"Unknown response error returned from SRC! {status} {self.response[0]!r}")
            raise APIException(self)

        return self.return_type(json.loads(content.decode()))


class BasePaginatedRequest(BaseRequest[R], Generic[R]):
    def _combine_results(self, pages: dict[int, R]) -> R:
        raise NotImplementedError(f"perform_all or perform_all_async on {type(self).__name__} is NOT yet implemented! Use _perform_all_raw() or _perform_all_async_raw()")

    def _get_pagination(self, p: R) -> Pagination:
        """Locates the pagination object on a response. Overriden on certain subclasses."""
        return p["pagination"]
    
    @staticmethod
    def _combine_keys(pages: dict[int, R], main_keys: list[str], merge_keys: list[str]) -> R:
        """Merge multiple pages. `main_keys` are appended, `merge_keys` are deduplicated by id."""
        accumulator: R = copy(pages[1])
        accuDicts: dict[str, dict[str, Datatype]] = {key: dict() for key in merge_keys}
        
        iterator = iter(pages.items())
        next(iterator)  # skip first page (already in accumulator)
        for i, p in iterator:
            for main_key in main_keys:
                accumulator[main_key] += p[main_key]
            for key in merge_keys:
                if p[key] is None: continue  # Guard against None fields
                accuDicts[key].update({item["id"]: item for item in p[key]})
        
        for key in merge_keys:
            accumulator[key] = list(accuDicts[key].values())
        
        return accumulator
    
    def perform_all(self, retries=5, delay=1, autovary=False, max_pages=0, **kwargs) -> R:
        """Returns a combined dict of all pages. `pagination` is removed."""
        pages = self._perform_all_raw(retries, delay, autovary, max_pages, **kwargs)
        return self._combine_results(pages)
    
    def _perform_all_raw(self, retries=5, delay=1, autovary=False, max_pages=0, **kwargs) -> dict[int, R]:
        """Get all pages and return a dict of {pageNo : pageData}."""
        try:
            return asyncio.run(self._perform_all_async_raw(retries, delay, autovary, max_pages, **kwargs))
        except RuntimeError:
            raise AIOException("Synchronous interface called from asynchronous context - use `await perform_async` instead.") from None
    
    async def perform_all_async(self, retries=5, delay=1, autovary=False, max_pages=0, **kwargs) -> R:
        """Returns a combined dict of all pages. `pagination` is removed."""
        pages = await self._perform_all_async_raw(retries, delay, autovary, max_pages, **kwargs)
        return self._combine_results(pages)
    
    async def _perform_all_async_raw(self, retries=5, delay=1, autovary=False, max_pages=0, **kwargs) -> dict[int, R]:
        """Get all pages and return a dict of {pageNo : pageData}."""
        self.pages: dict[int, R] = {}
        vary = 0 if not autovary else random.randint(1, 1000000000)
        self.pages[1] = await self.perform_async(retries, delay, page=1, vary=vary, **kwargs)
        numpages = self._get_pagination(self.pages[1])["pages"]
        if max_pages >= 1:
            numpages = min(numpages, max_pages)
        if numpages > 1:
            results = await asyncio.gather(*[self.perform_async(retries, delay, vary=vary, page=p, **kwargs) for p in range(2, numpages + 1)])
            self.pages.update({p + 2: result for p, result in enumerate(results)})
        return self.pages


class GetRequest(BaseRequest[R], Generic[R]):
    def __init__(self, endpoint, returns: type = LenientDatatype, _api: SpeedrunComPy | None = None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_get, endpoint=endpoint, returns=returns, **params)


class PostRequest(BaseRequest[R], Generic[R]):
    def __init__(self, endpoint, returns: type = LenientDatatype, _api: SpeedrunComPy | None = None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_post, endpoint=endpoint, returns=returns, **params)
