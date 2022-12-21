from typing import List, Optional, Any
from pydantic import BaseModel

from models import Trx, FunctionSelector


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class TrxList(BaseResponse):
    result: Optional[List[Trx]]


class FunctionSelectorList(BaseResponse):
    result: Optional[List[FunctionSelector]]
