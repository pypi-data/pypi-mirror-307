import typing
from relari.metrics import ToolCall

_SAFE_DICT = {k: v for k, v in typing.__dict__.items() if not k.startswith("__")}
_SAFE_DICT["UID"] = str
_SAFE_DICT["ToolCall"] = ToolCall

def str_to_type_hint(t: str) -> typing.Type:
    return eval(t, _SAFE_DICT)