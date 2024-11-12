import logging
import requests
import urllib.parse as urlparse

from enum import Enum
from requests import HTTPError
from flask import Flask

from typing import Optional, Any, Type
from logging import Logger

from .exceptions import (
    BaseCentralDigitalPlatformHTTPException,
    CentralDigitalPlatformHTTPExceptionUnauthorized,
    CentralDigitalPlatformHTTPExceptionNotFound,
    CentralDigitalPlatformHTTPExceptionInternalServerError,
    CentralDigitalPlatformImproperlyConfigured
)


class CentralDigitalPlatformURL(Enum):
    GET_SHARED_DATA = '/share/data/{share_code}'
    VERIFY_SHARED_DATA = '/share/data/verify'


class HTTPMethod(Enum):
    GET = 'get'
    POST = 'post'


# This class is based off the API client for DMP as well as the Direct Plus client
class CentralDigitalPlatformClient(object):
    REQUEST_TIMEOUT = (15, 45,)

    def init_app(self, app: Flask):
        self._base_url = app.config['DM_CENTRAL_DIGITAL_PLATFORM_API_URL']
        self._api_key = app.config['DM_CENTRAL_DIGITAL_PLATFORM_API_KEY']

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        logger: Optional[Logger] = None
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._logger = logger if logger else logging.getLogger(__name__)

    def _log_and_raise_exception(self, exception: Exception, message: Optional[str] = None):
        self._logger.error(message if message else str(exception))
        raise exception

    def _check_configuration(self):
        exception = None

        if self._base_url is None:
            exception = CentralDigitalPlatformImproperlyConfigured(
                f"{self.__class__.__name__} has no URL configured"
            )
        elif self._api_key is None:
            exception = CentralDigitalPlatformImproperlyConfigured(
                f"{self.__class__.__name__} has no API Key configured"
            )

        if exception:
            self._log_and_raise_exception(exception)

    def _build_url(self, url: str):
        return urlparse.urljoin(self._base_url, url)

    def _request(
        self,
        method: HTTPMethod,
        url: str,
        data: Optional[dict[str, Any]] = None
    ):
        self._check_configuration()

        url = self._build_url(url)
        headers = {
            "Content-type": "application/json",
            "accept": "application/json",
            "CDP-Api-Key": self._api_key
        }

        if method != HTTPMethod.GET:
            response = getattr(requests, method.value)(url, headers=headers, json=data, timeout=self.REQUEST_TIMEOUT)
        else:
            response = requests.get(url, headers=headers, timeout=self.REQUEST_TIMEOUT)

        try:
            response.raise_for_status()
        except (HTTPError, BaseCentralDigitalPlatformHTTPException) as exception:
            central_digital_platform_exception: Optional[Type[BaseCentralDigitalPlatformHTTPException]] = None

            if response.status_code == CentralDigitalPlatformHTTPExceptionUnauthorized.status_code:
                central_digital_platform_exception = CentralDigitalPlatformHTTPExceptionUnauthorized
            elif response.status_code == CentralDigitalPlatformHTTPExceptionNotFound.status_code:
                central_digital_platform_exception = CentralDigitalPlatformHTTPExceptionNotFound
            elif response.status_code == CentralDigitalPlatformHTTPExceptionInternalServerError.status_code:
                central_digital_platform_exception = CentralDigitalPlatformHTTPExceptionInternalServerError

            if central_digital_platform_exception is not None:
                exception = central_digital_platform_exception(response)

            self._log_and_raise_exception(exception)

        try:
            response_json = response.json()
        except ValueError as exception:
            self._log_and_raise_exception(
                exception,
                f"Unable to parse Central Digital Platform API response: {response}: {exception}"
            )

        return response_json

    def get_shared_data(self, share_code: str):
        return self._request(
            HTTPMethod.GET,
            CentralDigitalPlatformURL.GET_SHARED_DATA.value.format(
                share_code=share_code
            )
        )

    def verify_shared_data(self, share_code: str, form_version_id: str):
        return self._request(
            HTTPMethod.POST,
            CentralDigitalPlatformURL.VERIFY_SHARED_DATA.value,
            {
                "shareCode": share_code,
                "formVersionId": form_version_id
            }
        )
