from web3 import Web3
from typing import List
from pydantic import BaseModel

from configs.constant_config import constants
from utils.types import ChainId, Url, ApiKey, MongoClient


class Chain(BaseModel):
    chainId: ChainId

    @staticmethod
    def supported_chains() -> List[ChainId]:
        return [5, 5001]

    @property
    def url(self) -> Url:
        return constants.chains[self.chainId]["apiEndPoint"]

    @property
    def api_keys(self) -> List[ApiKey]:
        return constants.api_keys[self.chainId]

    @property
    def w3(self) -> Web3:
        rpc = constants.chains[self.chainId]["rpcUrls"]["default"]
        return Web3(Web3.HTTPProvider(rpc))

    @property
    def wNative(self):
        return constants.chains[self.chainId]["wNativeCurrency"]

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
