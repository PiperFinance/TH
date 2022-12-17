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


def cache_function_selector(
    hex_signature: str,
    text_signature: str
):
    try:
        cache_client().set(
            f'{RedisNamespace.FUNC_SELECTOR.value}{hex_signature}',
            text_signature
        )
    except Exception as e:
        logging.exception(e)


def get_function_selector_from_redis(signature_hex: str):
    try:
        return cache_client().get(
            f'{RedisNamespace.FUNC_SELECTOR.value}{signature_hex}')
    except Exception as e:
        logging.exception(e)


def cache_last_cached_function_selector_page(
    page_number: int
):
    cache_client().set(
        str(RedisNamespace.LAST_CACHED_FUN_SELECTOR_PAGE.value),
        page_number
    )


def get_last_cached_function_selector_page_from_redis():
    try:
        return int(cache_client().get(str(RedisNamespace.LAST_CACHED_FUN_SELECTOR_PAGE.value)))
    except Exception as e:
        logging.exception(e)
