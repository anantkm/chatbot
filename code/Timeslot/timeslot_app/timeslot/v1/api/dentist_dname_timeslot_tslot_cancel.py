# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify

from . import Resource
from .. import schemas
import json


class DentistDnameTimeslotTslotCancel(Resource):

    def put(self, dname, tslot):

        print("dname:", dname)
        print("tslot:", tslot)


        # return {}, 200, None
        with open('data.json') as data_file:
            data = json.load(data_file)
        
         #Dentist name is not in the database 
        all_keys = data.keys()
        if dname not in all_keys:
            print("I did not find Dentist name "+dname+" in the database. Please check the dentist name and try again.\n")            
            return jsonify({"answer":"I did not find Dentist name "+dname+" in the database. Please check the dentist name and try again."})
        
        #specified timeslot not in the database.
        all_timeslots = data[dname]['time'].keys()        
        if tslot not in all_timeslots:
            print("I did not find the specified timeslot for dentist " +dname+" in the database. Please correct the timeslot you would like to cancel" )
            return jsonify({"answer":"I did not find the specified timeslot for dentist " +dname+" in the database. Please correct the timeslot you would like to cancel."})


        #the timeslot is already cancelled.
        if data[dname]['time'][tslot] == "not reserved":
            print("The time " + tslot + " you would like to cancel is available.")
            return jsonify({'answer':"The time " + tslot + " you would like to cancel is available."})

        

        #actual cacellation. 
        all_timeslots_list  = list(all_timeslots)
        timeslot_index = all_timeslots_list.index(tslot)        
        data[dname]['time'][tslot] = "not reserved"
        data[dname]['availableTime'].insert(timeslot_index,tslot)
        file_out = open('data.json', "w")
        file_out.write(json.dumps(data))
        print("You have successfully canceled " + tslot + " with " + dname)
        return jsonify({'answer': "You have successfully canceled " + tslot + " with " + dname})
        

            