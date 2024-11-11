import os
import urllib

import requests
from dotenv import load_dotenv

from relari import clients 
from relari.core.types import HTTPMethod

load_dotenv()

class RelariClient:
    def __init__(self, api_key: str = None, api_url: str = "https://api.relari.ai/v2/"):
        self.api_url = os.getenv("RELARI_URL", api_url)
        self.api_key = os.getenv("RELARI_API_KEY", api_key)
        if self.api_key is None:
            raise ValueError(
                "Please set the environment variable RELARI_API_KEY or pass it as an argument."
            )
        self.timeout = 10
        self.valid = self._validate()

        self.datasets = clients.DatasetClient(self)
        self.projects = clients.ProjectsClient(self)
        self.evaluations = clients.EvaluationsClient(self)
        self.metrics = clients.MetricsClient(self)
        self.custom_metrics = clients.CustomMetricsClient(self)
        self.usage = clients.UsageClient(self)
        self.prompts = clients.PromptOptimizationClient(self)
        self.synth = clients.SyntheticDataClient(self)

    def _request(self, endpoint: str, method: HTTPMethod, **kwargs):
        url = urllib.parse.urljoin(self.api_url, endpoint)
        url = url if url.endswith("/") else f"{url}/"
        headers = {"X-API-Key": self.api_key}
        if "files" not in kwargs:
            headers["Content-Type"] = "application/json"
        request_fcn = getattr(requests, method)
        try:
            response = request_fcn(url, headers=headers, timeout=self.timeout, **kwargs)
        except requests.exceptions.Timeout:
            if endpoint == "status":
                raise Exception("Server is unreachable")
            elif endpoint == "auth":
                if not self.status():
                    raise Exception("Server is unreachable")
                raise Exception("Request timed out while trying to validate API key")
            else:
                raise Exception("Request timed out")
        return response

    def status(self):
        response = self._request("status", HTTPMethod.GET)
        if response.status_code != 200:
            return False
        return True

    def _validate(self):
        response = self._request("auth", HTTPMethod.GET)
        if response.status_code != 200:
            raise RuntimeError(response.json()["detail"])
        return True
