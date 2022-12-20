import logging
from fastapi import APIRouter

from utils.trx.save_trxs import save_users_chain_token_trxs
from schemas.request_schemas import UsersData
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_users_trxs", response_model=BaseResponse)
async def save_users_chain_trxs(
    request: UsersData
):
    try:
        save_users_chain_token_trxs(
            request.chainId,
            request.userAddresses
        )
        return {"result": "Successfully saved trxs"}
    except Exception as e:
        logging.exception(e)
