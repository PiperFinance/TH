import requests
import logging
import numpy as np
from web3 import exceptions
from zlib import crc32
from pydantic import parse_obj_as

from models import Chain
from models.token import Token
from configs.constant_config import constants
from utils.abis import token_abi
from utils.types import ChainId, Address


def get_trx_token(
    chain_id: ChainId,
    token_address: Address,
    user_address: Address
):
    tokens = constants.tokens
    token_checksum = crc32(
        "-".join([token_address.lower(), str(chain_id)]).encode())
    # logging.info(
    #     f"----------------------------------> {token_address}: {token_checksum}")

    token = tokens.get(token_checksum)
    if not token:
        return None

    token = parse_obj_as(Token, token)
    # balance = get_token_balance(
    #     chain_id, token_address, user_address)
    # if balance:
    #     token.balance = str(balance)
    # price = get_token_price(chain_id, token_checksum)
    # if price:
    #     token.priceUSD = price
    #     token.value = calculate_token_value(float(price), balance)

    return token.dict()


def get_token_price(chain_id: ChainId, token_id: int):
    url = f"https://tp.piper.finance/?chainId={chain_id}&tokenId={token_id}"
    try:
        res = requests.get(url)
        logging.info(f"--------------------------------->{res.text}")

        if res.text == '':
            return None
        res = np.format_float_positional(float(res.text), trim='-')
    except requests.exceptions.ConnectionError:
        return None


def get_token_balance(
    chain_id: ChainId,
    token_address: Address,
    user_address: Address
):
    try:
        w3 = Chain(chainId=chain_id).w3
        contract = w3.eth.contract(token_address, abi=token_abi)
        balance = contract.functions.balanceOf(user_address).call()
        return balance
    except exceptions.ContractLogicError:
        return None


def calculate_token_value(price: float, balance: int):
    return np.format_float_positional(price * balance, trim='-')
