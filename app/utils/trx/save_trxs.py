import asyncio
import httpx
import requests
import logging
from pymongo import errors
from web3 import Web3, exceptions
from pydantic import parse_obj_as
from typing import List, Dict, Optional

from models import Trx, Chain, TrxType, token
from .decode_trx_input import decode_trx_function_selector
from .get_trx_token import get_trx_token, get_token_price, get_chain_native_token
from utils.sync_redis import cache_last_block_number, get_last_block_number
from utils.types import Address, ChainId, Hash32


async def save_users_token_trxs(
    chain_ids: List[ChainId],
    addresses: List[Address],
    scan_iterations: int,
):
    calls = []
    for chain_id in chain_ids:
        calls.append(save_users_chain_token_trxs(chain_id, addresses, scan_iterations))
    await asyncio.gather(
        *calls,
        return_exceptions=True,
    )


async def save_users_chain_token_trxs(
    chain_id: ChainId,
    addresses: List[Address],
    scan_iterations: int,
):
    await asyncio.gather(
        *[
            save_user_chain_token_trxs(chain_id, address, scan_iterations)
            for address in addresses
        ],
        return_exceptions=True,
    )


async def save_user_chain_token_trxs(
    chain_id: ChainId,
    address: Address,
    scan_iterations: int,
):
    trxs: Dict[TrxType, List[Dict]] = dict()
    for trx_type in TrxType:
        start_block = get_last_block_number(chain_id, address, trx_type) or 0
        type_trxs = await get_user_chain_token_trxs(
            chain_id, address, trx_type.url, start_block
        )
        if type_trxs:
            trxs[trx_type] = type_trxs

    if len(trxs) == 0:
        return

    trxs_list = create_trxs(chain_id, address, trxs)
    insert_trxs(chain_id, trxs_list)


async def get_user_chain_token_trxs(
    chain_id: ChainId, address: Address, trx_url: str, start_block: int = 0
) -> List[Dict] | None:

    if start_block in [None, 0]:
        start_block = 0

        trx_count = await get_user_chain_trx_count(chain_id, address)
        if trx_count == 0:
            return None
        if trx_count is not None:
            return await return_token_trxs(
                chain_id, address, trx_url, start_block, trx_count
            )
    return await return_token_trxs(chain_id, address, trx_url, start_block)


async def return_token_trxs(
    chain_id: ChainId,
    address: Address,
    trx_url: str,
    start_block: int,
    trx_count: int | None = None,
):
    if trx_count == 0:
        return None

    if trx_count == None:
        result = await get_token_trxs(chain_id, address, trx_url, start_block, False)
        if len(result) <= 10000:
            return result
    return await get_token_trxs(chain_id, address, trx_url, start_block, True)


async def get_user_chain_trx_count(chain_id: ChainId, address: Address):
    chain = Chain(chainId=chain_id)

    url = f"{chain.url}?module=proxy&action=eth_getTransactionCount&address={address}&tag=latest&apikey={chain.next_api_key}"  # noqa: E501
    async with httpx.AsyncClient() as cl:
        res = await cl.get(url=url)
        if res.status_code == 200:
            res = res.json()
            if res.get("error") is not None or res.get("status") == 0:
                return None
        return None


async def get_token_trxs(
    chain_id: ChainId,
    address: Address,
    trx_url: str,
    start_block: int,
    chunk: bool = False,
) -> List:
    result = []
    async with httpx.AsyncClient(http2=True) as cl:
        if not chunk or (start_block + 10000) > 99999999:
            await get_token_trxs_from_scanner(
                cl, chain_id, address, trx_url, start_block, 99999999, result=result
            )
        else:
            calls = []
            for block_number in range(start_block, 99999999, 10000):
                calls.append(
                    get_token_trxs_from_scanner(
                        cl,
                        chain_id,
                        address,
                        trx_url,
                        start_block,
                        block_number,
                        result=result,
                    )
                )
            asyncio.gather(
                *calls,
                return_exceptions=True,
            )
    return result


async def get_token_trxs_from_scanner(
    cl: httpx.AsyncClient,
    chain_id: ChainId,
    address: Address,
    trx_url: str,
    start_block: int = 0,
    end_block: int = 99999999,
    result: List | None = None,
):
    if result is None:
        raise RuntimeError("Need result")

    chain = Chain(chainId=chain_id)
    data = f"&address={address}&startblock={start_block}&endblock={end_block}&sort=asc"
    url = f"{chain.url}{trx_url}{data}&apikey={chain.next_api_key}"
    res = await cl.get(url=url, timeout=chain.req_timeout)
    if res.status_code == 200:
        res = res.json()
        if res.get("message") == "OK" or res.get("message") == "No transactions found":
            result.extend(res.get("result"))


