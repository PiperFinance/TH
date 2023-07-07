import logging
from fastapi import APIRouter, HTTPException

from utils.trx.save_function_selectors import (
    save_function_selectors,
    save_function_selector,
)
from schemas.request_schemas import FunctionSelectorSchema, FunctionSelectorsSchema
from schemas.response_schema import BaseResponse
from configs.constant_config import constants

routes = APIRouter()


@routes.post("/save_function_selectors", response_model=BaseResponse)
async def save_func_selectors(request: FunctionSelectorsSchema):
    if request.secret != constants.save_secret:
        raise HTTPException(401, "Bad Secret")
    save_function_selectors(request.functionSelectors)
    return {"result": "Successfully saved function selectors"}


@routes.post("/save_function_selector", response_model=BaseResponse)
async def save_func_selector(request: FunctionSelectorSchema):
    if request.secret != constants.save_secret:
        raise HTTPException(401, "Bad Secret")
    save_function_selector(request)
    return {"result": "Successfully saved function selector"}
