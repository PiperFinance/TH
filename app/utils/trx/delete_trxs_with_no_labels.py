import logging
from pymongo import errors
from typing import List, Dict
from sqlmodel import select

from models import TrxWithNoLabels
from configs.postgres_config import InitializePostgres


def delete_trxs(
    hashes: List[str]
):
    ps = InitializePostgres()

    for hash in hashes:
        with ps.session() as session:
            try:
                statement = select(TrxWithNoLabels).where(
                    TrxWithNoLabels.hash == hash)
                results = session.exec(statement)
                trx = results.first()
                session.delete(trx)
            except Exception as e:
                logging.exception(e)
                continue
