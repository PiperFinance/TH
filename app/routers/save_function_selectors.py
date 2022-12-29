import logging
from fastapi import APIRouter

from utils.trx.save_function_selectors import (
    save_function_selectors,
    save_function_selector
)
from schemas.request_schemas import (
    FunctionSelectorSchema,
    FunctionSelectorsSchema
)
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_function_selectors", response_model=BaseResponse)
async def save_func_selectors(
    request: FunctionSelectorsSchema
):
    try:
        save_function_selectors(request.functionSelectors)
        return {"result": "Successfully saved function selectors"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_function_selector", response_model=BaseResponse)
async def save_func_selector(request: FunctionSelectorSchema):
    try:
        save_function_selector(request)
        return {"result": "Successfully saved function selector"}
    except Exception as e:
        logging.exception(e)
