from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import timedelta
from .device.fcs_injection_db import FCSInjectionDevice_db

logger = get_task_logger(__name__)
__oPeriod = 10              # initial period is 10s
__dPeriod = __oPeriod       # dynamic period

@periodic_task(run_every=timedelta(seconds=__oPeriod))
def pollDeviceStatus():
    logger.info("Polling device data (p={})...".format(__dPeriod))
    #ptask = PeriodicTask.objects.filter(name='scope_core.tasks.pollDeviceStatus')[0]
    result = FCSInjectionDevice_db.getDeviceStatus()
    logger.info("Result: %s" % result)