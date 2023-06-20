import json
import logging
from pydantic import parse_obj_as
from typing import List, Dict, Union
from sqlmodel import select

from models import Trx, Token, Label
from utils.types import Address, ChainId
from configs.postgres_config import InitializePostgres
from schemas.response_schema import TrxSchema


def get_users_token_trxs_len(
    chain_ids: Union[List[ChainId], ChainId],
    addresses: Union[List[Address], Address]
):
    if type(chain_ids) == list:
        if type(addresses) == list:
            statement = select(Trx).where(
                Trx.chainId in chain_ids,
                Trx.userAddress in addresses)
        else:
            statement = select(Trx).where(
                Trx.chainId in chain_ids,
                Trx.userAddress == addresses)
    else:
        if type(addresses) == list:
            statement = select(Trx).where(
                Trx.chainId == chain_ids,
                Trx.userAddress in addresses)
        else:
            statement = select(Trx).where(
                Trx.chainId == chain_ids,
                Trx.userAddress == addresses)

    ps = InitializePostgres()
    with ps.session() as session:
        results = session.exec(statement)
        trxs_len = len(results.all())

    return trxs_len


def get_users_token_trxs(
    chain_ids: Union[List[ChainId], ChainId],
    addresses: Union[List[Address], Address],
    skip: int = 0,
    limit: int = 0
) -> List[Trx]:

    if type(addresses) == list:
        if type(chain_ids) == list:
            _statement = select(Trx).where(
                Trx.chainId.in_(chain_ids),
                Trx.userAddress.in_(addresses))
        else:
            _statement = select(Trx).where(
                Trx.chainId == chain_ids,
                Trx.userAddress.in_(addresses))
    else:
        if type(chain_ids) == list:
            _statement = select(Trx).where(
                Trx.chainId.in_(chain_ids),
                Trx.userAddress == addresses)
        else:
            _statement = select(Trx).where(
                Trx.chainId == chain_ids,
                Trx.userAddress == addresses)

    ps = InitializePostgres()
    with ps.session as session:

        if limit >= 1 and skip >= 1:
            statement = _statement.order_by(Trx.timeStamp.desc())
            results = session.exec(statement)
            trxs = results.all()[skip:skip + limit]

        elif limit >= 1 and skip < 1:
            statement = _statement.limit(limit).order_by(Trx.timeStamp.desc())
            results = session.exec(statement)
            trxs = results.all()

        else:
            statement = _statement.order_by(Trx.timeStamp.desc())
            results = session.exec(statement)
            trxs = results.all()

    return create_trxs_schema(trxs)


def create_trxs_schema(trxs: List[Trx]):
    trx_list = []

    for trx in trxs:
        trx = trx.dict()
        if trx.get("tokens"):
            token_list = json.loads(trx.get("tokens"))
            tokens = []
            for token in token_list:
                tokens.append(parse_obj_as(Token, token))
            trx["tokens"] = tokens

        if trx.get("labels"):
            label_list = json.loads(trx.get("labels"))
            labels = []
            for label in label_list:
                labels.append(parse_obj_as(Label, label))
            trx["labels"] = labels

        trx_list.append(parse_obj_as(TrxSchema, trx))

    return trx_list
