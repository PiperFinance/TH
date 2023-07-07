from pydantic import BaseModel
from typing import List, Optional

from utils.types import Address, ChainId


class FunctionSelectorSchema(BaseModel):
    hex: str
    text: str
    args: Optional[List[List[str]]]


class FunctionSelectorsSchema(BaseModel):
    functionSelectors: List[FunctionSelectorSchema]


class UsersChainData(BaseModel):
    chainId: ChainId
    userAddresses: List[Address]


class UsersData(BaseModel):
    chainIds: List[ChainId]
    userAddresses: List[Address]
    scanIterations: Optional[int]


class TrxWithNoLabelsSchema(BaseModel):
    chainId: ChainId
    hash: str


class TrxsWithNoLabelsSchema(BaseModel):
    trxs: List[TrxWithNoLabelsSchema]
