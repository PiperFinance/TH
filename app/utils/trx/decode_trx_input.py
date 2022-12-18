from typing import List
from pydantic import parse_obj_as

from models import Label
from .get_function_selectors import get_function_selector


def decode_trx_input_data(input: str) -> List[Label]:
    if input == "deprecated":
        return None

    labels = []

    func_sig_with_args = get_function_selector(input[:10])

    if func_sig_with_args:
        labels.append(Label(**{
            "title": func_sig_with_args.hex,
            "value": func_sig_with_args.text
        }))

        starter = 10

        for arg, arg_type in func_sig_with_args.args:

            labels.append(parse_obj_as(
                Label,
                {
                    "title": arg,
                    "value": arg_type.parse(input[starter: (starter + 64)])
                }))
            starter += 64

        return labels

    return None
