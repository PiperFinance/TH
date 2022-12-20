from pydantic import parse_obj_as
from typing import List, Dict, Union

from models import Trx
from utils.types import Address, ChainId


def get_users_chain_token_trxs_len(
    chain_id: ChainId,
    addresses: Union[List[Address], Address],
) -> int:
    client = Trx.mongo_client(chain_id)
    if type(addresses) == list:
        addrs = []
        for address in addresses:
            addrs.append({"userAddress": address})
        query = {"$or": addrs}
    else:
        query = {"userAddress": addresses}

    return len(list(client.find(query)))


def get_users_chain_token_trxs(
    chain_id: ChainId,
    addresses: Union[List[Address], Address],
    skip: int = 0,
    limit: int = 0
) -> List[Trx]:

    client = Trx.mongo_client(chain_id)
    if type(addresses) == list:
        addrs = []
        for address in addresses:
            addrs.append({"userAddress": address})
        query = {"$or": addrs}
    else:
        query = {"userAddress": addresses}

    if limit < 1:
        trxs = list(client.find(query).sort("timeStamp", -1))

    if skip < 1:
        trxs = list(client.find(query).sort("timeStamp", -1).limit(limit))

    else:
        trxs = list(client.find(query).sort(
            "timeStamp", -1).skip(skip).limit(limit))

    return create_trx_objects(trxs)


def create_trx_objects(trxs: List[Dict]):
    trx_objs = []
    for trx in trxs:
        trx_objs.append(parse_obj_as(Trx, trx))
    return trx_objs
