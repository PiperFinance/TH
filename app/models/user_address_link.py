from typing import List, Optional
from sqlmodel import Field, SQLModel


class UserAddressLink(SQLModel, table=True):
    userId: Optional[int] = Field(foreign_key="user.id", primary_key=True)
    addressId: Optional[str] = Field(
        foreign_key="address.address", primary_key=True)
