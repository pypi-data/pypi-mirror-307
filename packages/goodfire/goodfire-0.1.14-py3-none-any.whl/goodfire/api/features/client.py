from typing import Any, Iterable, Optional, Union

import requests

from ...features.features import Feature, FeatureGroup
from ...variants.variants import VariantInterface
from ..chat.interfaces import ChatMessage
from ..constants import PRODUCTION_BASE_URL
from ..exceptions import check_status_code
from .interfaces import SearchFeatureResponse


class _ExperimentalFeaturesAPI:
    def __init__(
        self,
        features_api: "FeaturesAPI",
    ):
        self.features_api = features_api

        self._warned_user = False

    def _warn_user(self):
        if not self._warned_user:
            print("Warning: The experimental features API is subject to change.")
            self._warned_user = True

    def neighbors(
        self,
        features: Union[Feature, FeatureGroup],
        model: Union[str, VariantInterface] = "meta-llama/Meta-Llama-3-8B-Instruct",
        top_k: int = 10,
    ):
        self._warn_user()
        if isinstance(features, Feature):
            features = FeatureGroup([features])

        url = f"{self.features_api.base_url}/api/inference/v1/attributions/neighbors"
        payload = {
            "feature_indices": [feature.index_in_sae for feature in features],
            "model": model if isinstance(model, str) else model.base_model,
            "top_k": top_k,
        }
        headers = self.features_api._get_headers()
        response = requests.post(url, json=payload, headers=headers)

        check_status_code(response.status_code, response.text)

        response_body = response.json()

        results: list[Feature] = []
        for feature in response_body["neighbors"]:
            results.append(
                Feature(
                    uuid=feature["id"],
                    label=feature["label"],
                    max_activation_strength=feature["max_activation_strength"],
                    index_in_sae=feature["index_in_sae"],
                )
            )

        return FeatureGroup(results)


class FeaturesAPI:
    def __init__(
        self,
        goodfire_api_key: str,
        base_url: str = PRODUCTION_BASE_URL,
    ):
        self.goodfire_api_key = goodfire_api_key
        self.base_url = base_url

        self._experimental = _ExperimentalFeaturesAPI(self)

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.goodfire_api_key}",
            "Content-Type": "application/json",
        }

    def search(
        self,
        query: str,
        model: Union[str, VariantInterface] = "meta-llama/Meta-Llama-3-8B-Instruct",
        top_k: int = 10,
    ):
        url = f"{self.base_url}/api/inference/v1/features/search"
        params = {
            "query": query,
            "page": 1,
            "perPage": top_k,
            "model": model if isinstance(model, str) else model.base_model,
        }
        headers = self._get_headers()
        response = requests.get(url, params=params, headers=headers)

        check_status_code(response.status_code, response.text)

        response = SearchFeatureResponse.model_validate_json(response.text)

        features: list[Feature] = []
        relevance_scores: list[float] = []
        for feature in response.features:
            features.append(
                Feature(
                    uuid=feature.id,
                    label=feature.label,
                    max_activation_strength=feature.max_activation_strength,
                    index_in_sae=feature.index_in_sae,
                )
            )
            relevance_scores.append(feature.relevance)

        return FeatureGroup(features), relevance_scores

    def rerank(
        self,
        features: FeatureGroup,
        query: str,
        model: Union[str, VariantInterface] = "meta-llama/Meta-Llama-3-8B-Instruct",
        top_k: int = 10,
    ):
        url = f"{self.base_url}/api/inference/v1/features/rerank"
        payload = {
            "query": query,
            "top_k": top_k,
            "model": model if isinstance(model, str) else model.base_model,
            "feature_ids": [str(feature.uuid) for feature in features],
        }
        headers = self._get_headers()
        response = requests.post(url, json=payload, headers=headers)

        check_status_code(response.status_code, response.text)

        response = SearchFeatureResponse.model_validate_json(response.text)

        features_to_return: list[Feature] = []
        for feature in response.features:
            features_to_return.append(
                Feature(
                    uuid=feature.id,
                    label=feature.label,
                    max_activation_strength=feature.max_activation_strength,
                    index_in_sae=feature.index_in_sae,
                )
            )

        return FeatureGroup(features_to_return)

    def inspect(
        self,
        messages: list[ChatMessage],
        model: Union[str, VariantInterface] = "meta-llama/Meta-Llama-3-8B-Instruct",
        features: Optional[Union[Feature, FeatureGroup]] = None,
    ):
        payload: dict[str, Any] = {
            "messages": messages,
        }

        if isinstance(model, str):
            payload["model"] = model
        else:
            payload["model"] = model.base_model
            payload["controller"] = model.controller.json()

        include_feature_ids: Optional[set[str]] = None
        if features:
            if isinstance(features, Feature):
                include_feature_indexes = [features.index_in_sae]
                include_feature_ids = {str(features.uuid)}
            else:
                include_feature_indexes: list[int] = []
                include_feature_ids = set()
                for f in features:
                    include_feature_ids.add(str(f.uuid))
                    include_feature_indexes.append(f.index_in_sae)

            payload["include_feature_indexes"] = include_feature_indexes

        response = requests.post(
            f"{self.base_url}/api/inference/v1/attributions/compute-features",
            headers=self._get_headers(),
            json=payload,
        )
        check_status_code(response.status_code, response.text)

        return ContextInspector(
            self, response.json(), include_feature_ids=include_feature_ids
        )

    def get(self, ids: list[str]):
        url = f"{self.base_url}/api/inference/v1/features"
        params = {
            "feature_id": ids,
        }
        headers = self._get_headers()
        response = requests.get(url, params=params, headers=headers)

        check_status_code(response.status_code, response.text)

        response = SearchFeatureResponse.model_validate_json(response.text)

        return FeatureGroup(
            [
                Feature(
                    uuid=feature.id,
                    label=feature.label,
                    max_activation_strength=feature.max_activation_strength,
                    index_in_sae=feature.index_in_sae,
                )
                for feature in response.features
            ]
        )

    def contrast(
        self,
        messages: list[ChatMessage],
        steer_to: Union[str, list[str]],
        steer_away: Union[str, list[str]],
        model: Union[str, VariantInterface] = "meta-llama/Meta-Llama-3-8B-Instruct",
        steer_to_rerank_query: Optional[str] = None,
        steer_away_rerank_query: Optional[str] = None,
        top_k: int = 5,
    ):
        if isinstance(steer_to, str):
            steer_to = [steer_to]

        if isinstance(steer_away, str):
            steer_away = [steer_away]

        if len(steer_to) != len(steer_away):
            raise ValueError("steer_to and steer_away must have the same length")

        if len(steer_to) == 0:
            raise ValueError("steer_to and steer_away must have at least one element")

        url = f"{self.base_url}/api/inference/v1/attributions/contrast"
        payload = {
            "prompt": messages,
            "steer_to_responses": steer_to,
            "steer_away_from_responses": steer_away,
            "k_to_add": top_k * 4,
            "k_to_remove": top_k * 4,
            "model": model if isinstance(model, str) else model.base_model,
        }

        headers = self._get_headers()
        response = requests.post(url, json=payload, headers=headers)

        check_status_code(response.status_code, response.text)

        response_body = response.json()

        to_add = FeatureGroup(
            [
                Feature(
                    uuid=feature["id"],
                    label=feature["label"],
                    max_activation_strength=feature["max_activation_strength"],
                    index_in_sae=feature["index_in_sae"],
                )
                for feature in response_body["steer_to"]
            ]
        )
        to_remove = FeatureGroup(
            [
                Feature(
                    uuid=feature["id"],
                    label=feature["label"],
                    max_activation_strength=feature["max_activation_strength"],
                    index_in_sae=feature["index_in_sae"],
                )
                for feature in response_body["steer_away"]
            ]
        )

        to_add = self.rerank(
            to_add, steer_to_rerank_query or steer_to[0], model, top_k=top_k
        )
        to_remove = self.rerank(
            to_remove, steer_away_rerank_query or steer_away[0], model, top_k=top_k
        )

        return to_add, to_remove


