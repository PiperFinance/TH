import json
import logging
from typing import List, Union, Dict
from pydantic import parse_obj_as
from sqlmodel import select

from models import FunctionSelector, Arg
from utils.types import HexStr
from configs.postgres_config import InitializePostgres
from schemas.response_schema import FunctionSelectorSchema


def get_all_function_selectors(
    skip: int = 0,
    limit: int = 0
) -> List[FunctionSelector]:

    ps = InitializePostgres()
    with ps.session as session:

        if skip >= 1 and limit >= 1:
            statement = select(FunctionSelector)
            results = session.exec(statement)
            function_selectors = results.all()[skip:skip + limit]

        elif skip < 1 and limit >= 1:
            statement = select(FunctionSelector).limit(limit)
            results = session.exec(statement)
            function_selectors = results.all()

        else:
            statement = select(FunctionSelector)
            results = session.exec(statement)
            function_selectors = results.all()

    return create_function_selectors_schema(function_selectors)


def get_all_function_selectors_len():
    ps = InitializePostgres()
    with ps.session as session:
        statement = select(FunctionSelector)
        results = session.exec(statement)
        return len(results.all())


def get_function_selectors(
    hexs: Union[List[HexStr], HexStr],
) -> List[FunctionSelector]:

    if type(hexs) == list:
        statement = select(FunctionSelector).where(
            FunctionSelector.hex.in_(hexs))
    else:
        statement = select(FunctionSelector).where(
            FunctionSelector.hex == hexs)

    ps = InitializePostgres()
    with ps.session as session:
        function_selectors = session.exec(statement).all()

    return create_function_selectors_schema(function_selectors)


def get_function_selector(hex: HexStr):
    ps = InitializePostgres()
    with ps.session as session:
        statement = select(FunctionSelector).where(FunctionSelector.hex == hex)
        result = session.exec(statement)
        function_selector = result.first()

    if function_selector:
        return create_function_selector_schema(function_selector)


def create_function_selectors_schema(function_selectors: List[FunctionSelector]):
    function_selector_list = []
    for function_selector in function_selectors:
        function_selector_list.append(
            create_function_selector_schema(function_selector))
    return function_selector_list


def create_function_selector_schema(function_selector: FunctionSelector):
    func_selector = function_selector.dict()

    if func_selector.get("args"):
        arg_list = json.loads(func_selector.get("args"))
        args = []
        for arg in arg_list:
            args.append(parse_obj_as(Arg, arg))
        func_selector["args"] = args

    return parse_obj_as(FunctionSelectorSchema, func_selector)
