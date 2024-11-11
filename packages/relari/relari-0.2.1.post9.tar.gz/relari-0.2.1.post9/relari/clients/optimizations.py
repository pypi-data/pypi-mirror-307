import json
from enum import Enum
from typing import Optional

from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod, Prompt


class PromptOptimizationClient:
    class Metrics(str, Enum):
        CORRECTNESS = "correctness"
        STYLE_CONSISTENCY = "style_consistency"
        ROUGE = "rouge"
        TOKEN_OVERLAP = "token_overlap"
        EXACT_MATCH = "exact_match"
        TONE = "tone"
        SQL_CORRECTNESS = "sql_correctness"

    def __init__(self, client) -> None:
        self._client = client

    def find(self, project_id: str, name: str):
        ls = self.list(project_id)
        _name = name.strip()
        out = list()
        for prompt in ls:
            if prompt["name"].strip() == _name:
                out.append(prompt)
        if len(out) == 0:
            return None
        return out

    def find_one(self, project_id: str, name: str):
        ls = self.list(project_id)
        _name = name.strip()
        for prompt in ls:
            if prompt["name"].strip() == _name:
                return prompt
        return None

    def list(self, project_id: str):
        assert project_id and isinstance(
            project_id, str
        ), "You must provide a valid project ID"
        endpoint = f"projects/{project_id}/prompts/"
        res = self._client._request(endpoint, HTTPMethod.GET)
        if res.status_code != 200:
            raise APIError(message="Failed to list optimization tasks", response=res)
        return res.json()

    def get(self, prompt_id: str):
        assert prompt_id and isinstance(
            prompt_id, str
        ), "You must provide a valid prompt ID"
        endpoint = f"prompts/{prompt_id}/"
        res = self._client._request(endpoint, HTTPMethod.GET)
        if res.status_code != 200:
            raise APIError(message="Failed to get optimization task", response=res)
        return res.json()

    def delete(self, prompt_id: str):
        assert prompt_id and isinstance(
            prompt_id, str
        ), "You must provide a valid prompt ID"
        endpoint = f"prompts/{prompt_id}/"
        res = self._client._request(endpoint, HTTPMethod.DELETE)
        if res.status_code != 204:
            raise APIError(message="Failed to delete optimization task", response=res)

    def optimize(
        self,
        project_id: str,
        dataset_id: str,
        prompt: Prompt,
        llm: str,
        task_description: str,
        metric: Metrics,
        name: Optional[str] = None,
    ):
        assert isinstance(prompt, Prompt), "prompt must be an instance of Prompt"
        assert prompt.is_valid()
        assert llm and isinstance(llm, str), "You must provide a valid LLM"
        assert task_description and isinstance(
            task_description, str
        ), "You must provide a valid task description"
        assert metric and isinstance(
            metric, self.Metrics
        ), "You must provide a valid metric"
        assert project_id and isinstance(
            project_id, str
        ), "You must provide a valid project ID"
        assert dataset_id and isinstance(
            dataset_id, str
        ), "You must provide a valid dataset ID"
        assert (name and isinstance(name, str)) or (
            name is None
        ), "You must provide a valid name"

        payload = {
            "name": name,
            "llm": llm,
            "dataset": dataset_id,
            "task_description": task_description,
            "experiment": None,
            "metric": metric.value,
            "prompt": prompt.asdict(),
        }
        endpoint = f"prompts/opt/{project_id}/"
        res = self._client._request(endpoint, HTTPMethod.POST, data=json.dumps(payload))
        if res.status_code != 200:
            raise APIError(message="Failed to submit optimization task", response=res)
        return res.json()

    def get_progress(self, prompt_id: str) -> dict:
        endpoint = f"prompts/{prompt_id}/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get optimization task", response=response)

        status = response.json()["status"]

        out = {
            "status": status,
            "eta": None,
            "progress": None,
            "total": None,
            "completed": None,
        }

        endpoint = f"prompts/opt/{prompt_id}/progress/"
        response = self._client._request(endpoint, HTTPMethod.GET)
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
