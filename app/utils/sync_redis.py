import logging

from .types import Address, ChainId
from configs.redis_config import RedisNamespace, cache_client


def cache_last_block_number(
    chain_id: ChainId,
    user_address: Address,
    block_number: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.LAST_CACHED_BLOCKNUMBER.value}:{chain_id}:{user_address}',
            block_number
        )
    except Exception as e:
        logging.exception(e)


def get_last_block_number(
    chain_id: ChainId,
    user_address: Address
):
    try:
        return int(cache_client().get(
            f'{RedisNamespace.LAST_CACHED_BLOCKNUMBER.value}:{chain_id}:{user_address}'))
    except Exception as e:
        logging.exception(e)
        return 0
