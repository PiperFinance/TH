from pydantic import BaseModel
from typing import List, Optional

from utils.types import Address, ChainId


class FunctionSelectorSchema(BaseModel):
    hex: str
    text: str
    args: Optional[List[List[str]]]
    secret: Optional[str]


class FunctionSelectorsSchema(BaseModel):
    functionSelectors: List[FunctionSelectorSchema]
    secret: Optional[str]


class UsersChainData(BaseModel):
    chainId: ChainId
    userAddresses: List[Address]
    secret: Optional[str]


class UsersData(BaseModel):
    chainIds: List[ChainId]
    userAddresses: List[Address]
    scanIterations: Optional[int]
    secret: Optional[str]


class TrxWithNoLabelsSchema(BaseModel):
    chainId: ChainId
    hash: str


class TrxsWithNoLabelsSchema(BaseModel):
    trxs: List[TrxWithNoLabelsSchema]
