import logging
from fastapi import APIRouter

from utils.trx.delete_trxs_with_no_trxs import delete_trxs
from schemas.request_schemas import TrxsWithNoLabelsSchema
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.delete("/delete_trxs_with_no_labels", response_model=BaseResponse)
async def delete_trxs_with_no_label(
    request: TrxsWithNoLabelsSchema
):
    try:
        delete_trxs(request.trxs)
        return {"result": "Successfully deleted trxs"}

    except Exception as e:
        logging.exception(e)
