from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Union, Any

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
            return "?module=account&action=txlist&apikey="
        if self.value == "token":
            return "?module=account&action=tokentx&apikey="


class Label(BaseModel):
    title: str
    value: Any
    # value: Union[str, int, bytes, bytearray, List]

    class Config:
        arbitrary_types_allowed = True


class Trx(Chain):
    userAddress: Address
    labels: Optional[List[Label]]
    token: Optional[Union[Token, List[Token]]]
    blockNumber: StringBlockNumber
    timeStamp: int
    hash: str
    nonce: str
    blockHash: str
    fromAddress: Address
    contractAddress: Optional[str]
    to: Address
    value: str
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    input: str
    confirmations: str
    isError: Optional[str]
    txreceipt_status: Optional[str]

    def __hash__(self):
        return hash(self.hash)

    @classmethod
    def mongo_client(cls, chain_id: int) -> MongoClient:
        c = client(cls.__name__, chain_id)
        c.create_index("hash", unique=True)
        return c
