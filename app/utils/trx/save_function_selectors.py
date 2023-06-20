import  json
import logging
from pymongo import errors
from pydantic import parse_obj_as
from typing import List

from models import FunctionSelector, ArgType
from schemas.request_schemas import FunctionSelectorSchema
from configs.postgres_config import InitializePostgres


def save_function_selectors(function_selectors: List[FunctionSelectorSchema]):
    for function_selector in function_selectors:
        try:
            function_selector = make_function_selector_obj(function_selector)
            insert_function_selector(function_selector)
        except Exception as e:
            logging.exception(e)
            continue


def save_function_selector(function_selector: FunctionSelectorSchema):
    function_selector = make_function_selector_obj(function_selector)
    insert_function_selector(function_selector)


def make_function_selector_obj(function_selector: FunctionSelectorSchema):
    try:
        function_selector = function_selector.dict()

        if function_selector.get('args'):
            args = []
            for arg in function_selector.get("args"):
                args.append((arg[0], ArgType.convert(arg[1])))
            function_selector["args"] = json.dumps(args)

        function_selector = parse_obj_as(
            FunctionSelector, function_selector)
        return function_selector
    except Exception as e:
        logging.exception(e)
        return None

def insert_function_selector(
    function_selector: FunctionSelector
):
    ps = InitializePostgres()
    with ps.session as session:
        try:
            session.add(function_selector)
            session.commit()
        except Exception as e:
            logging.exception(e)
            return
