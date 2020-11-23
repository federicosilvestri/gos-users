"""
This file contains all background tasks for users-ms
"""
from gooutsafe import celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

import datetime
from datetime import timedelta

from gooutsafe.dao.customer_manager import CustomerManager

logger = get_task_logger(__name__)


@celery.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    # Executes every minutes
    sender.add_periodic_task(
        crontab(minute='*'),
        check_customer_health_status.s(),
    )

    logger.info('Period Tasks scheduled with celery')


@celery.task()
def check_customer_health_status():
    logger.info('Executing the task <customer_healthcheck>')
    positive_users = CustomerManager.retrieve_all_positive()

    for positive_user in positive_users:
        time_delta = datetime.datetime.utcnow() - positive_user.health_status_change_datetime

        if time_delta >= timedelta(days=14):
            # unmarking
            positive_user.set_health_status(False)
            CustomerManager.update_customer(customer=positive_user)

    logger.info('Task <customer_healthcheck> finished')
