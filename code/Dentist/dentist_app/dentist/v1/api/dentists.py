# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify

from . import Resource
from .. import schemas
import json

class Dentists(Resource):

    def get(self):
        with open('data.json') as data_file:
            data = json.load(data_file)
            data_file.close()
            result = data['available']
            output = ', '.join([str(name) for name in result])            
        return jsonify({'answer':"The available dentists: " + output})