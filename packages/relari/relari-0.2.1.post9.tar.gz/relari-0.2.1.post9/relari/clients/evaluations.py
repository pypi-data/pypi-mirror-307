import json
from collections import defaultdict
from typing import Any, Dict, List, Optional

from relari.core.exceptions import APIError
from relari.core.types import DatasetDatum, HTTPMethod
from relari.metrics import Metric, MetricDef


class EvaluationResults:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.dataset = data["dataset"]
        self.metadata = data["metadata"]
        self.status = data["status"]
        self.error_info = data["error_info"]
        self.results = data["results"]

    def __getitem__(self, uid: str):
        for k, v in self.results.items():
            if k == uid:
                return v["metrics"]
        return None

    @property
    def metric_results(self):
        return [x["metrics"] for x in self.results.values()]

    def averages(self):
        sums = defaultdict(float)
        counts = defaultdict(int)
        for d in self.metric_results:
            for key, value in d.items():
                sums[key] += value
                counts[key] += 1
        averages = {key: sums[key] / counts[key] for key in sums}
        return averages

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dataset": self.dataset,
            "metadata": self.metadata,
            "status": self.status,
            "error_info": self.error_info,
            "results": self.results,
        }


class EvaluationsClient:
    def __init__(self, client):
        self._client = client

    def list(self, project_id: str):
        endpoint = f"projects/{project_id}/experiments/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to list evaluations", response=response)
        return response.json()

    def get(self, experiment_id: str) -> EvaluationResults:
        endpoint = f"projects/experiments/{experiment_id}/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get evaluation", response=response)
        return EvaluationResults(response.json())

    def delete(self, experiment_id: str):
        endpoint = f"projects/experiments/{experiment_id}/"
        response = self._client._request(endpoint, HTTPMethod.DELETE)
        if response.status_code != 204:
            raise APIError(message="Failed to delete evaluation", response=response)

    def find(self, project_id: str, name: str):
        lst = self.list(project_id)
        out = list()
        name_ = name.strip()
        for d in lst:
            if d["name"].strip() == name_:
                out.append(d)
        if len(out) == 0:
            return None
        return out

    def find_one(self, project_id: str, name: str):
        lst = self.list(project_id)
        name_ = name.strip()
        for d in lst:
            if d["name"].strip() == name_:
                return d
        return None

    def compute_metrics(self, experiment_id: str, pipeline: List[Metric]):
        if not all(isinstance(m, (Metric, MetricDef)) for m in pipeline):
            raise ValueError("metrics must be a list of Metric")
        payload = {"pipeline": [metric.value for metric in pipeline]}
        endpoint = f"projects/experiments/{experiment_id}/compute_metrics/"
        res = self._client._request(endpoint, HTTPMethod.POST, data=json.dumps(payload))
        if res.status_code != 200:
            raise APIError(message="Failed to submit evaluation", response=res)
        return True

    def submit(
        self,
        project_id: str,
        name: Optional[str],
        pipeline: List[Metric],
        data: List[Dict[str, Any]],
        dataset: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = dict(),
    ):
        if not all(isinstance(m, (Metric, MetricDef)) for m in pipeline):
            raise ValueError("pipeline must be a list of Metric")
        if dataset is not None:
            if not all(isinstance(d, DatasetDatum) for d in data):
                raise ValueError(
                    "data must be a list of DatasetDatum if dataset is provided"
                )
            for metric in pipeline:
                [metric.args.validate(x.data, with_optional=False) for x in data]
            data_ = [x.asdict() for x in data]
        else:
            for metric in pipeline:
                [metric.args.validate(x, with_optional=True) for x in data]
            data_ = data
        endpoint = f"projects/{project_id}/experiments/"
        payload = {
            "name": name,
            "pipeline": [metric.value for metric in pipeline],
            "data": data_,
            "dataset": dataset,
            "metadata": metadata,
        }
        res = self._client._request(endpoint, HTTPMethod.POST, data=json.dumps(payload))
        if res.status_code != 200:
            raise APIError(message="Failed to submit evaluation", response=res)
        return res.json()

    def get_progress(self, experiment_id: str) -> dict:
        endpoint = f"projects/experiments/{experiment_id}/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get evaluation", response=response)

        status = response.json()["status"]

        out = {
            "status": status,
            "eta": None,
            "progress": None,
            "total": None,
            "completed": None,
        }

        response = self._client._request(f"{endpoint}/progress/", HTTPMethod.GET)
        if response.status_code == 200:
            body = response.json()
            out["eta"] = round(body.get("eta", 0)) if body.get("eta") else None
            out["progress"] = (
                f"{body.get('completed', 0)/body['total'] * 100:.2f}%"
                if body.get("total")
                else None
            )
            out["total"] = body.get("total")
            out["completed"] = body.get("completed")

        return out
