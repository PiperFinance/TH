import time
from typing import List
from fastapi import FastAPI, Request

from models import Chain
from utils.types import ChainId
from errors.custom_error import Errors


def add_middlewares(app: FastAPI):

    @app.middleware("http")
    async def time_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    return app


def check_chain(chain_id: ChainId):
    if chain_id not in Chain.supported_chains():
        raise Errors.ChainIdNotSupported


def check_chains(chain_ids: List[ChainId]):
    for chain_id in chain_ids:
        check_chain(chain_id)
