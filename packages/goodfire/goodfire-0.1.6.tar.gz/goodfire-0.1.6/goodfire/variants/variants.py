from typing import Protocol

from ..controller.controller import Controller


class VariantInterface(Protocol):
    base_model: str

    @property
    def controller(self) -> Controller:
        ...


class ProgrammableVariant(VariantInterface):
    def __init__(self, base_model: str, controller: Controller):
        self.base_model = base_model
        self._controller = controller

    @property
    def controller(self) -> Controller:
        return self._controller
