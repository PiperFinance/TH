import logging
from fastapi import APIRouter, Query
from typing import List

from utils.trx.get_trxs import (
    get_users_chain_token_trxs_len,
    get_users_chain_token_trxs
)
from schemas.response_schema import TrxList
from utils.types import ChainId, Address

routes = APIRouter()


@routes.get("/get_users_trxs_len")
async def get_users_chain_trxs_len(
    chainId: ChainId,
    # userAddress: List[Address] | None = Query(default=None)
    userAddress: List[Address] or None = Query(default=None)
) -> int:
    try:
        trx_len = get_users_chain_token_trxs_len(chainId, userAddress)
        return trx_len
    except Exception as e:
        logging.exception(e)


@routes.get("/get_users_trxs", response_model=TrxList)
async def get_users_chain_trxs(
    chainId: ChainId,
    pageSize: int,
    pageNumber: int,
    # userAddress: List[Address] | None = Query(default=None)
    userAddress: List[Address] or None = Query(default=None)
):
    try:
        skip = pageSize * (pageNumber - 1)

        trxs = get_users_chain_token_trxs(
            chainId, userAddress, skip, pageSize)
        return {"result": trxs}
    except Exception as e:
        logging.exception(e)
