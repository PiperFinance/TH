import logging
from typing import List
from pydantic import parse_obj_as

from models import Label, Chain
from .get_function_selectors import get_function_selector
from utils.types import ChainId


def decode_trx_input_data(
    chain_id: ChainId,
    hash: str,
    input: str
) -> List[Label]:
    if input == "deprecated":
        input = get_trx_input_from_web3(chain_id, hash)
        if input == None:
            return None, None

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

        return input, labels

    return None, None


def get_trx_input_from_web3(
    chain_id: ChainId,
    hash: str
):
    try:
        w3 = Chain(chainId=chain_id).w3
        web3_trx = w3.eth.get_transaction(hash)
        if web3_trx:
            return web3_trx.get("input")
    except Exception as e:
        logging.exception(e)
        return None
