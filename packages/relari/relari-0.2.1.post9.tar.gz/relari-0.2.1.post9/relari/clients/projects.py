import json
from relari.core.types import HTTPMethod
from relari.core.exceptions import APIError

class ProjectsClient:
    def __init__(self, client):
        self._client = client

    def list(self):
        response = self._client._request("projects", HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to list projects", response=response)
        return response.json()

    def create(self, name: str, do_not_create_if_exists: bool = False):
        if do_not_create_if_exists:
            projects = self.find(name)
            if projects is not None:
                return projects
        payload = {"name": name}
        response = self._client._request(
            "projects", HTTPMethod.POST, data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise APIError(message="Failed to create project", response=response)
        return response.json()
    
    def delete(self, id: str):
        response = self._client._request(
            f"projects/{id}", HTTPMethod.DELETE
        )
        if response.status_code != 204:
            raise APIError(message="Failed to delete project", response=response)

    def find(self, name: str):
        projects = self.list()
        name_ = name.strip()
        out = list()
        for project in projects:
            if project["name"].strip() == name_:
                out.append(project)
        if len(out) == 0:
            return None
        return out
    
    def find_one(self, name: str):
        projects = self.list()
        name_ = name.strip()
        for project in projects:
            if project["name"].strip() == name_:
                return project
        return None