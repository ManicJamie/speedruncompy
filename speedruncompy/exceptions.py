from typing import TYPE_CHECKING

from requests import Response
if TYPE_CHECKING:
    from .api import BaseRequest

class SrcpyException(Exception):
    """speedruncompy found an issue with your request during initialisation (eg. bad arguments)"""

class AuthException(Exception):
    """speedruncompy found an issue within the auth module."""

class APIException(Exception):
    def __init__(self, caller: 'BaseRequest', *args) -> None:
        self.caller = caller
        if isinstance(self.caller.response, Response):
            status = self.caller.response.status_code
        else:
            status = self.caller.response[1]
        super().__init__(status, self.caller.response.content, self.caller, *args)

class ClientException(APIException):
    """There was an issue with your request that the client must handle."""

class BadRequest(ClientException):
    """The server could not recognise your request - fix your request parameters"""

class Unauthorized(ClientException):
    """You are not signed in"""

class Forbidden(ClientException):
    """Your account does not have the privileges to perform this action"""

class NotFound(ClientException):
    """Your request could not locate any matching resource"""

class MethodNotAllowed(ClientException):
    """This endpoint does not accept this HTTP method - try POST"""

class RequestTimeout(ClientException):
    """Server waited too long to receive request. Only called after retries."""
    pass

class RateLimitExceeded(ClientException):
    """Too many requests. You must wait the full timeout period to make any more requests.
      
    Timeout is estimated via direct testing.
    """
    def __init__(self, caller, *args):
        self.timeout = 1500
        super().__init__(caller, *args)

class ServerException(APIException):
    """The server threw a 5xx error code, meaning there was an internal exception. These will trigger retries."""