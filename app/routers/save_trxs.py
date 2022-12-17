import logging
from fastapi import APIRouter

from utils.trx.save_trxs import save_user_chain_token_trxs
from schemas.request_schemas import (
    UserData,
    UsersData
)
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_user_trxs", response_model=BaseResponse)
async def save_user_chain_trxs(
    request: UserData
):
    try:
        save_user_chain_token_trxs(
            request.chainId,
            request.userAddress
        )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)


@routes.post("/save_multipule_users_trxs", response_model=BaseResponse)
async def save_multipule_users_chain_trxs(
    request: UsersData
):
    try:
        for address in request.user_addresses:
            save_user_chain_token_trxs(
                request.chainId,
                address
            )
        return BaseResponse()
    except Exception as e:
        logging.exception(e)
