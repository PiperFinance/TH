from fastapi import APIRouter


from . import (
    get_function_selectors,
    get_trxs,
    get_trxs_with_no_labels,
    save_function_selectors,
    save_trxs,
    save_trxs_with_no_labels,
    delete_trxs_with_no_labels,
    update_trxs
)

routers = APIRouter()

routers.include_router(
    save_function_selectors.routes,
    tags=["Save Function Selectors"])

routers.include_router(
    get_function_selectors.routes,
    tags=["Get Function Selectors"])


routers.include_router(
    save_trxs.routes,
    tags=["Save Transactions"])


routers.include_router(
    get_trxs.routes,
    tags=["Get Transactions"])


routers.include_router(
    update_trxs.routes,
    tags=["Update Transactions"])


routers.include_router(
    save_trxs_with_no_labels.routes,
    tags=["Save Transactions with no Labels"])


routers.include_router(
    get_trxs_with_no_labels.routes,
    tags=["Get Transactions with no Labels"])


routers.include_router(
    delete_trxs_with_no_labels.routes,
    tags=["Delete Transactions with no Labels"])
