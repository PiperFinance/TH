import logging
from pydantic import parse_obj_as
from fastapi import APIRouter, Query
from typing import List

from utils.trx.get_trxs import (
    get_user_chain_token_trxs_len,
    get_user_chain_token_trxs
)
from schemas.response_schema import TrxList
from utils.types import ChainId, Address

routes = APIRouter()


@routes.get("/get_user_trxs_len")
async def get_user_chain_trxs_len(
    chain_id: ChainId,
    user_address: Address
) -> int:
    try:
        return get_user_chain_token_trxs_len(
            chain_id,
            user_address
        )
    except Exception as e:
        logging.exception(e)


@routes.get("/get_user_trxs", response_model=TrxList)
async def get_user_chain_trxs(
    chain_id: ChainId,
    user_address: Address,
    page_number: int,
    page_size: int
):
    try:
        skip = page_size * (page_number - 1)
        result = get_user_chain_token_trxs(
            chain_id,
            user_address,
            skip,
            page_size
        )
        return parse_obj_as(TrxList, {"result": result})
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_trxs_len")
async def get_multipule_users_chain_trxs_len(
    chain_id: int,
    # user_addresses: List[Address] | None = Query(default=None)
    user_addresses: List[Address] or None = Query(default=None)

) -> int:
    try:
        trx_len = 0
        for user_address in user_addresses:
            trx_len += get_user_chain_token_trxs_len(
                chain_id, user_address)
        return trx_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_multipule_users_trxs", response_model=TrxList)
async def get_multipule_users_chain_trxs(
    chain_id: int,
    page_size: int,
    page_number: int,
    # user_addresses: List[Address] | None = Query(default=None)
    user_addresses: List[Address] or None = Query(default=None)

):
    try:
        skip = page_size * (page_number - 1)

        trxs = []
        for address in user_addresses:
            trxs.extend(get_user_chain_token_trxs(
                chain_id,
                address,
                skip,
                page_size
            )
            )
        return parse_obj_as(TrxList, {"result": trxs})
    except Exception as e:
        logging.exception(e)
