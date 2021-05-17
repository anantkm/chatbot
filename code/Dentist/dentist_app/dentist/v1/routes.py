# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.dentists import Dentists
from .api.dentist_details_dname import DentistDetailsDname


routes = [
    dict(resource=Dentists, urls=['/dentists'], endpoint='dentists'),
    dict(resource=DentistDetailsDname, urls=['/dentist/details/<dname>'], endpoint='dentist_details_dname'),
]