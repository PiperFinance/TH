import os
import asyncio
import logging
from dotenv import load_dotenv
from pathlib import Path

from configs import redis_config, mongo_config
from save_function_selectors import save_first_function_selectors

if os.path.exists((env_file := f"{Path(os.getcwd())}/.env")):
    load_dotenv(env_file)


REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"
MONGO_URL = os.getenv("MONGO_URL") or "mongodb://localhost:27017/"


async def intialize():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()
    mongo_config.initialize(MONGO_URL)
    save_first_function_selectors()

try:
    asyncio.run(intialize())
except Exception as e:
    logging.exception(e)
