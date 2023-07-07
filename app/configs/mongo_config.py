from math import e
import pymongo
import logging

global _CLIENT
_CLIENT: pymongo.MongoClient | None = None


def initialize(url: str) -> bool:
    global _CLIENT
    if not _CLIENT:
        try:
            _CLIENT = pymongo.MongoClient(url)
            return True
        except Exception as e:
            logging.exception(e)
    return False


def client(class_name: str, chain_id: int):
    global _CLIENT
    if _CLIENT is not None:
        db = _CLIENT[str(chain_id)]
        col = db[class_name]
        return col
    else:
        raise RuntimeError("Mongo Not initiated !")


def _client(class_name: str):
    global _CLIENT
    if _CLIENT is not None:
        db = _CLIENT[class_name]
        col = db[class_name]
        return col
    else:
        raise RuntimeError("Mongo Not initiated !")
