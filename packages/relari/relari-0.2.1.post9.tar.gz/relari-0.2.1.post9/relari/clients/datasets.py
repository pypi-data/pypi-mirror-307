import tempfile
from pathlib import Path

from relari.core.dataset import Dataset
from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod


class DatasetClient:
    def __init__(self, client):
        self._client = client

    def list(self, project_id: str):
        endpoint = f"projects/{project_id}/datasets/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message=f"Project {project_id} not found", response=response)
        return response.json()

    def create(self, project_id: str, dataset: Dataset):
        if not dataset.name:
            raise ValueError("Dataset name is required, please set dataset.name")
        endpoint = f"projects/{project_id}/datasets/"
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            dataset.save(out_dir / "dataset.jsonl", save_manifest=True)
            with open(out_dir / "dataset.jsonl", "rb") as data_file, open(
                out_dir / "manifest.yaml", "rb"
            ) as manifest_file:
                files = {
                    "data": ("dataset.jsonl", data_file, "application/x-ndjson"),
                    "manifest": ("manifest.yaml", manifest_file, "application/x-yaml"),
                }
                response = self._client._request(endpoint, HTTPMethod.POST, files=files)
        body = response.json()
        if response.status_code != 200:
            msg = f"Project {project_id} not found"
            msg = f"{msg}: {body['detail']}" if "detail" in body else msg
            raise Exception(msg)
        return response.json()

    def delete(self, dataset_id: str):
        response = self._client._request(
            f"projects/datasets/{dataset_id}", HTTPMethod.DELETE
        )
        if response.status_code != 204:
            raise APIError(message="Failed to delete dataset", response=response)

    def get(self, dataset_id: str):
        response = self._client._request(
            f"projects/datasets/{dataset_id}", HTTPMethod.GET
        )
        if response.status_code != 200:
            raise ValueError(f"Dataset {dataset_id} not found")
        return Dataset.from_data(response.json()["data"], response.json()["manifest"])

    def find(self, proj_id: str, name: str):
        lst = self.list(proj_id)
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
