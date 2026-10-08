from app.models.module import ModuleType
from app.modules.base import BaseModule
from app.modules.practical import PracticalModule
from app.modules.quiz import QuizModule
from app.modules.theoretical import TheoreticalModule

REGISTRY: dict[ModuleType, BaseModule] = {
    ModuleType.THEORETICAL: TheoreticalModule(),
    ModuleType.QUIZ: QuizModule(),
    ModuleType.PRACTICAL: PracticalModule(),
}


def get_handler(module_type: ModuleType) -> BaseModule:
    return REGISTRY[module_type]
