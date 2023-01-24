import requests
import logging
from pymongo import errors
from web3 import Web3
from zlib import crc32
from pydantic import parse_obj_as
from typing import List, Dict
from models import Trx, Chain, TrxType

from .decode_trx_input import decode_trx_function_selector
from .get_trx_token import (
    get_trx_token,
    get_token_price,
    get_chain_native_token
)
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
    trxs = dict()
    for trx_type in TrxType:
        start_block = get_last_block_number(chain_id, address, trx_type.value)

        trx_url = trx_type.url

        type_trxs = get_user_chain_token_trxs(
            chain_id,
            address,
            trx_url,
            start_block
        )

        if type_trxs not in [None, []]:
            trxs[trx_type.value] = type_trxs

    if trxs in [None, {}]:
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
        users_trxs: Dict[str, List]
) -> List[Trx]:
    total_trxs = dict()
    created_trxs_tokens = dict()
    for trx_type, trxs in users_trxs.items():
        for trx in trxs:
            if trx_type == TrxType.NORMAL_TRX.value:
                trx_dict = create_trx(chain_id, address, trx)
                total_trxs[trx_dict.get("hash")] = trx_dict
                cache_last_block_number(
                    chain_id,
                    trx_dict.get("userAddress"),
                    trx_type,
                    trx_dict.get("blockNumber")
                )

            if trx_type == TrxType.TOKEN_TRX.value:
                if trx.get("hash") in total_trxs.keys():
                    existed_trx = total_trxs.get(trx.get("hash"))
                    token, created_trxs_tokens = create_trx_tokens(
                        chain_id, trx, created_trxs_tokens)

                    if token != None:
                        existed_trx["tokens"] = token
                        total_trxs[trx.get("hash")] = existed_trx

                else:
                    trx_dict = create_trx(
                        chain_id,
                        address,
                        trx
                    )
                    cache_last_block_number(
                        chain_id,
                        trx_dict.get("userAddress"),
                        trx_type,
                        trx_dict.get("blockNumber")
                    )
                    token, created_trxs_tokens = create_trx_tokens(
                        chain_id, trx, created_trxs_tokens)
                    if token:
                        trx_dict["tokens"] = token
                    total_trxs[trx_dict.get("hash")] = trx_dict

    return list(total_trxs.values())


def create_trx(
    chain_id: ChainId,
    address: Address,
    trx: Dict
):
    trx["userAddress"] = Web3.toChecksumAddress(address)
    if trx.get("contractAddress") not in ["0x", "", "0x0000000000000000000000000000000000000000", None]:
        trx["contractAddress"] = Web3.toChecksumAddress(
            trx.get("contractAddress"))
    try:

        input, labels = decode_trx_function_selector(
            chain_id,
            trx.get("hash"),
            trx.get("input"),
            trx.get("methodId"),
            trx.get("functionName")
        )
        trx["input"] = input
        trx["labels"] = labels
    except Exception as e:
        logging.exception(
            f"{e} -----------------> {trx.get('hash')} - {chain_id}")

    trx["chainId"] = chain_id
    trx["fromAddress"] = trx.get("from")
    trx["timeStamp"] = int(trx.get("timeStamp"))

    usd_price = get_usd_price(chain_id)
    if usd_price:
        trx["gas"] = calculate_gas(trx.get("gas"), usd_price)
        trx["gasUsed"] = calculate_gas(trx.get("gasUsed"), usd_price)
        trx["cumulativeGasUsed"] = calculate_gas(
            trx.get("cumulativeGasUsed"), usd_price)

    trx_obj = parse_obj_as(Trx, trx)
    return trx_obj.dict()


def create_trx_tokens(
    chain_id: ChainId,
    trx: Dict,
    created_trxs_tokens: Dict
):
    token = None

    if trx.get("contractAddress") not in ["0x", "", "0x0000000000000000000000000000000000000000", None]:
        trx["contractAddress"] = Web3.toChecksumAddress(
            trx.get("contractAddress"))

        if trx.get("hash") in created_trxs_tokens.keys():
            same_trxs_tokens = created_trxs_tokens.get(
                trx.get("hash"))
            token = create_trx_token(chain_id, trx)
            if token != None:
                same_trxs_tokens.extend(token)
                token = list(tuple(same_trxs_tokens))
                created_trxs_tokens[trx.get(
                    "hash")] = token
        else:
            token = create_trx_token(chain_id, trx)
            if token != None:
                created_trxs_tokens[trx.get("hash")] = token

    return token, created_trxs_tokens


def create_trx_token(
    chain_id: ChainId,
    trx: Dict
):
    if not trx.get("tokenName"):
        return None

    token = get_trx_token(
        chain_id,
        trx.get("contractAddress"),
        trx.get("userAddress"),
        trx.get("tokenName"),
        trx.get("tokenSymbol"),
        trx.get("tokenDecimal")
    )

    if trx.get("value") not in ["0", "", None]:
        native = get_chain_native_token(
            chain_id,
            trx.get("userAddress")
        )
        if None not in [native, token]:
            return [token, native]

    if token:
        return [token]

    return None


def get_usd_price(chain_id: ChainId):
    token_checksum = crc32(
        "-".join(["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE".lower(), str(chain_id)]).encode())
    return get_token_price(chain_id, token_checksum)


def calculate_gas(gas: str, price: str):
    return int(gas) * float(price) * 0.000000001


def insert_trxs(
    chain_id: ChainId,
    trxs: List[Dict]
):
    client = Trx.mongo_client(chain_id)

    for trx in trxs:
        try:
            client.insert_one(trx)
        except errors.DuplicateKeyError:
            continue
