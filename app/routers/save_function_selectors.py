import logging
from fastapi import APIRouter
from typing import List

from utils.trx.save_function_selectors import (
    save_function_selectors,
    save_function_selector
)
from schemas.request_schemas import FunctionSelectorSchema
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_function_selectors", response_model=BaseResponse)
async def save_func_selectors(
    function_selectors: FunctionSelectorSchema
):
    try:
        save_function_selectors(function_selectors)
        return {"result": "Successfully saved function selectors"}
    except Exception as e:
        logging.exception(e)


@routes.post("/save_function_selector", response_model=BaseResponse)
async def save_func_selector(function_selector: List[FunctionSelectorSchema]):
    try:
        save_function_selector(function_selector)
        return {"result": "Successfully saved function selector"}
    except Exception as e:
        logging.exception(e)
