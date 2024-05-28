import base64, json
import logging
import asyncio, aiohttp
import sys
import random
from typing import Awaitable, Callable, Any, Generic, TypeVar

from yarl import URL
from copy import copy

from .datatypes import Datatype, LenientDatatype, Pagination
from .exceptions import *

API_ROOT = "/api/v2/"
LANG = "en"
ACCEPT = "application/json"
DEFAULT_USER_AGENT = "speedruncompy/"

_log = logging.getLogger("speedruncompy")


class SpeedrunClient():
    """Api class. Holds a unique PHPSESSID and user_agent, as well as its own logger."""
    
    _session: aiohttp.ClientSession | None
    cookie_jar: aiohttp.CookieJar | None
    """An asyncio CookieJar. Constructed on first entry to an async context."""
    loose_cookies: dict[str, str]
    """Cookies before jar construction."""
    _header: dict[str, str]
    
    def __init__(self, user_agent: str | None = None, PHPSESSID: str | None = None) -> None:
        self.cookie_jar = None
        self._session = None
        self.loose_cookies = {}
        if PHPSESSID is not None:
            self.loose_cookies["PHPSESSID"] = PHPSESSID
        self._header = {"Accept-Language": LANG, "Accept": ACCEPT,
                        "User-Agent": f"{DEFAULT_USER_AGENT}{user_agent}"}
        self._log = _log if user_agent is None else _log.getChild(user_agent)
    
    async def __aenter__(self):
        self._session = await (await self._construct_session()).__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session is None: return
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None
    
    async def _construct_session(self):
        if self.cookie_jar is None:
            self.cookie_jar = aiohttp.CookieJar()
            self.cookie_jar.update_cookies(self.loose_cookies)
        return aiohttp.ClientSession(base_url="https://www.speedrun.com", cookie_jar=self.cookie_jar, headers=self._header,
                                     json_serialize=lambda o: json.dumps(o, separators=(",", ":")))

    def _get_PHPSESSID(self) -> str | None:
        if self.cookie_jar is None: return self.loose_cookies.get("PHPSESSID", None)
        cookie = self.cookie_jar.filter_cookies(URL("/")).get("PHPSESSID")
        return None if cookie is None else cookie.value

    def _set_PHPSESSID(self, phpsessid):
        if self.cookie_jar is not None:
            self.cookie_jar.update_cookies({"PHPSESSID": phpsessid})
        else:
            self.loose_cookies.update({"PHPSESSID": phpsessid})
    
    PHPSESSID = property(_get_PHPSESSID, _set_PHPSESSID)
    """Login token. Set by `PutAuthLogin`, or you may set it manually to a logged in session."""

    @staticmethod
    def _encode_r(params: dict):
        """Encodes a parameter dict into url-base64 encoded min-json, ready for use as `_r` in a GET URL."""
        paramsjson = bytes(json.dumps(params, separators=(",", ":")).strip(), "utf-8")
        return base64.urlsafe_b64encode(paramsjson).replace(b"=", b"").decode()

    async def do_get(self, endpoint: str, params: dict = {}) -> tuple[bytes, int]:
        self._log.debug(f"GET {endpoint} w/ params {params}")
        
        session = self._session
        if session is None:
            session = await (await self._construct_session()).__aenter__()
        
        try:
            async with session.get(url=f"{API_ROOT}{endpoint}", params={"_r": self._encode_r(params)}) as response:
                out = (await response.read(), response.status)
        except Exception as e:
            raise e
        else:
            return out
        finally:
            if self._session is None:
                await session.__aexit__(*sys.exc_info())
    
    async def do_post(self, endpoint: str, params: dict = {}) -> tuple[bytes, int]:
        self._log.debug(f"POST {endpoint} w/ params {params}")
        
        session = self._session
        if session is None:
            session = await (await self._construct_session()).__aenter__()
        
        try:
            async with session.post(url=f"{API_ROOT}{endpoint}", json=params) as response:
                out = (await response.read(), response.status)
        except Exception as e:
            raise e
        else:
            return out
        finally:
            if self._session is None:
                await session.__aexit__(*sys.exc_info())


_default = SpeedrunClient()


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
        return p["pagination"]  # type:ignore
    
    @staticmethod
    def _combine_keys(pages: dict[int, R], main_keys: list[str], merge_keys: list[str]) -> R:
        """Merge multiple pages. `main_keys` are appended, `merge_keys` are deduplicated by id."""
        accumulator: R = copy(pages[1])
        accuDicts: dict[str, dict[str, Datatype]] = {key: dict() for key in merge_keys}
        
        iterator = iter(pages.items())
        next(iterator)  # skip first page (already in accumulator)
        for i, p in iterator:
            for main_key in main_keys:
                accumulator[main_key] += p[main_key]  # type: ignore
            for key in merge_keys:
                if p[key] is not None:  # Guard against None fields
                    accuDicts[key].update({item["id"]: item for item in p[key]})  # type: ignore
        
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
        numpages: int = self._get_pagination(self.pages[1])["pages"]  # type: ignore
        if max_pages >= 1:
            numpages = min(numpages, max_pages)
        if numpages > 1:
            results = await asyncio.gather(*[self.perform_async(retries, delay, vary=vary, page=p, **kwargs) for p in range(2, numpages + 1)])
            self.pages.update({p + 2: result for p, result in enumerate(results)})
        return self.pages


class GetRequest(BaseRequest[R], Generic[R]):
    def __init__(self, endpoint, returns: type = LenientDatatype, _api: SpeedrunClient | None = None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_get, endpoint=endpoint, returns=returns, **params)


class PostRequest(BaseRequest[R], Generic[R]):
    def __init__(self, endpoint, returns: type = LenientDatatype, _api: SpeedrunClient | None = None, **params) -> None:
        if _api is None: _api = _default
        super().__init__(method=_api.do_post, endpoint=endpoint, returns=returns, **params)
