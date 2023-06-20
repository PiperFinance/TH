from enum import Enum
import pymongo
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import List, Optional, Any, Union

from .chain import Chain
from .token import Token
from .address import Address
from configs.mongo_config import client


class TrxType(Enum):
    NORMAL_TRX = "normal"
    TOKEN_TRX = "token"

    @property
    def url(self):
        if self.value == "normal":
            return "?module=account&action=txlist"
        if self.value == "token":
            return "?module=account&action=tokentx"


class Label(BaseModel):
    title: str
    value: Any
    # value: Union[str, int, bytes, bytearray, List]

    class Config:
        arbitrary_types_allowed = True


class Trx(SQLModel, table=True):
    hash: str = Field(primary_key=True)
    chainId: int = Field(foreign_key=Chain.id)
    userAddress: str = Field(foreign_key=Address.address)
    fromAddress: str
    toAddress: Optional[str]
    labels: Optional[str]
    tokens: Optional[str]
    type: Optional[int]
    contractAddress: Optional[str]
    input: Optional[str]
    isError: Optional[str]
    txreceipt_status: Optional[str]
    blockNumber: str
    timeStamp: int = Field(index=True)
    nonce: str
    blockHash: str
    value: str
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    confirmations: str
