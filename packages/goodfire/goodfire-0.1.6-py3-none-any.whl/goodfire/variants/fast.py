from typing import Literal, Union, overload

from typing_extensions import TypedDict

from ..controller.controller import Controller
from ..features.features import Feature, FeatureGroup
from .variants import VariantInterface


class FeatureDelta(TypedDict):
    mode: Literal["nudge", "pin"]
    value: Union[float, bool]


class Variant(VariantInterface):
    def __init__(self, base_model: str):
        self.base_model = base_model
        self.edits: dict[Feature, FeatureDelta] = {}

    @overload
    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, None],
        mode: Literal["nudge"] = "nudge",
    ) -> None:
        ...

    @overload
    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, bool, None],
        mode: Literal["pin"] = "pin",
    ) -> None:
        ...

    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, bool, None],
        mode: Literal["nudge", "pin"] = "pin",
    ):
        if value is None:
            self.clear(feature)
            return

        if isinstance(feature, Feature):
            self.edits[feature] = {
                "mode": mode,
                "value": value,
            }
        else:
            for f in feature:
                self.edits[f] = {"mode": mode, "value": value}

    def clear(self, feature: Union[Feature, FeatureGroup]):
        if isinstance(feature, Feature):
            self.edits.pop(feature, None)
        else:
            for f in feature:
                self.edits.pop(f, None)

    def reset(self):
        self.edits = {}

    def __repr__(self):
        return str(self)

    def __str__(self):
        edits = "{"
        for feature, edit in self.edits.items():
            edits += f"\n      {feature}: {edit},"
        edits += "\n   }"

        return f"Variant(\n   base_model={self.base_model},\n   edits={edits}\n)"

    def json(self):
        return {
            "base_model": self.base_model,
            "fastmodel_config": [
                {
                    "feature_id": str(feature.uuid),
                    "feature_label": feature.label,
                    "max_activation_strength": feature.max_activation_strength,
                    "index_in_sae": feature.index_in_sae,
                    "mode": edit["mode"],
                    "value": edit["value"],
                }
                for feature, edit in self.edits.items()
            ],
        }

    @property
    def controller(self) -> Controller:
        controller = Controller()

        for feature, edit in self.edits.items():
            value = edit["value"]
            if isinstance(value, bool):
                value = 0.5 if value else -0.3

            if edit["mode"] == "nudge":
                controller[feature] += edit["value"]
            else:
                controller[feature] = edit["value"]

        return controller
