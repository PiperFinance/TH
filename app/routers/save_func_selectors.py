import logging
from pydantic import parse_obj_as
from fastapi import APIRouter
from typing import List

from models import FunctionSelector
from utils.trx.save_function_selectors import (
    save_function_selectors,
    save_function_selector
)
from schemas.response_schema import BaseResponse

routes = APIRouter()


@routes.post("/save_function_selectors", response_model=BaseResponse)
async def save_func_selectors(
    function_selectors: List[FunctionSelector]
):
    try:
        save_function_selectors(function_selectors)
        return parse_obj_as(BaseResponse, {"result": "Successfully saved function selectors"})
    except Exception as e:
        logging.exception(e)


@routes.post("/save_function_selector", response_model=BaseResponse)
async def save_func_selector(function_selector: FunctionSelector):
    try:
        save_function_selector(function_selector)
        return parse_obj_as(BaseResponse, {"result": "Successfully saved function selector"})
    except Exception as e:
        logging.exception(e)
