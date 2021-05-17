# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.dentist_timeslot_dname import DentistTimeslotDname
from .api.dentist_dname_timeslot_tslot_cancel import DentistDnameTimeslotTslotCancel
from .api.dentist_dname_timeslot_tslot_reserve import DentistDnameTimeslotTslotReserve


routes = [
    dict(resource=DentistTimeslotDname, urls=['/dentist/timeslot/<dname>'], endpoint='dentist_timeslot_dname'),
    dict(resource=DentistDnameTimeslotTslotCancel, urls=['/dentist/<dname>/timeslot/<tslot>/cancel'], endpoint='dentist_dname_timeslot_tslot_cancel'),
    dict(resource=DentistDnameTimeslotTslotReserve, urls=['/dentist/<dname>/timeslot/<tslot>/reserve'], endpoint='dentist_dname_timeslot_tslot_reserve'),
]