from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FeatureResponse(BaseModel):
    id: UUID
    label: str
    max_activation_strength: float
    index_in_sae: int


class SearchFeatureResponseItem(FeatureResponse):
    relevance: float


class SearchFeatureResponse(BaseModel):
    features: list[SearchFeatureResponseItem]


class FeatureDetailsResponse(BaseModel):
    features: list[FeatureResponse]


class ClusteringConfig(BaseModel):
    min_cluster_size: int = Field(default=5, ge=2)
    max_cluster_size: Optional[int] = Field(default=None)
    min_samples: Optional[int] = Field(default=None, ge=1)
    cluster_selection_method: str = Field(default="leaf", pattern="^(eom|leaf)$")
    cluster_selection_epsilon: float = Field(default=0.0, ge=0.0)
