import json
import mimetypes
from enum import Enum
from pathlib import Path
from typing import List, Optional

from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod


class SyntheticDataClient:
    class DatasetType(str, Enum):
        RAG = "rag"  # Generates questions and answer pairs from your documents
        CONVERSATIONAL_AGENTS = "conversational_agents"  # Produces multi-turn dialogues for testing conversational AI
        CODE_GENERATION = "code_generation"  # Creates code snippets based on given prompts or requirements
        SUMMARIZATION = (
            "summarization"  # Generates concise summaries from longer documents
        )
        DATA_EXTRACTION = (
            "data_extraction"  # Extracts specific information from unstructured text
        )
        CLASSIFICATION = (
            "classification"  # Generates labeled data for various classification task
        )

    def __init__(self, client) -> None:
        self._client = client

    @staticmethod
    def guess_mime_type(filename):
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = "application/octet-stream"
        return mime_type

    def new(
        self,
        project_id: str,
        samples: int,
        files: List[Path],
        name: Optional[str] = None,
        dataset_type: DatasetType = DatasetType.RAG,
    ):
        if dataset_type != self.DatasetType.RAG:
            feature = " ".join(
                word.capitalize() for word in dataset_type.value.split("_")
            )
            raise NotImplementedError(f"{feature} is coming soon. Stay tuned!")
        endpoint = f"projects/{project_id}/synth/rag/"
        payload = [
            ("files", (file.name, open(file, "rb"), "application/octet-stream"))
            for file in files
        ]
        res = self._client._request(
            endpoint,
            HTTPMethod.POST,
            params={"name": name, "samples": samples},
            files=payload,
        )
        # Ensuring files are closed after the request
        for _, file_info in payload:
            _, file_handle, _ = file_info
            file_handle.close()
        # Check response status and raise error if needed
        if res.status_code != 200:
            raise APIError(message="Failed to create synthetic data", response=res)
        return res.json()

    def get_progress(self, datasetid: str) -> dict:
        endpoint = f"projects/datasets/{datasetid}/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get synth task", response=response)

        status = response.json()["status"]

        out = {
            "status": status,
            "eta": None,
            "progress": None,
            "total": None,
            "completed": None,
        }

        endpoint = f"projects/datasets/{datasetid}/progress/"
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
