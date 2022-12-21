from pydantic import BaseModel
from typing import List, Optional, Union

from . import Chain
from configs.mongo_config import client
from utils.types import Address, StringBlockNumber, Symbol, Name, Decimal, MongoClient


class Label(BaseModel):
    title: str
    value: Union[str, int]


class Trx(Chain):
    userAddress: Address
    labels: Optional[List[Label]]
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

    # def __hash__(self):
    #     return hash(self.hash)

    # def __eq__(self, other_trx):
    #     return self.hash == other_trx.hash

    # def update(self, other_trx):
    #     if self == other_trx:
    #         self.input = other_trx.input

    @classmethod
    def mongo_client(cls, chain_id: int) -> MongoClient:
        c = client(cls.__name__, chain_id)
        c.create_index(
            "hash",
            unique=True
        )
        return c
