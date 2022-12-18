import pymongo
import logging

global _CLIENT
_CLIENT = None


def initialize(url: str) -> bool:
    global _CLIENT
    if not _CLIENT:
        try:
            _CLIENT = pymongo.MongoClient(url)
            return True
        except Exception as e:
            logging.exception(e)
            return False


def client(
    class_name: str,
    chain_id: int
):
    global _CLIENT
    db = _CLIENT[str(chain_id)]
    col = db[class_name]
    return col


def function_selector_client(
    class_name: str,
):
    global _CLIENT
    db = _CLIENT[class_name]
    col = db[class_name]
    return col
