from typing import List, Optional, Any
from pydantic import BaseModel

from models import Trx, TrxWithNoLabels, FunctionSelector


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class TrxResult(BaseModel):
    count: Optional[int]
    trxs: Optional[List[Trx]]


class TrxList(BaseResponse):
    result: Optional[TrxResult]


class TrxWithNoLabelsResult(BaseModel):
    count = Optional[int]
    trxs: Optional[List[TrxWithNoLabels]]

    class Config:
        arbitrary_types_allowed = True


class TrxWithNoLabelsList(BaseResponse):
    result: Optional[TrxWithNoLabelsResult]

    class Config:
        arbitrary_types_allowed = True


class FunctionSelectorResult(BaseModel):
    count: Optional[int]
    function_selectors: Optional[List[FunctionSelector]]


class FunctionSelectorList(BaseResponse):
    result: Optional[FunctionSelectorResult]
