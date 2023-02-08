import logging
from typing import List

from models import Trx, Label
from .decode_trx_input import decode_trx_function_selector
from .get_trxs import get_users_token_trxs, get_users_chain_token_trxs
from utils.types import Address, ChainId


def update_users_token_trxs(
    chain_ids: List[ChainId],
    addresses: List[Address]
):

    trxs = get_users_token_trxs(chain_ids, addresses)
    if trxs in [[], None]:
        return

    update_trxs(trxs)


def update_users_chain_token_trxs(
    chain_id: ChainId,
    addresses: List[Address]
):

    trxs = get_users_chain_token_trxs(chain_id, addresses)
    if trxs in [[], None]:
        return

    update_trxs(trxs)


def update_trxs(
    trxs: List[Trx]
):
    for trx in trxs:
        try:
            if not trx.labels:
                input, labels = decode_trx_function_selector(
                    trx.input,
                    None,
                    None
                )

                update_trx(
                    trx.chainId,
                    trx.hash,
                    input,
                    labels
                )
        except Exception as e:
            logging.exception(e)
            continue


def update_trx(
    chain_id: ChainId,
    hash: str,
    input: str = None,
    labels: List[Label] = None
):
    try:
        values = dict()

        if input:
            values["input"] = input

        if labels:
            label_list = []
            for label in labels:
                label_list.append(label.dict())
            values["labels"] = label_list

        if len(values) < 1:
            return

        client = Trx.mongo_client(chain_id)
        query = {"hash": hash}
        newvalues = {"$set": values}

        client.update_one(query, newvalues)
    except Exception as e:
        logging.exception(e)
