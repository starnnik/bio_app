from typing import Any

from app.models import Module, ModuleType
from app.modules import get_handler
from app.modules.base import Evaluation


def validate_content(module_type: ModuleType, content: dict[str, Any]) -> dict[str, Any]:
    return get_handler(module_type).validate_content(content)


def public_content(module: Module) -> dict[str, Any]:
    return get_handler(module.type).public_content(module.content)


def execute(module: Module, payload: dict[str, Any]) -> Evaluation:
    handler = get_handler(module.type)
    return handler.evaluate(module.content, handler.parse_submission(payload))
