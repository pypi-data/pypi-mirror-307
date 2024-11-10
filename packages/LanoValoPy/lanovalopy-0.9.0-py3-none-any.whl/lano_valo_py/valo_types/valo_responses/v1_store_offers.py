from typing import Dict, List, Optional

from pydantic import BaseModel


class RewardModel(BaseModel):
    ItemTypeID: str
    ItemID: str
    Quantity: int


class OfferModel(BaseModel):
    OfferID: str
    IsDirectPurchase: bool
    StartDate: str
    Cost: Dict[str, int]
    Rewards: List[RewardModel]


class OfferUpgradeCurrencyModel(BaseModel):
    OfferID: str
    StorefrontItemID: str
    Offer: OfferModel
    DiscountedPercent: float


class StoreOffersResponseModelV1(BaseModel):
    Offers: List[OfferModel]
    UpgradeCurrencyOffers: Optional[List[OfferUpgradeCurrencyModel]]
