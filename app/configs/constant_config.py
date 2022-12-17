import json
import requests
import os
from pydantic import BaseConfig
from typing import Dict, List
from pathlib import Path

from utils.types import ChainId

api_key_path = os.getenv("API_LIST") or f"{Path(os.getcwd())}/api_keys.json"

_chains = requests.get(
    "https://raw.githubusercontent.com/PiperFinance/CD/main/chains/mainnet.json")
_chains = _chains.json()

chains = {}

for chain in _chains:
    chains[chain.get("id")] = chain


with open(api_key_path) as f:
    _api_keys = json.load(f)

api_keys = {}

for chain_id, api_key_list in _api_keys.items():
    api_keys[int(chain_id)] = api_key_list


class Constants(BaseConfig):
    chains: Dict[ChainId, Dict] = chains
    api_keys: Dict[ChainId, List] = api_keys


constants = Constants()
