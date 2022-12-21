import logging
from typing import List
from fastapi import APIRouter, Query

from utils.trx.get_function_selectors import (
    get_all_function_selectors,
    get_all_function_selectors_len,
    get_function_selectors
)
from schemas.response_schema import FunctionSelectorList
from utils.types import HexStr

routes = APIRouter()


@routes.get("/get_all_function_selectors_len")
async def get_all_func_selectors_len() -> int:
    try:
        return get_all_function_selectors_len()
    except Exception as e:
        logging.exception(e)


@routes.get(
    "/get_all_function_selectors",
    response_model=FunctionSelectorList
)
async def get_all_func_selectors(
    pageSize: int,
    pageNumber: int
):
    try:
        skip = pageSize * (pageNumber - 1)
        result = get_all_function_selectors(skip, pageSize)
        return {"result": result}
    except Exception as e:
        logging.exception(e)


@routes.get(
    "/get_function_selectors",
    response_model=FunctionSelectorList
)
async def get_func_selectors(
    # hexs: List[HexStr] | None = Query(default=None)
    hex: List[HexStr] or None = Query(default=None)
):
    try:
        result = get_function_selectors(hex)
        return {"result": result}
    except Exception as e:
        logging.exception(e)
