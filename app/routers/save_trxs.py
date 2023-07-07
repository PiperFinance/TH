import logging
from fastapi import APIRouter

from middlewares.supported_chains import check_chain, check_chains
from utils.trx.update_trxs import update_users_chain_token_trxs, update_users_token_trxs
from utils.trx.save_trxs import save_users_chain_token_trxs, save_users_token_trxs
from schemas.request_schemas import UsersData, UsersChainData
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_users_chain_trxs", response_model=BaseResponse)
async def save_users_chain_trxs(request: UsersChainData):
    check_chain(request.chainId)
    update_users_chain_token_trxs(request.chainId, request.userAddresses)
    await save_users_chain_token_trxs(request.chainId, request.userAddresses, 1)
    return {"result": "Successfully saved trxs"}


@routes.post("/save_users_trxs", response_model=BaseResponse)
async def save_users_trxs(request: UsersData):
    check_chains(request.chainIds)
    # update_users_token_trxs(request.chainIds, request.userAddresses)
    await save_users_token_trxs(
        request.chainIds, request.userAddresses, request.scanIterations or 1
    )
    return {"result": "Successfully saved trxs"}
