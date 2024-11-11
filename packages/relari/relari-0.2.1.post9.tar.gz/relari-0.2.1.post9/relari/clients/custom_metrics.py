from relari.core.exceptions import APIError
from relari.core.type_parser import str_to_type_hint
from relari.core.types import HTTPMethod
from relari.metrics import MetricArgs, MetricDef


class CustomMetricsClient:
    def __init__(self, client) -> None:
        self._client = client
        self._custom_metrics = self._get_custom_metrics()

    def _get_custom_metrics(self):
        response = self._client._request("metrics/custom/", HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get custom metrics", response=response)
        return [
            MetricDef(
                name=metric["name"],
                help=metric["help"],
                args=MetricArgs(
                    base={
                        arg: prop["type"]
                        for arg, prop in metric["args"].items()
                        if not prop["is_ground_truth"]
                    },
                    ground_truth={
                        arg: prop["type"]
                        for arg, prop in metric["args"].items()
                        if prop["is_ground_truth"]
                    },
                ),
            )
            for metric in response.json()
        ]

    def list(self):
        return self._custom_metrics

    def __getitem__(self, name):
        for metric in self._custom_metrics:
            if metric.name == name:
                return metric
        raise KeyError(f"Custom metric '{name}' not found")
