import requests
import logging
from web3 import Web3
from pydantic import parse_obj_as
from typing import List, Dict
from models import Trx, Chain
from .decode_trx_input import decode_trx_input_data
from utils.sync_redis import cache_last_block_number, get_last_block_number
from utils.types import Address, ChainId


def save_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address
):
    start_block = get_last_block_number(chain_id, address)

    trxs = get_user_chain_token_trxs(
        chain_id,
        address,
        start_block
    )
    if trxs in [None, []]:
        return

    trxs = create_trxs(
        chain_id,
        address,
        trxs
    )
    insert_trxs(
        chain_id,
        trxs
    )


def get_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address,
    start_block: int = 0
) -> List[Dict]:

    chain = Chain(chainId=chain_id)
    url = chain.url
    api_keys = chain.api_keys

    data = {
        "address": address,
        "startblock": start_block,
        "endblock": 99999999,
        "sort": "asc"
    }

    for api_key in api_keys:
        try:
            url = f"{url}?module=account&action=tokentx&apikey={api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and (res.get("message") == "OK" or res.get("message") == "No transactions found"):
                return res.get("result")
        except Exception as e:
            logging.exception(f"{e} -> API Key didn't work.")
            continue


def create_trxs(
        chain_id: ChainId,
        address: Address,
        users_trxs: List[Dict]
) -> List[Trx]:
    trxs = []

    for trx in users_trxs:
        trx["userAddress"] = Web3.toChecksumAddress(address)
        labels = decode_trx_input_data(trx.get("input"))
        if labels:
            trx["labels"] = labels
        trx["chainId"] = chain_id
        trx["fromAddress"] = trx.get("from")
        trx["timeStamp"] = int(trx.get("timeStamp"))
        trx_obj = parse_obj_as(Trx, trx)
        trxs.append(trx_obj.dict())

    return trxs


def insert_trxs(
    chain_id: ChainId,
    trxs: List[Dict]
):
    client = Trx.mongo_client(chain_id)

    for trx in trxs:
        try:
            client.insert_one(trx)
            cache_last_block_number(
                chain_id,
                trx.get("userAddress"),
                trx.get("blockNumber")
            )
        except Exception as e:
            logging.exception(e)
            continue
