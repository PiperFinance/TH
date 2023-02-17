from enum import Enum
import pymongo
from pydantic import BaseModel
from typing import List, Optional, Any, Union

from . import Chain
from .token import Token
from configs.mongo_config import client
from utils.types import Address, StringBlockNumber, MongoClient


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


class Trx(Chain):
    userAddress: Address
    type: Optional[int]
    labels: Optional[List[Label]]
    tokens: Optional[List[Token]]
    blockNumber: StringBlockNumber
    timeStamp: int
    hash: str
    nonce: str
    blockHash: str
    fromAddress: Address
    contractAddress: Optional[str]
    to: Union[Address, str]
    value: str
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    input: Optional[str]
    confirmations: str
    isError: Optional[str]
    txreceipt_status: Optional[str]

    @classmethod
    def mongo_client(cls, chain_id: int) -> MongoClient:
        c = client(cls.__name__, chain_id)
        c.create_index("hash", unique=True)
        c.create_index([("timeStamp", pymongo.DESCENDING)], background=True)
        return c
