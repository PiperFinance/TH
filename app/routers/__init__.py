from fastapi import APIRouter


from . import (
    get_function_selectors,
    get_trxs,
    get_trxs_with_no_labels,
    save_function_selectors,
    save_trxs,
    save_trxs_with_no_labels,
    delete_trxs_with_no_labels

)

routers = APIRouter()

routers.include_router(
    save_function_selectors.routes,
    tags=["Save Function Selector"])

routers.include_router(
    get_function_selectors.routes,
    tags=["Get Function Selector"])


routers.include_router(
    save_trxs.routes,
    tags=["Save Transaction"])


routers.include_router(
    get_trxs.routes,
    tags=["Get Transaction"])


routers.include_router(
    save_trxs_with_no_labels.routes,
    tags=["Save Transactions with no Labels"])


routers.include_router(
    get_trxs_with_no_labels.routes,
    tags=["Get Transactions with no Labels"])


routers.include_router(
    delete_trxs_with_no_labels.routes,
    tags=["Delete Transactions with no Labels"])
