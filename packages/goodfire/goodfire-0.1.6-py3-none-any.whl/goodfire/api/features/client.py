from typing import List, Optional, Union

import requests

from ...features.features import Feature, FeatureGroup
from ..chat.interfaces import ChatMessage
from ..constants import PRODUCTION_BASE_URL
from ..exceptions import check_status_code
from .interfaces import ClusteringConfig, SearchFeatureResponse


class FeaturesAPI:
    def __init__(
        self,
        goodfire_api_key: str,
        base_url: str = PRODUCTION_BASE_URL,
    ):
        self.goodfire_api_key = goodfire_api_key
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.goodfire_api_key}",
            "Content-Type": "application/json",
        }

    def search(
        self,
        query: str,
        model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        top_k: int = 10,
    ):
        url = f"{self.base_url}/api/inference/v1/features/search"
        params = {
            "query": query,
            "page": 1,
            "perPage": top_k,
            "model": model,
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
        model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        top_k: int = 10,
    ):
        url = f"{self.base_url}/api/inference/v1/features/rerank"
        payload = {
            "query": query,
            "top_k": top_k,
            "model": model,
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

    def contrast(
        self,
        prompt: list[ChatMessage],
        steer_to: Union[str, list[str]],
        steer_away: Union[str, list[str]],
        model: str,
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
            "prompt": prompt,
            "steer_to_responses": steer_to,
            "steer_away_from_responses": steer_away,
            "k_to_add": top_k * 4,
            "k_to_remove": top_k * 4,
            "model": model,
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

    # def list(self, ids: list[str]):
    #     url = f"{self.base_url}/api/inference/v1/features"
    #     params = {
    #         "ids": ",".join(ids),
    #     }
    #     headers = self._get_headers()
    #     response = requests.get(url, params=params, headers=headers)

    #     check_status_code(response.status_code)

    #     response = SearchFeatureResponse.model_validate_json(response.text)

    #     return FeatureGroup(
    #         [
    #             Feature(
    #                 uuid=feature.id,
    #                 label=feature.label,
    #                 max_activation_strength=feature.max_activation_strength,
    #                 index_in_sae=feature.index_in_sae,
    #             )
    #             for feature in response.features
    #         ]
    #     )

    def _get_groups(
        self,
        feature_group: FeatureGroup,
        sae_id: str = "research-preview-alpha-chat-lmsys",
        config: ClusteringConfig = None,
    ) -> List[FeatureGroup]:
        """Returns a FeatureGroup of similar features for each feature in the input FeatureGroup"""
        url = f"{self.base_url}/api/inference/v1/features/{sae_id}/clusters"

        feature_ids = [
            str(feature.uuid) for feature in feature_group._features.values()
        ]
        body = {
            "feature_ids": feature_ids,
            "config": (config or ClusteringConfig()).model_dump(),
        }

        headers = self._get_headers()
        response = requests.post(url, headers=headers, json=body)

        check_status_code(response.status_code, response.text)

        feature_idx_to_features = response.json()["feature_idx_to_features"]
        return [
            FeatureGroup(
                [
                    Feature(
                        uuid=feature["uuid"],
                        label=feature["label"],
                        max_activation_strength=feature["max_activation_strength"],
                        index_in_sae=feature["index_in_sae"],
                    )
                    for feature in features
                ]
            )
            for features in feature_idx_to_features.values()
        ]
