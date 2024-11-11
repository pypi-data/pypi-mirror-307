from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, TypedDict, Union, Tuple
from math import isclose
UID = str


def args_to_dict(*args, **kwargs):
    arg_dict = dict(kwargs)
    for index, value in enumerate(args):
        arg_dict[f"_arg{index}"] = value
    return arg_dict


class ToolCall(TypedDict):
    name: str
    kwargs: Dict[str, Any]


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


@dataclass(frozen=True, eq=True)
class DatasetDatum:
    label: str
    data: dict

    def asdict(self):
        return {
            "label": self.label,
            "data": self.data,
        }


MetricsArgs = Union[DatasetDatum, Dict[str, Any]]

######################################################################################


@dataclass
class UserPrompt:
    prompt: str
    description: str

    def asdict(self):
        return {"prompt": self.prompt, "description": self.description}


@dataclass
class Prompt:
    system: str
    user: UserPrompt

    def is_valid(self):
        assert isinstance(self.user, UserPrompt), "user must be an instance of UserPrompt"
        assert self.system, "fixed must not be empty"
        assert self.user.prompt, "user.prompt must not be empty"
        assert self.user.description, "user.description must not be empty"
        return True


    def asdict(self):
        return {"system": self.system, "user": self.user.asdict()}
