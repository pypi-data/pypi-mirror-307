import json
from typing import Dict, List, Union

from relari.core.exceptions import APIError
from relari.core.types import DatasetDatum, HTTPMethod, MetricsArgs
from relari.metrics import Metric, MetricDef


class MetricsClient:
    def __init__(self, client) -> None:
        self._client = client

    def list(self):
        return [MetricDef(name=k.name, help="N/A", args=k.args) for k in Metric]

    def compute(
        self, metric: Union[Metric, MetricDef], args: Union[MetricsArgs, List[MetricsArgs]], **kwargs
    ):
        if not isinstance(metric, (Metric, MetricDef)):
            raise ValueError("metric must be a Metric")
        if not isinstance(args, (DatasetDatum, Dict, list)):
            raise ValueError(
                "args must be a DatasetDatum, Dict, or list of DatasetDatum or Dict"
            )
        if isinstance(args, list):
            return self._batch_compute(metric, args, **kwargs)
        else:
            return self._compute(metric, args, **kwargs)

    def _compute(self, metric: Union[Metric, MetricDef], args: MetricsArgs, **kwargs):
        # Version 1: metric_name, dataset, and label (datum uid)
        if "dataset" in kwargs and isinstance(args, DatasetDatum):
            metric.args.validate(args.data, with_optional=False)
            endpoint = "metrics/dataset/"
            payload = {
                "metric": metric.value,
                "dataset": kwargs["dataset"],
                "uid": args.label,
                "kwargs": args.data,
            }
        # Version 2: metric_name and args
        elif isinstance(args, Dict):
            metric.args.validate(args, with_optional=True)
            endpoint = "metrics/"
            payload = {
                "metric": metric.value,
                "kwargs": args,
            }
        else:
            raise ValueError("Invalid arguments provided to run_metric.")
        response = self._client._request(
            endpoint, HTTPMethod.POST, data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise APIError(message="Failed to run metric", response=response)
        return response.json()

    def _batch_compute(
        self,
        metric: Metric,
        args: List[MetricsArgs],
        **kwargs,
    ):
        if not isinstance(args, list):
            raise ValueError("args must be a list of DatasetDatum or Dict")
        num_datums = len(args)
        if num_datums == 0:
            raise ValueError("args must contain at least one DatasetDatum or Dict")
        if "LLMBased" in metric.value and self._client.timeout < 4 * num_datums:
            raise ValueError(
                f"This is a synchronous metric, please increase the timeout for LLM based metrics (suggested {6*num_datums}) or reduce batch size."
            )
        # Mode 1: DatasetDatum
        if "dataset" in kwargs and isinstance(args[0], DatasetDatum):
            [metric.args.validate(x.data, with_optional=False) for x in args]
            endpoint = "metrics/dataset/batch/"
            payload = {
                "metric": metric.value,
                "dataset": kwargs["dataset"],
                "kwargs": [x.asdict() for x in args],
            }
        else:
            [metric.args.validate(x, with_optional=True) for x in args]
            endpoint = "metrics/batch/"
            payload = {
                "metric": metric.value,
                "kwargs": args,
            }
        response = self._client._request(
            endpoint, HTTPMethod.POST, data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise APIError(message="Failed to run metric", response=response)
        return response.json()
