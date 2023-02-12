import logging
from fastapi import APIRouter

from utils.trx.get_trxs_with_no_labels import get_all_trxs_with_no_labels
from schemas.response_schema import TrxWithNoLabelsList

routes = APIRouter()


@routes.get("/get_trxs_with_no_labels", response_model=TrxWithNoLabelsList)
async def get_trxs_with_no_labels(
    pageSize: int,
    pageNumber: int,
):
    try:

        skip = pageSize * (pageNumber - 1)

        trxs, trxs_len = get_all_trxs_with_no_labels(skip, pageSize)
        return {
            "result": {
                "count": trxs_len,
                "trxs": trxs
            }
        }
    except Exception as e:
        logging.exception(e)
