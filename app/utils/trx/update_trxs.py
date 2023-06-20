import logging
from typing import List
from sqlmodel import select

from models import Trx, Label
from .save_trxs import get_trx_input_and_type_from_web3
from .decode_trx_input import decode_trx_function_selector
from .get_trxs import get_users_token_trxs
from utils.types import Address, ChainId
from configs.postgres_config import InitializePostgres

def update_users_token_trxs(
    chain_ids: List[ChainId],
    addresses: List[Address]
):

    trxs = get_users_token_trxs(chain_ids, addresses)
    if trxs in [[], None]:
        return

    update_trxs(trxs)


def update_trxs(
    trxs: List[Trx]
):
    for trx in trxs:
        try:
            if not trx.labels:
                input, type = get_trx_input_and_type_from_web3(
                    trx.chainId,
                    trx.hash,
                    trx.input
                )
                labels = decode_trx_function_selector(
                    trx.input,
                    None,
                    None
                )

                update_trx(
                    trx.hash,
                    input,
                    type,
                    labels
                )
        except Exception as e:
            logging.exception(e)
            continue

def update_trx(
    hash: str,
    input: str = None,
    type: int = None,
    labels: List[Label] = None
):
    if not input and not type and not labels:
        return

    ps = InitializePostgres()
    with ps.session as session:
        try:
            statement = select(Trx).where(Trx.hash == hash)
            results = session.exec(statement)
            trx = results.one()

            if input:
                trx.input = input

            if type:
                trx.type = type

            if labels:
                trx.labels = labels

            session.add(trx)
            session.commit()
            session.refresh(trx)

        except Exception as e:
            logging.exception(e)
