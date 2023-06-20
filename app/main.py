import os
import logging
from fastapi.middleware.cors import CORSMiddleware

from configs import redis_config, fastapi_config, mongo_config, postgres_config
from save_function_selectors import save_first_function_selectors


logging.basicConfig(level=logging.INFO)

DOMAIN = os.getenv("DOMAIN") or "http://localhost:23456"
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"
# POSTGRES_URL = os.getenv("POSTGRES_URL") or "postgresql://postgres:password@localhost/testth"
MONGO_URL = os.getenv("MONGO_URL") or "mongodb://localhost:27017/"


app = fastapi_config.config(DOMAIN)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_boot():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()

    # postgres_config.InitializePostgres().create_db_and_tables()
    # postgres_config.InitializePostgres().insert_networks()
    # postgres_config.InitializePostgres().insert_chains()
    # save_first_function_selectors()

    from test_functions import _tt_

    await _tt_()
