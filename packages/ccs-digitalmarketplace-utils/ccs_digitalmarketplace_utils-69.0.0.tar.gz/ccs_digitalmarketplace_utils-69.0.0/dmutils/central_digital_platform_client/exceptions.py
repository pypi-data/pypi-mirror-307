from requests import Response

from typing import Optional


class BaseCentralDigitalPlatformHTTPException(Exception):
    status_code: Optional[int] = None
    message: Optional[str] = None

    def __init__(self, response: Response):

        if self.status_code is None:
            error_type = 'Unexpected'
        elif 400 <= self.status_code < 500:
            error_type = "Client"
        elif 500 <= self.status_code < 600:
            error_type = "Server"

        super().__init__(f"{self.status_code} {error_type} Error: {self.message} for url: {response.url}")


class CentralDigitalPlatformHTTPExceptionUnauthorized(BaseCentralDigitalPlatformHTTPException):
    status_code = 401
    message = "Valid authentication credentials are missing in the request"


class CentralDigitalPlatformHTTPExceptionNotFound(BaseCentralDigitalPlatformHTTPException):
    status_code = 404
    message = "Share code not found or the caller is not authorised to use it"


class CentralDigitalPlatformHTTPExceptionInternalServerError(BaseCentralDigitalPlatformHTTPException):
    status_code = 500
    message = "Internal server error"


class CentralDigitalPlatformImproperlyConfigured(Exception):
    pass
