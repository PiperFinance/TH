from pydantic import BaseModel
from typing import List, Optional

from utils.types import Address, ChainId


class FunctionSelectorSchema(BaseModel):
    hex: str
    text: str
    args: List[List[str]]


class UsersData(BaseModel):
    chainId: ChainId
    userAddresses: List[Address]
