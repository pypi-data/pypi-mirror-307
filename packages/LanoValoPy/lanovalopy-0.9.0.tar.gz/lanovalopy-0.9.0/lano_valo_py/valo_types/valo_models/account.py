from typing import Optional

from pydantic import BaseModel

from ..valo_enums import AccountVersion


class AccountFetchOptionsModel(BaseModel):
    name: str
    tag: str
    version: AccountVersion = "v1"
    force: Optional[bool] = None


class AccountFetchByPUUIDOptionsModel(BaseModel):
    puuid: str
    force: Optional[bool] = None