import logging
from typing import List, Union, Dict
from pydantic import parse_obj_as

from models import FunctionSelector
from utils.types import HexStr


def get_all_function_selectors(
    skip: int = 0,
    limit: int = 0
) -> List[FunctionSelector]:
    client = FunctionSelector.mongo_client()

    if limit < 1:
        function_selectors = list(client.find())

    if skip < 1:
        function_selectors = list(client.find().limit(limit))

    else:
        function_selectors = list(client.find().skip(skip).limit(limit))

    if function_selectors in [None, []]:
        return
    function_selector_list = []

    for function_selector in function_selectors:
        function_selector_list.append(parse_obj_as(
            FunctionSelector, function_selector))

    return function_selector_list


def get_all_function_selectors_len():
    client = FunctionSelector.mongo_client()
    return len(list(client.find()))


def get_function_selectors(
    hexs: Union[List[HexStr], HexStr],
) -> List[FunctionSelector]:

    if type(hexs) == list:
        client = FunctionSelector.mongo_client()
        hs = []
        for hex in hexs:
            hs.append({"hex": hex})
        query = {"$or": hs}
        function_selector_list = list(client.find(query))
        if function_selector_list in [None, []]:
            return
        function_selectors = []
        for function_selector in function_selector_list:
            function_selectors.append(
                make_function_selector_obj(function_selector))
        return function_selectors
    else:
        return get_function_selector(hexs)


def get_function_selector(hex: HexStr):
    try:
        client = FunctionSelector.mongo_client()
        function_selector = client.find_one({"hex": hex})
        if function_selector:
            return make_function_selector_obj(function_selector)
    except Exception as e:
        logging.exception(e)
        return None


def make_function_selector_obj(function_selector: Dict):
    try:
        return parse_obj_as(
            FunctionSelector, function_selector)
    except Exception as e:
        logging.exception(e)
        return None
