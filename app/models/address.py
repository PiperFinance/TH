from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from .user_address_link import UserAddressLink
from .network import Network


class Address(SQLModel, table=True):
    address: str = Field(primary_key=True)
    networkId: int = Field(foreign_key=Network.id)
    users: List["User"] = Relationship(
        link_model=UserAddressLink, back_populates="addresses"
    )
