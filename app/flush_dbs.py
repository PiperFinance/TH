from configs.redis_config import cache_client
from models import Chain, Trx, FunctionSelector


def flush_redis():
    keys = cache_client().keys("*")
    cache_client().delete(*keys)


def flush_mongo():
    for chain_id in Chain.supported_chains():
        Trx.mongo_client(chain_id).drop()

    FunctionSelector.mongo_client().drop()
