from typing import Optional

from pydantic import BaseModel

from ..valo_enums import (
    Maps,
    Modes,
    Regions,
)


class GetMatchesByPUUIDFetchOptionsModel(BaseModel):
    region: Regions
    puuid: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetMatchesFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetMatchFetchOptionsModel(BaseModel):
    match_id: str