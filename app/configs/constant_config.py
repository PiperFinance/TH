import json
import requests
import os
from pydantic import BaseConfig
from typing import Dict, Generator, List
from pathlib import Path

from utils.types import ChainId, ApiKey

# _chains = requests.get(
#     "https://raw.githubusercontent.com/PiperFinance/CD/main/chains/mainnet.json")

with requests.request(
    "GET",
    url="https://raw.githubusercontent.com/PiperFinance/CD/main/chains/mainnet.json",
) as _chains:
    _chains = _chains.json()

chains = {}

for chain in _chains:
    chains[chain.get("id")] = chain


# _tokens = requests.get(
#     "https://raw.githubusercontent.com/PiperFinance/CD/main/tokens/outVerified/all_tokens.json")

with requests.request(
    "GET",
    url="https://raw.githubusercontent.com/PiperFinance/CD/main/tokens/outVerified/all_tokens.json",
) as _tokens:
    _tokens = _tokens.json()

tokens = {}

for token_checksum, token in _tokens.items():
    tokens[token_checksum] = token


api_key_path = os.getenv("API_LIST") or f"{Path(os.getcwd())}/data/api_keys.json"

with open(api_key_path) as f:
    _api_keys = json.load(f)

api_keys = {}

for chain_id, api_key_list in _api_keys.items():
    api_keys[int(chain_id)] = api_key_list

function_selector_path = f"{Path(os.getcwd())}/function_selectors.json"

with open(function_selector_path) as f:
    _function_selectors = json.load(f)

function_selectors = list(_function_selectors)


class Constants(BaseConfig):
    chains: Dict[ChainId, Dict] = chains
    tokens: Dict[str, Dict] = tokens
    api_keys: Dict[ChainId, List] = api_keys
    function_selectors: List[Dict] = function_selectors

    def api_key_generator(self, chain_id) -> Generator[ApiKey, None, None]:
        i = 0
        while keys := self.api_keys[chain_id]:
            yield ApiKey(keys[i])
            i += 1
            if i > len(keys):
                i = 0


constants = Constants()
