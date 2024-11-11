from typing import Protocol

from ..controller.controller import Controller


class VariantInterface(Protocol):
    base_model: str

    @property
    def controller(self) -> Controller:
        ...
