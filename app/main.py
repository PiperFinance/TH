import os
import uvicorn
from dotenv import load_dotenv
from pathlib import Path

from configs import redis_config, fastapi_config, mongo_config

load_dotenv(f"{Path(os.getcwd())}/.env")


DOMAIN = os.getenv("DOMAIN") or "http://localhost:23456"
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"
MONGO_URL = os.getenv("MONGO_URL") or "mongodb://localhost:27017/"


app = fastapi_config.config(DOMAIN)


@app.on_event("startup")
async def app_boot():
    await redis_config.initialize(REDIS_URL)
    redis_config.isConnected()
    mongo_config.initialize(MONGO_URL)
    from test_functions import _tt_

    await _tt_()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=23456)
