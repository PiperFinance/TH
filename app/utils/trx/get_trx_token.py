import requests
import logging
import numpy as np
from web3 import exceptions
from pydantic import parse_obj_as

from models import Chain
from models.token import Token
from configs.constant_config import constants
from utils.abis import token_abi
from utils.types import ChainId, Address


def get_chain_native_token(chain_id, user_address) -> Token:
    native = Chain(chainId=chain_id).wNative
    return get_trx_token(
        chain_id,
        native.get("address"),
        user_address,
        native.get("name"),
        native.get("symbol"),
        native.get("decimals"),
    )


def get_trx_token(
    chain_id: ChainId,
    token_address: Address,
    user_address: Address,
    token_name: str,
    token_symbol: str,
    token_decimal: str,
):
    tokens = constants.tokens
    token_checksum = f"{token_address.lower()}-{str(chain_id)}"

    token = tokens.get(token_checksum)
    if not token:
        token = {
            "detail": {
                "chainId": chain_id,
                "address": token_address,
                "name": token_name,
                "symbol": token_symbol,
                "decimals": int(token_decimal),
            }
        }

    token = parse_obj_as(Token, token)

    # balance = get_token_balance(
    #     chain_id, token_address, user_address)
    # if balance:
    #     token.balance = str(balance)
    # price = get_token_price(chain_id, token_checksum)
    # if price:
    #     token.priceUSD = price
    #     token.value = calculate_token_value(float(price), balance)

    return token


def get_token_price(chain_id: ChainId, token_id: str):
    url = f"https://tp.piper.finance/?chainId={chain_id}&tokenId={token_id}"
    try:
        # res = requests.get(url)
        with requests.request("GET", url=url) as res:
            if res.text == "":
                return None
            res = np.format_float_positional(float(res.text), trim="-")
    except (
        requests.exceptions.JSONDecodeError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.SSLError,
        requests.exceptions.ReadTimeout,
    ):
        return None


def get_token_balance(chain_id: ChainId, token_address: Address, user_address: Address):
    try:
        w3 = Chain(chainId=chain_id).w3
        contract = w3.eth.contract(token_address.checked, abi=token_abi)
        balance = contract.functions.balanceOf(user_address).call()
        return balance
    except (exceptions.ContractLogicError, requests.exceptions.ReadTimeout):
        return None


def calculate_token_value(price: float, balance: int):
    return np.format_float_positional(price * balance, trim="-")
