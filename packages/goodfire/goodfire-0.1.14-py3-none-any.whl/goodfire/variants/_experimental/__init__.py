import logging

from ...controller.controller import Controller
from ..variants import VariantInterface

logger = logging.getLogger(__name__)


has_warned = False


class ProgrammableVariant(VariantInterface):
    def __init__(self, base_model: str):
        global has_warned

        if not has_warned:
            logger.warning(
                "ProgrammableVariants are an experimental feature and may change in the future."
            )
            has_warned = True

        self.base_model = base_model
        self._controller = Controller()

    @property
    def controller(self) -> Controller:
        return self._controller

    def reset(self):
        self._controller = Controller()
