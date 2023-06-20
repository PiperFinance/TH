from typing import List, Optional, Any
from pydantic import BaseModel

from models import Token, Label, TrxWithNoLabels


class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None


class TrxSchema(BaseModel):
    hash: str
    chainId: int
    userAddress: str
    fromAddress: str
    toAddress: Optional[str]
    labels: Optional[List[Label]]
    tokens: Optional[List[Token]]
    type: Optional[int]
    contractAddress: Optional[str]
    input: Optional[str]
    isError: Optional[str]
    txreceipt_status: Optional[str]
    blockNumber: str
    timeStamp: int
    nonce: str
    blockHash: str
    value: str
    transactionIndex: str
    gas: str
    gasPrice: str
    gasUsed: str
    cumulativeGasUsed: str
    confirmations: str


class TrxResult(BaseModel):
    count: Optional[int]
    trxs: Optional[List[TrxSchema]]


class TrxList(BaseResponse):
    result: Optional[TrxResult]


class TrxWithNoLabelsResult(BaseModel):
    count: Optional[int]
    trxs: Optional[List[TrxWithNoLabels]]


class TrxWithNoLabelsList(BaseResponse):
    result: Optional[TrxWithNoLabelsResult]


class FunctionSelectorSchema(BaseModel):
    hex: str
    text: str
    args: Optional[List[List]]


class FunctionSelectorResult(BaseModel):
    count: Optional[int]
    function_selectors: Optional[List[FunctionSelectorSchema]]


class FunctionSelectorList(BaseResponse):
    result: Optional[FunctionSelectorResult]
