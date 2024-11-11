from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod


class UsageClient:
    def __init__(self, client) -> None:
        self._client = client

    def get_current(self):
        endpoint = "usage/current/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get current usage", response=response)
        return response.json()
    
    def get_history(self):
        endpoint = "usage/history/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get usage history", response=response)
        return response.json()