import logging
import requests
from web3 import exceptions
from typing import List, Tuple, Union
from pydantic import parse_obj_as

from models import Label, Chain, ArgType
from .save_function_selectors import save_function_selector
from .get_function_selectors import get_function_selector
from utils.types import ChainId
from schemas.request_schemas import FunctionSelectorSchema


def decode_trx_function_selector(
    input: str = None,
    method_id: str = None,
    function_name: str = None
):
    if input not in ["deprecated", "0x", "", None]:
        function_selector, labels = get_and_create_function_selector(input)
        if function_selector:
            if function_selector.args:
                labels = create_function_selector_args(
                    input,
                    labels,
                    function_selector.args
                )

        else:
            if function_name not in ["", None] and method_id not in ["0x", None]:
                labels, args = save_and_create_function_selector(
                    method_id,
                    function_name
                )

                if args != []:
                    labels = create_function_selector_args(
                        input,
                        labels,
                        args
                    )

    elif function_name not in ["", None] and method_id not in ["0x", None]:
        labels = save_and_create_function_selector(
            method_id, function_name)
    else:
        return None
    return labels


def get_and_create_function_selector(
    input: str
):
    function_selector = get_function_selector(input[:10])

    if function_selector:
        labels = [Label(**{
            "title": "function",
            "value": function_selector.text
        })]
    else:
        labels = None

    return function_selector, labels


def save_and_create_function_selector(
    method_id: str,
    function_name: str
):
    function = function_name.split("(")[0]

    labels = [parse_obj_as(Label, {
        "title": "function",
        "value": function
    })]

    function_selector = {
        "hex": method_id,
        "text": function,
    }

    args = []
    _args = function_name.split("(")[1]
    _args = _args.split(")")[0]
    if _args != '':
        for i, val in enumerate(_args.split(",")):
            try:
                if i < 1:
                    if len(val.split(" ")) >= 2:
                        args.append(
                            [
                                val.split(" ")[1],
                                ArgType.convert(
                                    val.split(" ")[0])
                            ]
                        )
                    else:
                        args.append(
                            [
                                " ",
                                ArgType.convert(val)
                            ]
                        )
                else:
                    if val[0] != " ":
                        if len(val.split(" ")) >= 2:
                            args.append(
                                [
                                    val.split(" ")[1],
                                    ArgType.convert(
                                        val.split(" ")[0])
                                ]
                            )
                        else:
                            args.append(
                                [
                                    " ",
                                    ArgType.convert(
                                        val.split(" ")[0])
                                ]
                            )
                    else:
                        if len(val.split(" ")) > 2:
                            args.append(
                                [
                                    val.split(" ")[2],
                                    ArgType.convert(
                                        val.split(" ")[1])
                                ]
                            )
                        else:
                            args.append(
                                [
                                    " ",
                                    ArgType.convert(
                                        val.split(" ")[1])
                                ]
                            )
            except Exception as e:
                logging.exception(f"{e} -----------> {val}")
        if args != []:
            function_selector["args"] = args

        function_selector = parse_obj_as(
            FunctionSelectorSchema, function_selector)
        save_function_selector(function_selector)

    return labels, args


def create_function_selector_args(
    input: str,
    labels: List[Label],
    args: List[Union[Tuple, List]]
):
    starter = 10

    for arg, arg_type in args:
        try:
            value = parse_obj_as(ArgType, arg_type)
            labels.append(parse_obj_as(
                Label,
                {
                    "title": arg,
                    "value": value.parse(input[starter: (starter + 64)])
                }))
            starter += 64
        except Exception as e:
            logging.exception(e)

    return labels
