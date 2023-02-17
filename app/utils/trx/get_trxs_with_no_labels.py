import logging
from pydantic import parse_obj_as
from typing import List, Dict

from models import TrxWithNoLabels
from .get_trxs import create_trx_objects


def get_all_trxs_with_no_labels(
    skip: int = 0,
    limit: int = 0
):
    client = TrxWithNoLabels.mongo_client()
    try:
        trxs = list(client.find())
        trxs_len = len(trxs)
    except Exception as e:
        logging.exception(e)
        return None, None

    if limit < 1:
        trxs = trxs

    if skip < 1:
        try:
            trxs = list(client.find().limit(limit))
        except Exception as e:
            logging.exception(e)
            return None, None

    else:
        try:
            trxs = list(client.find().skip(skip).limit(limit))
        except Exception as e:
            logging.exception(e)
            return None, None

    if trxs in [None, []]:
        return None, 0

    trxs = create_trx_with_no_labels_objects(trxs)
    return trxs, trxs_len


def create_trx_with_no_labels_objects(trxs: List[Dict]):
    trx_objs = []
    for trx in trxs:
        trx_objs.append(parse_obj_as(TrxWithNoLabels, trx))
    return trx_objs
