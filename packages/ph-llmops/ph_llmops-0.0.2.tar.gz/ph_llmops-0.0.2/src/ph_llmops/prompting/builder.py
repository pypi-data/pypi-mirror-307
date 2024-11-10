from typing import Any
from pydantic import BaseModel


def get_schema_from_model(model: type[BaseModel]) -> dict[str, Any]:
    return {k: str(v) for (k, v) in model.model_fields.items()}


def build_prompt(template: str, values: dict[str, Any]) -> str:
    return template.format(**values)
