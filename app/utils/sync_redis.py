import logging

from .types import Address, ChainId
from configs.redis_config import RedisNamespace, cache_client


def cache_last_block_number(
    chain_id: ChainId, user_address: Address, trx_type: str, block_number: str
):
    try:
        cache_client().set(
            f"{RedisNamespace.LAST_CACHED_BLOCKNUMBER.value}:{trx_type}:{chain_id}:{user_address}",
            block_number,
        )
    except Exception as e:
        logging.exception(e)


def get_last_block_number(chain_id: ChainId, user_address: Address, trx_type: str):
    try:
        block_number = cache_client().get(
            f"{RedisNamespace.LAST_CACHED_BLOCKNUMBER.value}:{trx_type}:{chain_id}:{user_address}"
        )
        if block_number:
            return int(block_number)
    except Exception as e:
        logging.exception(e)
        return 0
