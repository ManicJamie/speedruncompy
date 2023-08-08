from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .api import BaseRequest

class APIException(Exception):
    def __init__(self, caller: 'BaseRequest', *args) -> None:
        self.caller = caller
        super().__init__(self.caller.response.status_code, self.caller.response.content, self.caller, *args)

class ClientException(APIException):
    """There was an issue with your request that the client must handle."""

class BadRequest(ClientException):
    pass

class Unauthorized(ClientException):
    pass

class Forbidden(ClientException):
    pass

class NotFound(ClientException):
    pass

class MethodNotAllowed(ClientException):
    pass

class RequestTimeout(ClientException):
    """Server waited too long to receive request. This should probably be retryable."""
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