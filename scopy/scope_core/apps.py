from __future__ import unicode_literals

from django.apps import AppConfig

from .tasks import pollDeviceStatus
from device.fcs_injection_db import FCSInjectionDevice_db


class ScopeCoreConfig(AppConfig):
    name = 'scope_core'
    verbose_name = 'Scope Device Adapter'
    
    def ready(self):
        fcsDevice = FCSInjectionDevice_db('B0750018')
        if fcsDevice.isConnected:
            pollDeviceStatus.delay()