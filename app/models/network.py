from enum import IntEnum
from typing import List, Optional
from sqlmodel import Field, SQLModel


class NetworkType(IntEnum):
    EVM = 1
    TRON = 2
    SOLANA = 3
    TON = 4
    BITCOIN = 5
    EOS = 6


class Network(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    # chains: List["Chain"] = Relationship(back_populates="networkType")
