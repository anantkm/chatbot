# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify

from . import Resource
from .. import schemas
import json


class DentistTimeslotDname(Resource):

    def get(self, dname):
        with open('data.json') as data_file:
            json_data = json.load(data_file)
        data_file.close()

        all_keys = json_data.keys()
        if dname not in all_keys:
            print('I did not find dentist '+dname+' in the database.\n')            
            return jsonify({'answer':'I did not find dentist '+dname+' in the database.'})
        
        if len(json_data[dname]['availableTime']) < 1:
            print('Unfortunately Dentist '+dname+ ' do not have available timeslot this week.')
            return jsonify({'answer':'Unfortunately Dentist '+dname+ ' do not have available timeslot this week.'})        

        result = json_data[dname]['availableTime']
        output = ', '.join([str(value) for value in result])
        return jsonify({'answer': "A list of available timeslot of " + dname + ": " + output})

