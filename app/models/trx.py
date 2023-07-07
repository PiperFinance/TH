from enum import Enum
import pymongo
from pydantic import BaseModel
from typing import List, Optional, Any, Union

from . import Chain
from .token import Token
from configs.mongo_config import client
from utils.types import Address, StringBlockNumber, Collection


class TrxType(Enum):
    NORMAL_TRX = "normal"
    TOKEN_TRX = "token"

    @property
    def url(self) -> str:
        if self == self.NORMAL_TRX:
            return "?module=account&action=txlist"
        elif self == self.TOKEN_TRX:
            return "?module=account&action=tokentx"
        else:
            return ""


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
    def mongo_client(cls, chain_id: int) -> Collection:
        c = client(cls.__name__, chain_id)
        c.create_index("hash", unique=True)
        c.create_index([("timeStamp", pymongo.DESCENDING)], background=True)
        return c


# class Base(DeclarativeBase):
#     pass


# class Trx(Base, Chain):
#     __tablename__: "Trx"

#     userAddress: Mapped[Address]
#     chainIdUserAddress: Mapped[str] = mapped_column(primary_key=True)
#     type: Mapped[Optional[int]]
#     labels: Mapped[Optional[List["Label"]]]
#     tokens: Mapped[Optional[List["Token"]]]
#     blockNumber: StringBlockNumber
#     timeStamp: Mapped[int]
#     hash: Mapped[str]
#     nonce: Mapped[str]
#     blockHash: Mapped[str]
#     fromAddress: Mapped[Address]
#     contractAddress: Mapped[Optional[str]]
#     to: Mapped[Union[Address, str]]
#     value: Mapped[str]
#     transactionIndex: Mapped[str]
#     gas: Mapped[str]
#     gasPrice: Mapped[str]
#     gasUsed: Mapped[str]
#     cumulativeGasUsed: Mapped[str]
#     input: Mapped[Optional[str]]
#     confirmations: Mapped[str]
#     isError: Mapped[Optional[str]]
#     txreceipt_status: Mapped[Optional[str]]
