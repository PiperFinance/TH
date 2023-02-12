from pydantic import BaseModel

from configs.mongo_config import _client
from utils.types import ChainId, MongoClient


class TrxWithNoLabels(BaseModel):
    chainId: ChainId
    hash: str
    chainIdHash: str


    @classmethod
    def mongo_client(cls) -> MongoClient:
        c = _client(cls.__name__)
        c.create_index("chainIdHash", unique=True)
        return c
