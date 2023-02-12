from pymongo import errors
from typing import List, Dict

from models import TrxWithNoLabels


def delete_trxs(
    trxs: List[Dict]
):
    client = TrxWithNoLabels.mongo_client()
    for trx in trxs:
        try:
            query = {"chainIdHash": f'{trx.get("chainId")}_{trx.get("hash")}'}
            client.delete_one(query)
        except errors.PyMongoError:
            continue