class FeatureActivation:
    def __init__(self, feature: Feature, activation_strength: float):
        self.feature = feature
        self.activation = activation_strength

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            f"FeatureActivation(feature={self.feature}, activation={self.activation})"
        )


class FeatureActivations:
    def __init__(self, acts: Iterable[tuple[Feature, float]]):
        self._acts = [FeatureActivation(feat, act) for feat, act in acts]

    def __getitem__(self, idx: int):
        return self._acts[idx]

    def __iter__(self):
        return iter(self._acts)

    def __len__(self):
        return len(self._acts)

    def __repr__(self):
        return str(self)

    def __str__(self):
        response_str = "FeatureActivations("

        for index, act in enumerate(self._acts[:10]):
            response_str += f"\n{index}: ({act.feature}, {act.activation})"

        if len(self._acts) > 10:
            response_str += "\n..."

        response_str = response_str.replace("\n", "\n   ")

        response_str += "\n)"

        return response_str


class Token:
    def __init__(
        self, client: FeaturesAPI, token: str, feature_acts: list[dict[str, Any]]
    ):
        self._client = client
        self._token = token
        self._feature_acts = feature_acts

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Token("{self._token}")'

    def inspect(self, k: int = 5):
        uuids = [act["id"] for act in self._feature_acts[:k]]
        features = self._client.get(uuids)

        return FeatureActivations(
            tuple(
                (feature, act["activation_strength"])
                for feature, act in zip(features, self._feature_acts)
            )
        )


class ContextInspector:
    def __init__(
        self,
        client: FeaturesAPI,
        context_response: dict[str, Any],
        include_feature_ids: Optional[set[str]] = None,
    ):
        self._client = client
        self.tokens: list[Token] = []
        self._feature_strengths: dict[str, list[float]] = {}

        if include_feature_ids:
            for id in include_feature_ids:
                self._feature_strengths[id] = [0, 0]

        for token_config in context_response["tokens"]:
            self.tokens.append(
                Token(client, token_config["token"], token_config["attributions"])
            )
            for act in token_config["attributions"]:
                if abs(act["activation_strength"]) > 0.5:
                    if not self._feature_strengths.get(act["id"]):
                        self._feature_strengths[act["id"]] = [0, 0]
                    self._feature_strengths[act["id"]][0] += 1
                    self._feature_strengths[act["id"]][1] += act["activation_strength"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        response_str = "ContextInspector(\n"

        for token in self.tokens[:50]:
            response_str += f"{token._token}"

        response_str = response_str.replace("\n", "\n   ")

        if len(self.tokens) >= 50:
            response_str += "..."

        response_str += "\n)"

        return response_str

    def top(self, k: int = 5):
        sorted_feature_ids = sorted(
            list(self._feature_strengths.items()), key=lambda row: row[1], reverse=True
        )

        features = self._client.get([feat[0] for feat in sorted_feature_ids[:k]])

        return FeatureActivations(
            sorted(
                tuple(
                    (feature, self._feature_strengths[str(feature.uuid)][1])
                    for feature in features
                ),
                key=lambda row: row[1],
                reverse=True,
            )
        )
