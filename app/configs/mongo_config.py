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
    chain_id: int,
    index: str = None
):
    global _CLIENT
    if _CLIENT[str(chain_id)][class_name] != None:
        return _CLIENT[str(chain_id)][class_name]
    db = _CLIENT[str(chain_id)]
    col = db[class_name]
    if index != None:
        col.create_index(index, unique=True)
    return col


def function_selector_client(
    class_name: str,
    index: str = None
):
    global _CLIENT
    if _CLIENT[class_name][class_name] != None:
        return _CLIENT[class_name][class_name]
    db = _CLIENT[class_name]
    col = db[class_name]
    if index != None:
        col.create_index(index, unique=True)
    return col
