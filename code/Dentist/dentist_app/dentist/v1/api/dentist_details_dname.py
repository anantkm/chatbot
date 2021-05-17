# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify

from . import Resource
from .. import schemas
import json 

class DentistDetailsDname(Resource):

    def get(self, dname):
        with open('data.json') as data_file:
            json_data = json.load(data_file)
        data_file.close()
        if dname in json_data:
            return (jsonify({'answer': dname + " has specialized in " + json_data[dname]['specialization'] + " and located at " + json_data[dname]['location']}))
        else:
            return jsonify({'answer':"I could not find " + dname + "'s name in the database. You could check all the available dentists by typing 'show all the dentists' "})