import os
import logging
from dotenv import load_dotenv
from dataclasses import dataclass
from celery import Task
from celery.signals import (
    worker_ready,
    # after_setup_task_logger,
    worker_process_init
)

from worker.a2s import async_run
from worker.configs.celery_config import config
from app.configs.redis_config import initialize
from app.utils.trx.four_bytes_function_selector import save_all_4bytes_function_selectors

try:
    load_dotenv(os.path.dirname(os.path.realpath(__file__)) + "/.env")
except:
    load_dotenv(".env")


REDIS_URL = os.getenv("REDIS_URL") or "redis://127.0.0.1:6381"
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL") or "redis://127.0.0.1:6377/8"
CELERY_RESULT_URL = os.getenv(
    "CELERY_RESULT_URL") or "redis://127.0.0.1:6377/8"

celery_instance = config(
    REDIS_URL,
    CELERY_BROKER_URL,
    CELERY_RESULT_URL,
)


@worker_process_init.connect
def startup_task(sender=None, conf=None, **kwargs):
    async_run(initialize(REDIS_URL))
    logging.info("celery is initializing Redis.")
    async_run(save_all_4bytes_function_selectors())
    logging.info("Function selectors are being added to MogoDB.")
   


class TaskWithRetry(Task):
    autoretry_for = (
        TypeError,
        ValueError
    )
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 1500
    retry_jitter = True
    rate_limit = "1/m"
    default_retry_delay = 30  # minutes
    interval_step = 15


@dataclass(frozen=True)
class RETRY_INTERVAL:
    REDIS_BUSY = 60 * 25  # minutes


# @after_setup_task_logger.connect
# def setup_task_logger(logger, *args, **kw):
#     gelf_config.config(
#         logger,
#         "CeleryV2.Worker"
#     )

@worker_ready.connect
def at_start(sender, **k):
    logging.info(celery_instance.control.purge())
