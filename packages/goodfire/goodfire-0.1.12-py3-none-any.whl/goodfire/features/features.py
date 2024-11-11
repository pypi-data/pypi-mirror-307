from collections import OrderedDict
from typing import Any, Optional, Union, overload
from uuid import UUID

from .interfaces import CONDITIONAL_OPERATOR, JOIN_OPERATOR


class FeatureNotInGroupError(Exception):
    pass


class Feature:
    def __init__(
        self, uuid: UUID, label: str, max_activation_strength: float, index_in_sae: int
    ):
        self.uuid = uuid
        self.label = label
        self.max_activation_strength = max_activation_strength
        self.index_in_sae = index_in_sae

    def json(self):
        return {
            # Change to hex while passing through http.
            "uuid": self.uuid.hex if isinstance(self.uuid, UUID) else self.uuid,
            "label": self.label,
            "max_activation_strength": self.max_activation_strength,
            "index_in_sae": self.index_in_sae,
        }

    @staticmethod
    def from_json(data: dict[str, Any]):
        # If str is provided, update it to UUID.
        if isinstance(data["uuid"], str):
            data["uuid"] = UUID(data["uuid"])
        return Feature(
            uuid=data["uuid"],
            label=data["label"],
            max_activation_strength=data["max_activation_strength"],
            index_in_sae=data["index_in_sae"],
        )

    def __or__(self, other: "Feature"):
        group = FeatureGroup()
        group.add(self)
        group.add(other)

        return group

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.uuid)

    def __str__(self):
        return f'Feature("{self.label}")'

    def __eq__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) == other

    def __ne__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) != other

    def __le__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) <= other

    def __lt__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) < other

    def __ge__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) >= other

    def __gt__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        return FeatureGroup([self]) > other


class FeatureGroup:
    def __init__(self, features: Optional[list["Feature"]] = None):
        self._features: OrderedDict[int, "Feature"] = OrderedDict()

        if features:
            for feature in features:
                self.add(feature)

    def __iter__(self):
        for feature in self._features.values():
            yield feature

    @overload
    def __getitem__(self, index: int) -> "Feature":
        ...

    @overload
    def __getitem__(self, index: list[int]) -> "FeatureGroup":
        ...

    @overload
    def __getitem__(self, index: slice) -> "FeatureGroup":
        ...

    @overload
    def __getitem__(self, index: tuple[int, ...]) -> "FeatureGroup":
        ...

    def __getitem__(self, index: Union[int, list[int], tuple[int, ...], slice]):
        if isinstance(index, int):
            if index not in self._features:
                raise FeatureNotInGroupError(f"Feature with ID {index} not in group.")
            return self._features[index]
        elif isinstance(index, list) or isinstance(index, tuple):
            if isinstance(index, tuple):
                index = list(index)
            features: list[Feature] = []
            failed_indexes: list[int] = []
            while len(index) > 0:
                latest_index = index.pop(0)
                try:
                    features.append(self._features[latest_index])
                except KeyError:
                    failed_indexes.append(latest_index)

            if len(failed_indexes) > 0:
                raise FeatureNotInGroupError(
                    f"Features with IDs {failed_indexes} not in group."
                )

            return FeatureGroup(features)
        else:
            start = index.start if index.start else 0
            stop = index.stop if index.stop else len(self._features)
            step = index.step if index.step else 1

            if start < 0:
                start = len(self._features) + start

            if stop < 0:
                stop = len(self._features) + stop

            if step < 0:
                start, stop = stop, start

            if stop > len(self._features):
                stop = len(self._features)

            if start > len(self._features):
                start = len(self._features)

            if step == 0:
                raise ValueError("Step cannot be zero.")

            return FeatureGroup([self._features[i] for i in range(start, stop, step)])

    def __repr__(self):
        return str(self)

    def pick(self, feature_indexes: list[int]):
        new_group = FeatureGroup()
        for index in feature_indexes:
            new_group.add(self._features[index])

        return new_group

    def json(self) -> dict[str, Any]:
        return {"features": [f.json() for f in self._features.values()]}

    @staticmethod
    def from_json(data: dict[str, Any]):
        return FeatureGroup([Feature.from_json(f) for f in data["features"]])

    def add(self, feature: "Feature"):
        self._features[len(self._features)] = feature

    def pop(self, index: int):
        feature = self._features[index]
        del self._features[index]

        return feature

    def union(self, feature_group: "FeatureGroup"):
        new_group = FeatureGroup()

        new_features: OrderedDict[int, Feature] = OrderedDict()

        for index, feature in self._features.items():
            new_features[index] = feature

        for index, feature in feature_group._features.items():
            new_features[index] = feature

        new_group._features = new_features

        return new_group

    def intersection(self, feature_group: "FeatureGroup"):
        new_group = FeatureGroup()
        new_features: OrderedDict[int, Feature] = OrderedDict()

        for index, feature in self._features.items():
            if index in feature_group._features:
                new_features[index] = feature

        new_group._features = new_features

        return new_group

    def __or__(self, other: "FeatureGroup"):
        return self.union(other)

    def __and__(self, other: "FeatureGroup"):
        return self.intersection(other)

    def __len__(self):
        return len(self._features)

    def __str__(self):
        features = list(self._features.items())
        if len(features) <= 10:
            features_str = ",\n   ".join(
                [f'{index}: "{f.label}"' for index, f in features[:10]]
            )
        else:
            features_str = ",\n   ".join(
                [f'{index}: "{f.label}"' for index, f in features[:9]]
            )
            features_str += ",\n   ...\n   "
            features_str += ",\n   ".join(
                [f'{index}: "{f.label}"' for index, f in features[-1:]]
            )

        return f"FeatureGroup([\n   {features_str}\n])"

    def __eq__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self == FeatureGroup([other])
        else:
            return Conditional(self, other, "==")

    def __ne__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self != FeatureGroup([other])
        else:
            return Conditional(self, other, "!=")

    def __le__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self <= FeatureGroup([other])
        else:
            return Conditional(self, other, "<=")

    def __lt__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self < FeatureGroup([other])
        else:
            return Conditional(self, other, "<")

    def __ge__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self >= FeatureGroup([other])
        else:
            return Conditional(self, other, ">=")

    def __gt__(
        self,
        other: Union[
            "FeatureGroup",
            "Feature",
            "FeatureStatistic",
            float,
        ],
    ) -> "Conditional":
        if isinstance(other, Feature):
            return self > FeatureGroup([other])
        else:
            return Conditional(self, other, ">")


