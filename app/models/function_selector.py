import re
import logging
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
            return ArgType.INT_LIST.value

        uint_array_like_regex = re.compile(r'^uint[0-9]*\[\]$')
        uint_match = uint_array_like_regex.match(value)
        if uint_match is not None:
            return ArgType.UINT_LIST.value

        int_like_regex = re.compile(r'^int[0-9]')
        int_match = int_like_regex.match(value)
        if int_match is not None:
            return ArgType.INT.value

        uint_like_regex = re.compile(r'^uint[0-9]')
        uint_match = uint_like_regex.match(value)
        if uint_match is not None:
            return ArgType.UINT.value

        bytes_array_like_regex = re.compile(r"^bytes[0-9]*\[\]$")
        bytes_match = bytes_array_like_regex.match(value)
        if bytes_match is not None:
            return ArgType.BYTES_LIST.value

        bytes_like_regex = re.compile(r'^bytes[0-9]')
        bytes_match = bytes_like_regex.match(value)
        if bytes_match is not None:
            return ArgType.BYTES.value

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

        if self.value == ArgType.ADDRESS.value:
            try:
                return Web3.toChecksumAddress(f"0x{val[24:]}")
            except Exception as e:
                logging.exception(e)
                return val
        if self.value in [ArgType.INT.value, ArgType.UINT.value]:
            try:
                return int(val, 16)
            except Exception as e:
                logging.exception(e)
                return val
        if self.value == ArgType.BYTES.value:
            try:
                return bytes.fromhex(val)
            except Exception as e:
                logging.exception(e)
                return val
        if self.value == ArgType.STRING.value:
            try:
                return bytes.fromhex(val).decode('utf-8')
            except Exception as e:
                logging.exception(e)
                return val
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
        c = function_selector_client(cls.__name__)
        c.create_index("hex", unique=True)
        return c
