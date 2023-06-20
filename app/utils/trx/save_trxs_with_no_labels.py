import logging
from sqlmodel import select
from pydantic import parse_obj_as
from pymongo import errors
from typing import List, Dict

from models import Chain, Trx, TrxWithNoLabels
from ..types import ChainId
from configs.postgres_config import InitializePostgres


def save_all_trxs_with_no_labels():
    trxs = get_all_trxs()
    if trxs in [None, []]:
        return
    insert_trxs_with_no_labels(trxs)


def get_all_trxs():
    ps = InitializePostgres()

    with ps.session as session:
        trxs = session.exec(select(Trx)).all()
    return trxs


def insert_trxs_with_no_labels(
    trxs: List[Dict]
):
    ps = InitializePostgres()
    for trx in trxs:
        with ps.session as session:
            if trx.input and not trx.labels:
                trx = parse_obj_as(
                    TrxWithNoLabels,
                    {
                        "chainId": trx.chainId,
                        "hash": trx.hash
                    }
                )
                try:
                    session.add(trx)
                    session.commit()
                except Exception as e:
                    logging.exception(e)
                    continue
