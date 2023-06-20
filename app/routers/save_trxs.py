import logging
from fastapi import APIRouter

from middlewares.supported_chains import check_chains
from utils.trx.save_trxs import save_users_token_trxs
from schemas.request_schemas import UsersData
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_users_trxs", response_model=BaseResponse)
async def save_users_trxs(
    request: UsersData
):
    check_chains(request.chainIds)
    try:
        save_users_token_trxs(
            request.chainIds,
            request.userAddresses
        )
        return {"result": "Successfully saved trxs"}
    except Exception as e:
        logging.exception(e)