class FeatureStatistic:
    def __init__(self, initial_values: dict[UUID, float]):
        self._values = initial_values

    def json(self):
        return {"values": self._values}

    @staticmethod
    def from_json(data: dict[str, Any]):
        return FeatureStatistic(data["values"])

    def copy(self):
        return FeatureStatistic({**self._values})

    def _check_keys(self, other: "FeatureStatistic"):
        if len(set(list(self._values.keys()) + list(other._values.keys()))) != len(
            self._values.keys()
        ):
            raise ValueError()

    def __add__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)

            for key, val in other._values.items():
                self._values[key] += val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] += other
        else:
            raise ValueError()

        return self

    def __sub__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)

            for key, val in other._values.items():
                self._values[key] -= val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] -= other
        else:
            raise ValueError()

        return self

    def __neg__(self):
        copy = self.copy()
        copy.__mul__(-1)

        return copy

    def __mul__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)
            for key, val in other._values.items():
                self._values[key] *= val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] *= other
        else:
            raise ValueError()

        return self

    def __pow__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)

            for key, val in other._values.items():
                self._values[key] **= val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] **= other
        else:
            raise ValueError()

        return self

    def __floordiv__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)

            for key, val in other._values.items():
                self._values[key] //= val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] //= other
        else:
            raise ValueError()

        return self

    def __truediv__(self, other: Union["FeatureStatistic", float]):
        if isinstance(other, FeatureStatistic):
            self._check_keys(other)

            for key, val in other._values.items():
                self._values[key] /= val
        elif isinstance(other, float):
            for key, val in self._values.items():
                self._values[key] /= other
        else:
            raise ValueError()

        return self

    def __iter__(self):
        for value in self._values.values():
            yield value

    def __len__(self):
        return len(self._values.keys())


class ConditionalGroup:
    def __init__(
        self, conditionals: list["Conditional"], operator: JOIN_OPERATOR = "AND"
    ):
        self.conditionals = conditionals
        self.operator = operator

    def json(self) -> dict[str, Any]:
        return {
            "conditionals": [c.json() for c in self.conditionals],
            "operator": self.operator,
        }

    @staticmethod
    def from_json(data: dict[str, Any]):
        return ConditionalGroup(
            [Conditional.from_json(c) for c in data["conditionals"]],
            operator=data["operator"],
        )

    def __and__(
        self, other: Union["ConditionalGroup", "Conditional"]
    ) -> "ConditionalGroup":
        if isinstance(other, Conditional):
            other_group = ConditionalGroup([other])
        else:
            other_group: ConditionalGroup = other

        return ConditionalGroup(
            self.conditionals + other_group.conditionals, operator="AND"
        )

    def __or__(
        self, other: Union["ConditionalGroup", "Conditional"]
    ) -> "ConditionalGroup":
        if isinstance(other, Conditional):
            other_group = ConditionalGroup([other])
        else:
            other_group: ConditionalGroup = other

        return ConditionalGroup(
            self.conditionals + other_group.conditionals, operator="OR"
        )


class Conditional:
    def __init__(
        self,
        left_hand: FeatureGroup,
        right_hand: Union[Feature, FeatureGroup, FeatureStatistic, float],
        operator: CONDITIONAL_OPERATOR,
    ):
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.operator = operator

    def json(self) -> dict[str, Any]:
        return {
            "left_hand": self.left_hand.json(),
            "right_hand": (
                self.right_hand.json()
                if getattr(self.right_hand, "json", None)
                else self.right_hand
            ),
            "operator": self.operator,
        }

    @staticmethod
    def from_json(data: dict[str, Any]):
        return Conditional(
            FeatureGroup.from_json(data["left_hand"]),
            (
                FeatureStatistic.from_json(data["right_hand"])
                if isinstance(data["right_hand"], dict)
                else data["right_hand"]
            ),
            data["operator"],
        )

    def __and__(self, other: "Conditional") -> ConditionalGroup:
        return ConditionalGroup([self, other], operator="AND")

    def __or__(self, other: "Conditional") -> ConditionalGroup:
        return ConditionalGroup([self, other], operator="OR")