def create_trxs(
    chain_id: ChainId, address: Address, users_trxs: Dict[TrxType, List[Dict]]
) -> List[Trx]:
    # usd_price = get_usd_price(chain_id)
    chain = Chain(chainId=chain_id)
    total_trxs: Dict[str, Trx] = dict()
    current_block_no = chain.w3.eth.block_number
    for trx_type, trxs in users_trxs.items():
        cache_last_block_number(
            chain_id,
            address,
            trx_type,
            current_block_no,
        )
        for trx in trxs:
            if trx_type == TrxType.NORMAL_TRX:
                trx_obj = parse_trx(chain_id, address, trx)
                if trx_obj:
                    total_trxs[trx_obj.hash] = trx_obj

            if trx_type == TrxType.TOKEN_TRX:
                trx_obj = total_trxs.get(trx["hash"])
                if trx_obj is None:
                    trx_obj = parse_trx(chain_id, address, trx)
                    if trx_obj is None:
                        continue
                    total_trxs[trx_obj.hash] = trx_obj
                check_trx_tokens(chain_id, address, trx, trx_obj)

    return list(total_trxs.values())


def parse_trx(
    chain_id: ChainId, address: Address, trx: Dict, usd_price: str | None = None
) -> Trx | None:
    trx["userAddress"] = Web3.toChecksumAddress(address)
    trx["fromAddress"] = trx.get("from")
    trx["chainId"] = chain_id
    if trx["contractAddress"] not in [
        "0x",
        "",
        "0x0000000000000000000000000000000000000000",
        None,
    ]:
        trx["contractAddress"] = Web3.toChecksumAddress(trx.get("contractAddress"))
    else:
        if int(trx["value"]) > 0:
            trx["fromAddress"] = "0x0000000000000000000000000000000000000000"
            return parse_obj_as(Trx, trx)
    try:
        input, _type = get_trx_input_and_type_from_web3(
            chain_id, trx["hash"], trx["input"]
        )
        if _type is None or input is None:
            return parse_obj_as(Trx, trx)
        else:
            trx["input"] = input
            trx["type"] = _type
        if "methodId" in trx and "functionName" in trx:
            labels = decode_trx_function_selector(
                input, trx["methodId"], trx["functionName"]
            )
            trx["labels"] = labels
    except exceptions.TransactionNotFound as e:
        logging.warning(e)
        return None
    except Exception as e:
        logging.exception(f"{e} -----------------> {trx.get('hash')} - {chain_id}")

    trx["chainId"] = chain_id
    trx["timeStamp"] = int(trx.get("timeStamp", "0"))

    if usd_price:
        trx["gas"] = calculate_gas(trx.get("gas", "0"), usd_price)
        trx["gasUsed"] = calculate_gas(trx.get("gasUsed", "0"), usd_price)
        trx["cumulativeGasUsed"] = calculate_gas(
            trx.get("cumulativeGasUsed", "0"), usd_price
        )

    return parse_obj_as(Trx, trx)


def get_trx_input_and_type_from_web3(
    chain_id: ChainId, hash: str, input: str | None = None
):
    if input == "deprecated":
        raise exceptions.TransactionNotFound

    try:
        w3 = Chain(chainId=chain_id).w3
        web3_trx = w3.eth.get_transaction(hash)  # type: ignore
        if web3_trx:
            if input in [None, "0x", "deprecated", ""]:
                input = web3_trx.get("input")
            if web3_trx.get("type"):
                type = int(str(web3_trx["type"]), 16)
                return input, type
            return input, None
    except (requests.exceptions.HTTPError) as e:
        logging.warning(e)
    return input, None


def check_trx_tokens(
    chain_id: ChainId, user_address: Address, trx_dict: Dict, trx: Trx
):
    if trx_dict.get("contractAddress") not in [
        "0x",
        "",
        "0x0000000000000000000000000000000000000000",
        None,
    ]:
        trx_dict["contractAddress"] = Web3.toChecksumAddress(
            trx_dict.get("contractAddress")
        )
        tokens = create_trx_token(chain_id, user_address, trx_dict)
        if tokens is None:
            return
        if trx.tokens is None:
            trx.tokens = tokens
        else:
            trx.tokens.extend(tokens)


def create_trx_token(
    chain_id: ChainId, user_address: Address, trx: Dict
) -> List[token.Token] | None:
    if not trx.get("tokenName"):
        return None

    token = get_trx_token(
        chain_id,
        trx["contractAddress"],
        user_address,
        trx["tokenName"],
        trx["tokenSymbol"],
        trx["tokenDecimal"],
    )

    if trx.get("value") not in ["0", "", None]:
        native = get_chain_native_token(chain_id, user_address)
        if None not in [native, token]:
            return [token, native]

    if token is not None:
        return [token]

    return None


def get_usd_price(chain_id: ChainId):
    return get_token_price(
        chain_id, f"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee-{chain_id}"
    )


def calculate_gas(gas: str, price: str):
    return int(gas) * float(price) * 0.000000001


def make_token_dict(tokens: List[token.Token]):
    token_dict_list = []
    for token in tokens:
        token_dict_list.append(token.dict())

    return token_dict_list


def insert_trxs(chain_id: ChainId, trxs: List[Trx]):
    client = Trx.mongo_client(chain_id)
    client.insert_many([_.dict() for _ in trxs])
    # for trx in trxs:
    #     try:
    #         client.insert_one(trx)
    #     except errors.DuplicateKeyError:
    #         continue
