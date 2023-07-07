from web3 import Web3
from typing import Dict, Generator, List
from pydantic import BaseModel, Field

from configs.constant_config import constants
from utils.types import ChainId, Url, ApiKey, MongoClient


class Chain(BaseModel):
    chainId: ChainId
    _key_gens: Dict[ChainId, Generator[ApiKey, None, None]] = dict()

    @staticmethod
    def supported_chains() -> List[ChainId | int]:
        return [250, 1, 10, 137, 42161, 42220, 56, 100, 1284, 43114, 1313161554]

    @property
    def url(self) -> Url:
        return constants.chains[self.chainId]["apiEndPoint"]

    @property
    def next_api_key(self) -> ApiKey:
        if self.chainId not in self._key_gens:
            self._key_gens[self.chainId] = constants.api_key_generator(self.chainId)
        return next(self._key_gens[self.chainId])

    @property
    def api_keys(self) -> Generator[ApiKey, None, None]:
        if self.chainId not in self._key_gens:
            self._key_gens[self.chainId] = constants.api_key_generator(self.chainId)
        return self._key_gens[self.chainId]

    @property
    def w3(self) -> Web3:
        rpc = constants.chains[self.chainId]["rpcUrls"]["default"]
        return Web3(Web3.HTTPProvider(rpc))

    @property
    def wNative(self):
        return constants.chains[self.chainId]["wNativeCurrency"]

    @property
    def req_timeout(self) -> float:
        return 5 * 60

    @classmethod
    def mongo_client(cls, chain_id: ChainId) -> MongoClient:
        raise NotImplementedError
