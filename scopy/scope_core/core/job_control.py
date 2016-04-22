#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manage Job activities and send corresponding Scope message
to the server
"""

from djcelery.models import IntervalSchedule
from lxml import etree
from scope_core.models import Machine, Job, ProductionDataTS, SessionManagement
from . import xmlparser
from . import request_sender

def processQueryResult(source, data, task=None):
    if source == 'opStatus':
        machine = Machine.objects.first()
        if data[0][0] == '離線':
            print 'Device is offline!'
            if machine.opmode != 0:
                machine.opmode = 0
                machine.save()
                request_sender.sendHttpRequest('false:bye', 'text')
        elif str(data[0][0])[0] == '1':
            if machine.opmode != 1:
                machine.opmode = 1
                machine.save()
                print 'Device in manual mode.'
        elif str(data[0][0])[0] == '2':
            if machine.opmode != 2:
                machine.opmode = 2
                machine.save()
                print 'Device in semi-auto mode.'
        elif str(data[0][0])[0] == '3':
            if machine.opmode != 3:
                machine.opmode = 3
                machine.save()
                print 'Device in auto mode.'
        else:
            pass
        
    elif source == 'opMetrics':
        mct = data[0][0]
        pcs = data[0][1]
        scopemsg = xmlparser.getJobUpdateXml(pcs, mct)
        request_sender.sendHttpRequest(scopemsg)
        
        dataEntry = ProductionDataTS.objects.create(job=SessionManagement.objects.first().job)
        dataEntry.output = pcs
        dataEntry.mct = mct
        dataEntry.save()
        
        if task is None:
            print '!!! Unable to update task period due to missing argument !!!'
        else:
            # Compare polling period with retrieved mct value
            if mct != task.interval.every:
                intv, created = IntervalSchedule.objects.get_or_create(
                    every=mct, period='seconds'
                )
                task.interval_id = intv.id
                task.save()
        
    elif source == 'alarmStatus':
        session = SessionManagement.objects.first()
        session.errid = data[0][1]
        if str(data[0][2]) == '1':
            if not session.errflag:
                session.errflag = True
                sendEventMsg(4, session.errid)
        else:
            session.errflag = False
            sendEventMsg(1)
        session.save()
    
    else:
        pass

def sendEventMsg(type, code=""):
    scopemsg = xmlparser.getJobEventXml(type, code)
    request_sender.sendHttpRequest(scopemsg)