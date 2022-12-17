from typing import List
from pydantic import BaseModel

from configs.constant_config import constants
from utils.types import ChainId, Url, ApiKey, MongoClient


class Chain(BaseModel):
    chainId: ChainId

    @staticmethod
    def supported_chains() -> List[ChainId]:
        return [250, 1, 3, 4, 5, 10, 42, 137, 42161, 42220, 80001]

    @property
    def url(self) -> Url:
        return constants.chains[self.chainId]["apiEndpoint"]

    @property
    def api_keys(self) -> List[ApiKey]:
        return constants.api_keys[self.chainId]

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
