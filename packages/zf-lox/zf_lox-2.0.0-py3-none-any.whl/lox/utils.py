from pydantic import BaseModel, create_model
from typing import Any


def build_pydantic_model(fields: list[str]) -> type[BaseModel]:
    fields_dict: dict[str, Any] = {}
    for field in fields:
        fields_dict[field] = (str, ...)

    return create_model("PydanticModel", **fields_dict)

