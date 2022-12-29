from pydantic import parse_obj_as
from typing import List, Dict, Union

from models import Trx
from utils.types import Address, ChainId


def get_users_token_trxs_len(
    chain_ids: Union[List[ChainId], ChainId],
    addresses: Union[List[Address], Address]
):
    if type(chain_ids) != list:
        chain_ids = [chain_ids]
    trx_len = 0
    for chain_id in chain_ids:
        trx_len += get_users_chain_token_trxs_len(chain_id, addresses)
    return trx_len


def get_users_token_trxs(
    chain_ids: Union[List[ChainId], ChainId],
    addresses: Union[List[Address], Address],
    skip: int = 0,
    limit: int = 0
) -> List[Trx]:
    if type(chain_ids) != list:
        chain_ids = [chain_ids]
    trxs = []
    for chain_id in chain_ids:
        chain_trxs = get_users_chain_token_trxs(
            chain_id, addresses, skip, limit)
        if chain_trxs not in [None, []]:
            trxs.extend(chain_trxs)
    return trxs


def get_users_chain_token_trxs_len(
    chain_id: ChainId,
    addresses: Union[List[Address], Address]
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
