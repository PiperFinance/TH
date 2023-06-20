from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from .user_address_link import UserAddressLink


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    addresses: List["Address"] = Relationship(
        link_model=UserAddressLink,
        back_populates="users"
    )
