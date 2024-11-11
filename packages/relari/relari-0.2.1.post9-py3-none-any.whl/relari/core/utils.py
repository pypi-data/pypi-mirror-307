from datetime import datetime
from typing import Any, Type, Union, Dict, List

from pydantic import ValidationError, create_model

SIZE = 32

Timestamp = float


def to_timestamp(datetime_obj) -> Timestamp:
    return datetime_obj.timestamp()


def from_timestamp(timestamp) -> datetime:
    return datetime.fromtimestamp(timestamp)


def now_timestamp() -> Timestamp:
    return to_timestamp(datetime.now())


def type_hint_to_str(type_hint: Type):
    if hasattr(type_hint, "__origin__"):  # Check if it's a generic type
        # Get the base type name (e.g., 'List' or 'Dict')
        base = type_hint.__origin__.__name__.title()
        # Recursively process the arguments (e.g., the contents of List, Dict, etc.)
        args = ", ".join(type_hint_to_str(arg) for arg in type_hint.__args__)
        return f"{base}[{args}]"
    elif hasattr(type_hint, "__name__"):
        return type_hint.__name__
    else:
        return type_hint if isinstance(type_hint, str) else repr(type_hint)


def check_type(var: Any, type_hint: Any) -> bool:
    """
    Checks if 'var' matches the 'type_hint'.

    Args:
    var (Any): The variable to check.
    type_hint (Any): The type hint (from the typing module) against which to check the variable.

    Returns:
    bool: True if 'var' matches the 'type_hint', False otherwise.
    """
    # Dynamically create a Pydantic model with one field 'data' of the provided type hint
    DynamicModel = create_model("DynamicModel", data=(type_hint, ...))
    DynamicModel.model_rebuild()  # Call model_rebuild to finalize the model

    try:
        # Create an instance of the model with 'var' as the data to validate the type
        DynamicModel(data=var)
        return True
    except ValidationError:
        return False


# def validate_metric_data(
#     metric, data: List[Dict[str, Any]], with_optional: bool = False
# ):
#     for d, t in metric.mandatory.items():
#         if d not in data:
#             raise ValueError(f"Missing field: {d}")
#         if not check_type(data[d], t):
#             raise ValueError(
#                 f"Invalid type for field {d}: expected {type_hint_to_str(t)} but found {type_hint_to_str(type(data[d]))}"
#             )
#     if with_optional:
#         for d in metric.optional:
#             if d not in data:
#                 raise ValueError(f"Missing field: {d}")
#             if not check_type(data[d], t):
#                 raise ValueError(
#                     f"Invalid type for field {d}: expected {type_hint_to_str(t)} but found {type_hint_to_str(type(data[d]))}"
#                 )
