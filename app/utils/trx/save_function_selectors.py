import logging
from pydantic import parse_obj_as
from typing import List

from models import FunctionSelector, ArgType
from schemas.request_schemas import FunctionSelectorSchema
from utils.types import MongoClient


def save_function_selectors(function_selectors: List[FunctionSelectorSchema]):
    client = FunctionSelector.mongo_client()
    for function_selector in function_selectors:
        try:
            function_selector = make_function_selector_obj(function_selector)
            insert_function_selector(client, function_selector)
        except Exception as e:
            logging.exception(e)
            continue


def save_function_selector(function_selector: FunctionSelectorSchema):
    client = FunctionSelector.mongo_client()
    function_selector = make_function_selector_obj(function_selector)
    insert_function_selector(client, function_selector)


def make_function_selector_obj(function_selector: FunctionSelectorSchema):
    try:
        function_selector = function_selector.dict()

        args = []
        for arg in function_selector.get("args"):
            args.append((arg[0], ArgType.convert(arg[1])))
        function_selector["args"] = args

        function_selector = parse_obj_as(
            FunctionSelector, function_selector)
        return function_selector
    except Exception as e:
        logging.exception(e)
        return None


def insert_function_selector(
    client: MongoClient,
    function_selector: FunctionSelector
):
    try:
        function_selector = function_selector.dict()
        client.insert_one(function_selector)
    except Exception as e:
        logging.exception(e)
