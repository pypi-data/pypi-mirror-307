from typing import Optional

from pydantic import BaseModel

from ..valo_enums import (
    Episodes,
    MMRVersions,
    Regions,
)


class GetMMRByPUUIDFetchOptionsModel(BaseModel):
    version: MMRVersions
    region: Regions
    puuid: str
    filter: Optional[Episodes] = None


class GetMMRHistoryByPUUIDFetchOptionsModel(BaseModel):
    region: Regions
    puuid: str


class GetLifetimeMMRHistoryFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
    page: Optional[int] = None
    size: Optional[int] = None


class GetMMRFetchOptionsModel(BaseModel):
    version: MMRVersions
    region: Regions
    name: str
    tag: str
    filter: Optional[Episodes] = None


class GetMMRHistoryFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
