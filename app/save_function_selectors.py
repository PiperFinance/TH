import logging
from pydantic import parse_obj_as

from configs.constant_config import constants
from schemas.request_schemas import FunctionSelectorSchema
from utils.trx.save_function_selectors import save_function_selectors


def save_first_function_selectors():
    try:
        _function_selectors = constants.function_selectors
        function_selectors = []
        for function_selector in _function_selectors:
            try:
                function_selectors.append(parse_obj_as(
                    FunctionSelectorSchema, function_selector))
            except Exception as e:
                logging.exception(e)
                continue
        save_function_selectors(function_selectors)
    except Exception as e:
        logging.exception(e)
