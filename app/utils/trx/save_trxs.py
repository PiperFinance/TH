import requests
import logging
from pymongo import errors
from web3 import Web3
from zlib import crc32
from pydantic import parse_obj_as
from typing import List, Dict
from models import Trx, Chain, TrxType
from .decode_trx_input import decode_trx_input_data
from .get_trx_token import get_trx_token, get_token_price
from utils.sync_redis import (
    cache_last_block_number,
    get_last_block_number
)
from utils.types import Address, ChainId


def save_users_token_trxs(
    chain_ids: List[ChainId],
    addresses: List[Address]
):
    for chain_id in chain_ids:
        save_users_chain_token_trxs(chain_id, addresses)


def save_users_chain_token_trxs(
    chain_id: ChainId,
    addresses: List[Address]
):
    for address in addresses:
        save_user_chain_token_trxs(chain_id, address)


def save_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address
):
    for trx_type in TrxType:
        start_block = 0
        # start_block = get_last_block_number(chain_id, address, trx_type.value)

        trx_url = trx_type.url

        trxs = get_user_chain_token_trxs(
            chain_id,
            address,
            trx_url,
            start_block
        )
        if trxs in [None, []]:
            return

        trxs = create_trxs(
            chain_id,
            address,
            trxs,
            trx_type.value
        )
        insert_trxs(
            chain_id,
            trxs,
            trx_type.value
        )


def get_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address,
    trx_url: str,
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
            url = f"{url}{trx_url}{api_key}"
            res = requests.post(url=url, data=data)
            res = res.json()
            if res is not None and (res.get("message") == "OK" or res.get("message") == "No transactions found"):
                return res.get("result")
        except (requests.exceptions.JSONDecodeError, requests.exceptions.SSLError):
            continue


def create_trxs(
        chain_id: ChainId,
        address: Address,
        users_trxs: List[Dict],
        trx_type: str
) -> List[Trx]:
    trxs = dict()
    created_trxs_tokens = dict()
    for trx in users_trxs:
        trx["userAddress"] = Web3.toChecksumAddress(address)
        if trx.get("contractAddress") not in ["0x", "", "0x0000000000000000000000000000000000000000", None]:
            trx["contractAddress"] = Web3.toChecksumAddress(
                trx.get("contractAddress"))
            if trx_type == TrxType.TOKEN_TRX.value:
                if trx.get("hash") in created_trxs_tokens.keys():
                    same_trxs_tokens = created_trxs_tokens.get(trx.get("hash"))
                    token = create_trx_token(chain_id, trx)
                    if token != None:
                        same_trxs_tokens.append(token)
                        created_trxs_tokens[trx.get("hash")] = same_trxs_tokens
                    trx["tokens"] = same_trxs_tokens
                    logging.info(
                        f"trx: {trx.get('hash')} in chain: {chain_id} has more than one token.")
                    logging.info(same_trxs_tokens)
                else:
                    token = create_trx_token(chain_id, trx)
                    if token != None:
                        created_trxs_tokens[trx.get("hash")] = [token]
                        trx["tokens"] = [token]

        input, labels = decode_trx_input_data(
            chain_id,
            trx.get("hash"),
            trx.get("input")
        )
        if input:
            trx["labels"] = labels
            trx["input"] = input

        # usd_price = get_usd_price(chain_id)
        # if usd_price:
        #     trx["gas"] = calculate_gas(trx.get("gas"), usd_price)
        #     trx["gasUsed"] = calculate_gas(trx.get("gasUsed"), usd_price)
        #     trx["cumulativeGasUsed"] = calculate_gas(
        #         trx.get("cumulativeGasUsed"), usd_price)

        trx["chainId"] = chain_id
        trx["fromAddress"] = trx.get("from")
        trx["timeStamp"] = int(trx.get("timeStamp"))
        trx_obj = parse_obj_as(Trx, trx)
        trxs[trx_obj.hash] = trx_obj.dict()
        if trx_obj.tokens and len(trx_obj.tokens) > 1:
            logging.info("multi tokens saved")

    return list(trxs.values())


def create_trx_token(
    chain_id: ChainId,
    trx: Dict,
):
    token = get_trx_token(
        chain_id,
        trx.get("contractAddress"),
        trx.get("userAddress"),
        trx.get("tokenName"),
        trx.get("tokenSymbol"),
        trx.get("tokenDecimal")
    )
    return token


def get_usd_price(chain_id: ChainId):
    token_checksum = crc32(
        "-".join(["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE".lower(), str(chain_id)]).encode())
    return get_token_price(chain_id, token_checksum)


def calculate_gas(gas: str, price: str):
    return int(gas) * float(price) * 0.000000001


def insert_trxs(
    chain_id: ChainId,
    trxs: List[Dict],
    trx_type: str
):
    client = Trx.mongo_client(chain_id)

    for trx in trxs:
        if trx.get("tokens") and len(trx.get("tokens")) > 1:
            logging.info(f"Mongo --> Trx: {trx.get('hash')} in chain: {chain_id} has more than one token")
            logging.info(trx.get("tokens"))
        try:
            client.insert_one(trx)
            cache_last_block_number(
                chain_id,
                trx.get("userAddress"),
                trx_type,
                trx.get("blockNumber")
            )
        except errors.DuplicateKeyError:
            continue
