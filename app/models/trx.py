from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Union

from . import Chain
from .token import Token
from configs.mongo_config import client
from utils.types import Address, StringBlockNumber, Symbol, Name, Decimal, MongoClient


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
    value: Union[str, int]


class Trx(Chain):
    userAddress: Address
    labels: Optional[List[Label]]
    token: Optional[Token]
    blockNumber: StringBlockNumber
    timeStamp: int
    hash: str
    nonce: str
    blockHash: str
    fromAddress: Address
    contractAddress: Address
    to: Address
    value: str
    tokenName: Name
    tokenSymbol: Symbol
    tokenDecimal: Decimal
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    input: str
    confirmations: str

    @classmethod
    def mongo_client(cls, chain_id: int) -> MongoClient:
        return client(cls.__name__, chain_id, "hash")
