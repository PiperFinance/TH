from fastapi import APIRouter


from . import (
    get_func_selectors,
    get_trxs,
    save_func_selectors,
    save_trxs
)

routers = APIRouter()

routers.include_router(
    save_func_selectors.routes,
    tags=["Save Function Selector"])

routers.include_router(
    get_func_selectors.routes,
    tags=["Get Function Selector"])


routers.include_router(
    save_trxs.routes,
    tags=["Save Transaction"])

routers.include_router(
    get_trxs.routes,
    tags=["Get Transaction"])
