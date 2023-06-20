from web3 import Web3
from typing import List, Optional
from sqlmodel import Field, SQLModel

from configs.constant_config import constants
from .network import Network


class Chain(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    isMainnet: bool = Field(default=True)
    networkId: int = Field(foreign_key=Network.id)

    @staticmethod
    def supported_chains() -> List[int]:
        return [250, 1, 10, 137, 42161, 42220, 56, 100, 1284, 43114, 1313161554]


    @property
    def url(self):
        return constants.chains[self.id]["apiEndPoint"]

    @property
    def api_keys(self):
        return constants.api_keys[self.id]

    @property
    def w3(self):
        rpc = constants.chains[self.id]["rpcUrls"]["default"]
        return Web3(Web3.HTTPProvider(rpc))

    @property
    def wNative(self):
        return constants.chains[self.id]["wNativeCurrency"]
