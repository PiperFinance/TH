import re
from enum import Enum
from web3 import Web3
from pydantic import BaseModel
from typing import List, Optional, NamedTuple
from configs.mongo_config import function_selector_client
from utils.types import HexStr


class ArgType(Enum):
    ADDRESS = "address"
    ADDRESS_LIST = "address[]"
    INT = "int"
    INT_LIST = "int[]"
    UINT = "uint"
    UINT_LIST = "uint[]"
    BYTES = "bytes"
    BYTES_LIST = "bytes[]"
    TUPLE = "tuple"
    TUPLE_LIST = "tuple[]"
    STRING = "string"
    STRING_LIST = "string[]"
    BOOL = "bool"
    BOOL_LIST = "bool[]"

    @classmethod
    def convert(cls, value: str):
        int_array_like_regex = re.compile(r"^int[0-9]*\[\]$")
        int_match = int_array_like_regex.match(value)
        if int_match is not None:
            return "int[]"

        uint_array_like_regex = re.compile(r'^uint[0-9]*\[\]$')
        uint_match = uint_array_like_regex.match(value)
        if uint_match is not None:
            return "uint[]"

        int_like_regex = re.compile(r'^int[0-9]')
        int_match = int_like_regex.match(value)
        if int_match is not None:
            return "int"

        uint_like_regex = re.compile(r'^uint[0-9]')
        uint_match = uint_like_regex.match(value)
        if uint_match is not None:
            return "uint"

        bytes_array_like_regex = re.compile(r"^bytes[0-9]*\[\]$")
        bytes_match = bytes_array_like_regex.match(value)
        if bytes_match is not None:
            return "bytes[]"

        bytes_like_regex = re.compile(r'^bytes[0-9]')
        bytes_match = bytes_like_regex.match(value)
        if bytes_match is not None:
            return "bytes"

        else:
            return value

    def parse(self, val):
        # match self:
        #     case self.ADDRESS:
        #         return Web3.toChecksumAddress(f"0x{val[24:]}")
        #     case self.INT or self.UINT:
        #         return int(val, 16)
        #     case _:
        #         return val

        if self.value == "address":
            return Web3.toChecksumAddress(f"0x{val[24:]}")
        if self.value in ["int", "uint"]:
            # return Web3.toInt(val)
            return int(val, 16)
        if self.value == "bytes":
            return Web3.toBytes(val)
        else:
            return val


class Arg(NamedTuple):
    title: str
    type: ArgType


class FunctionSelector(BaseModel):
    hex: HexStr
    text: str
    args: Optional[List[Arg]]

    def dict(self, *a, **kwd):
        if self.args:
            self.args = [(_.title, _.type.value) for _ in self.args]
        return super().dict(*a, **kwd)

    @classmethod
    def mongo_client(cls):
        return function_selector_client(cls.__name__, "hex")
