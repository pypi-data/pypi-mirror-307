from typing import Optional

from pydantic import BaseModel


class ContentTierModel(BaseModel):
    name: str
    dev_name: str
    icon: str


class StoreOffersResponseModelV2(BaseModel):
    offer_id: str
    cost: int
    name: str
    icon: Optional[str]
    type: str
    skin_id: str
    content_tier: Optional[ContentTierModel]