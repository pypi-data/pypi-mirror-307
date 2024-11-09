import os
from typing import Any, Literal, Optional, Type

import requests
from pydantic import BaseModel


class APIKey:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self._api_key = api_key or os.getenv("SEPAY_API_KEY") or ""
        if not self._api_key:
            raise ValueError("Missing API Key.")


class BaseRequest(APIKey):
    BASE_URL = "https://my.sepay.vn/userapi/"

    class RequestException(Exception):
        def __init__(self, response: requests.Response):
            self.status_code = response.status_code
            self.request_body = response.request.body
            self.method = response.request.method
            self.url = response.request.url
            self.exception_message = f"""
                Request: {self.method} {self.url}:
                    {self.request_body!r}
                Response: {self.status_code}
                    {response.text!r}
            """
            super().__init__(self.exception_message)

    def _make_request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self._api_key,
        }
        url = self.BASE_URL + path
        response = requests.request(method, url, headers=headers, json=body, params=params)

        if response.status_code >= 400:
            raise self.RequestException(response)

        if response.status_code == 204:
            data = {}
        else:
            data = response.json()

        return data

    def _get(
        self,
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        return self._make_request("GET", path, body, params)

    def _post(
        self,
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        return self._make_request("POST", path, body, params)

    def _put(
        self,
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        return self._make_request("PUT", path, body, params)

    def _patch(
        self,
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        return self._make_request("PATCH", path, body, params)

    def _delete(
        self,
        path: str,
        body: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> dict[Any, Any]:
        return self._make_request("DELETE", path, body, params)

    def get_object(self, object_class: Type[BaseModel], data: dict):
        return object_class.model_validate(data)
