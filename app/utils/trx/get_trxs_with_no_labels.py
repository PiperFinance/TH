import logging
from pydantic import parse_obj_as
from typing import List, Dict
from sqlmodel import select

from models import TrxWithNoLabels, FunctionSelector
# from .get_trxs import create_trx_objects
from configs.postgres_config import InitializePostgres


def get_all_trxs_with_no_labels(
    skip: int = 0,
    limit: int = 0
):
    ps = InitializePostgres()
    with ps.session as session:
        statement = select(FunctionSelector)
        results = session.exec(statement)
        trxs = results.all()
        trxs_len = len(trxs)

    if limit >= 1 and skip >= 1:
        trxs = trxs[skip:skip + limit]

    elif skip < 1 and limit >= 1:
        with ps.session as session:
            statement = select(FunctionSelector).limit(limit)
            results = session.exec(statement)
            trxs = results.all()

    return trxs, trxs_len
