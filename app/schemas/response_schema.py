from typing import List, Optional, Any
from pydantic import BaseModel

from models import Trx, FunctionSelector


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class TrxResult(BaseModel):
    count: Optional[int]
    trxs: Optional[List[Trx]]


class TrxList(BaseResponse):
    result: Optional[TrxResult]


class FunctionSelectorResult(BaseModel):
    count: Optional[int]
    function_selectors: Optional[List[FunctionSelector]]


class FunctionSelectorList(BaseResponse):
    result: Optional[FunctionSelectorResult]
