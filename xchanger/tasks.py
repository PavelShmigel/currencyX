# -*- coding:utf-8 -*-
__author__ = 'pavel.sh'

from celery.task import periodic_task
from celery.utils.log import get_task_logger
from xchanger.tools.dbupdate import update_db


logger = get_task_logger(__name__)


@periodic_task(run_every=60*60)
def update_rates():
    logger.info("Start task update_rates")
    update_db()
    logger.info("Task update_rates: DONE")

