import logging
from fastapi import APIRouter

from utils.trx.save_trxs_with_no_labels import save_all_trxs_with_no_labels
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.get("/save_trxs_with_no_labels", response_model=BaseResponse)
async def save_trxs_with_no_labels(
):
    try:
        save_all_trxs_with_no_labels()
        return {"result": "Successfully saved trxs"}
    except Exception as e:
        logging.exception(e)
