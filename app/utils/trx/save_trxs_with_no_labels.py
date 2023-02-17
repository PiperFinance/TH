from pydantic import parse_obj_as
from pymongo import errors
from typing import List, Dict

from models import Chain, Trx, TrxWithNoLabels
from ..types import ChainId


def save_all_trxs_with_no_labels():
    chains = Chain.supported_chains()
    trxs = []
    for chain_id in chains:
        insert_trxs_with_no_labels(
            list(Trx.mongo_client(chain_id).find())
        )
    return trxs


def insert_trxs_with_no_labels(
    chain_id: ChainId,
    trxs: List[Dict]
):
    client = TrxWithNoLabels.mongo_client()
    for trx in trxs:
        if trx.get("input") and not trx.get("labels"):
            trx = parse_obj_as(
                {
                    "chainId": chain_id,
                    "hash": trx.get("hash"),
                    "chainIdHash": f'{chain_id}_{trx.get("hash")}'
                }
            )
            trx = trx.dict()
            try:
                client.insert_one(trx)
            except errors.DuplicateKeyError:
                continue
