# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_cors import CORS

import json
import v1
STARTAPP = 1


def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    return app

if __name__ == '__main__':
    if STARTAPP == 1:
        with open('tempData.json') as data_file:
            data = json.load(data_file)
        file_out = open('tempData.json', "w")
        data['DOCNAME'] = 'Empty'
        data['TIMEVal'] = 'Empty'
        data['bookingStatus'] = '0'
        data['callForCancellation'] = '0'
        file_out.write(json.dumps(data))
        file_out.close()
        print("Cleared all the status \n")
        STARTAPP = 0
    create_app().run(port = 5000,debug=True)
