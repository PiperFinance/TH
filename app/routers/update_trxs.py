import logging
from fastapi import APIRouter

from middlewares.supported_chains import check_chain, check_chains
from utils.trx.update_trxs import (
    update_users_chain_token_trxs,
    update_users_token_trxs
)
from schemas.request_schemas import UsersData, UsersChainData
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.put("/update_users_chain_trxs", response_model=BaseResponse)
async def update_users_chain_trxs(
    request: UsersChainData
):
    check_chain(request.chainId)
    try:
        update_users_chain_token_trxs(
            request.chainId,
            request.userAddresses
        )
        return {"result": "Successfully updated trxs"}
    except Exception as e:
        logging.exception(e)


@routes.put("/update_users_trxs", response_model=BaseResponse)
async def update_users_trxs(
    request: UsersData
):
    check_chains(request.chainIds)
    try:
        update_users_token_trxs(
            request.chainIds,
            request.userAddresses
        )
        return {"result": "Successfully updated trxs"}
    except Exception as e:
        logging.exception(e)
