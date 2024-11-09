from typing import Any, Literal, Optional, overload

import requests
from pydantic import BaseModel

from ...api.constants import PRODUCTION_BASE_URL
from ...api.exceptions import check_status_code
from ...controller.controller import Controller
from ...features.features import Feature
from ...variants.fast import Variant
from ...variants.variants import ProgrammableVariant, VariantInterface


class VariantMetaData(BaseModel):
    name: str
    base_model: str
    id: str


class VariantsAPI:
    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.base_url = base_url
        self.api_key = api_key

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @overload
    def get(self, variant_id: str, fast_variant: Literal[True] = True) -> Variant:
        ...

    @overload
    def get(
        self, variant_id: str, fast_variant: Literal[False] = False
    ) -> ProgrammableVariant:
        ...

    def get(self, variant_id: str, fast_variant: bool = True):
        url = f"{self.base_url}/api/inference/v1/model-variants/{variant_id}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)

        check_status_code(response.status_code, response.text)

        response_json = response.json()

        if response_json.get("fastmodel_config") or fast_variant:
            model = Variant(
                response_json["base_model"],
            )

            if config := response_json.get("fastmodel_config"):
                for edit in config:
                    model.set(
                        Feature(
                            uuid=edit["feature_id"],
                            label=edit["feature_label"],
                            max_activation_strength=edit["max_activation_strength"],
                            index_in_sae=edit["index_in_sae"],
                        ),
                        edit["value"],
                        edit["mode"],
                    )
        else:
            controller = Controller.from_json(
                response_json["controller"],
                response_json.get("name", "controller"),
                response_json["id"],
            )

            model = ProgrammableVariant(
                base_model=response_json["base_model"],
                controller=controller,
            )

        return model

    def list(self):
        url = f"{self.base_url}/api/inference/v1/model-variants"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)

        check_status_code(response.status_code, response.text)

        response_json = response.json()

        return [
            VariantMetaData(
                name=variant["name"],
                base_model=variant["base_model"],
                id=variant["id"],
            )
            for variant in response_json["model_variants"]
        ]

    def create(self, variant: VariantInterface, name: str):
        payload: dict[str, Any] = {
            "tokens": [],
            "base_model": variant.base_model,
            "name": name,
        }

        if isinstance(variant, Variant):
            payload["fastmodel_config"] = variant.json()["fastmodel_config"]
        else:
            payload["controller"] = variant.controller.json()

        url = f"{self.base_url}/api/inference/v1/model-variants"
        headers = self._get_headers()
        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )

        check_status_code(response.status_code, response.text)

        response_json = response.json()

        return response_json["id"]

    def update(
        self, id: str, variant: VariantInterface, new_name: Optional[str] = None
    ):
        payload: dict[str, Any] = {
            "tokens": [],
            "base_model": variant.base_model,
        }

        if isinstance(variant, Variant):
            payload["fastmodel_config"] = variant.json()["fastmodel_config"]
        else:
            payload["controller"] = variant.controller.json()

        if new_name:
            payload["name"] = new_name

        url = f"{self.base_url}/api/inference/v1/model-variants/{id}"
        headers = self._get_headers()
        response = requests.put(
            url,
            headers=headers,
            json=payload,
        )

        check_status_code(response.status_code, response.text)

    def delete(self, id: str):
        url = f"{self.base_url}/api/inference/v1/model-variants/{id}"
        headers = self._get_headers()
        response = requests.delete(url, headers=headers)

        check_status_code(response.status_code, response.text)
