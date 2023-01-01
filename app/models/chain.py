from web3 import Web3
from typing import List, Dict
from pydantic import BaseModel

from configs.constant_config import constants
from utils.types import ChainId, Url, ApiKey, MongoClient


class Chain(BaseModel):
    chainId: ChainId

    @staticmethod
    def supported_chains() -> List[ChainId]:
        return [250, 1, 10, 137, 42161, 42220, 56, 100, 1284, 43114, 1313161554]

    @property
    def url(self) -> Url:
        return constants.chains[self.chainId]["apiEndpoint"]

    @property
    def api_keys(self) -> List[ApiKey]:
        return constants.api_keys[self.chainId]

    @property
    def w3(self) -> Web3:
        rpc = constants.chains[self.chainId]["defaultRpcUrl"]
        return Web3(Web3.HTTPProvider(rpc))

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
