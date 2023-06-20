from sqlmodel import Field, SQLModel

from .chain import Chain
from .token import Token
from .address import Address
from configs.mongo_config import client


class TrxWithNoLabels(SQLModel, table=True):
    chainId: int = Field(foreign_key=Chain.id)
    hash: str = Field(primary_key=True)
