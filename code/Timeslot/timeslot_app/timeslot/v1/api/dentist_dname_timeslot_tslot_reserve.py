# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify

from . import Resource
from .. import schemas
import json 


class DentistDnameTimeslotTslotReserve(Resource):

    def put(self, dname, tslot):
        print("dname",dname)
        print("tslot",tslot)
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
            allAvailTimeslots = ""
            avail_timeslot_count=0;
            for item in all_timeslots:
                if data[dname]['time'][item] == "not reserved":
                    avail_timeslot_count +=1;
                    allAvailTimeslots += item + ", "
            allAvailTimeslots = allAvailTimeslots[:-2]
            if avail_timeslot_count > 1:                
                print("I did not find the specified timeslot for dentist " +dname+" in the database. However you could choose from following timeslots : "+allAvailTimeslots )
                return jsonify({"answer":"I did not find the specified timeslot for dentist " +dname+" in the database. However you could choose from following timeslots : "+allAvailTimeslots })
            else:
                print("I did not find the specified timeslot for dentist " +dname+" in the database. Looks like all the timeslots are full." )
                return jsonify({"answer":"I did not find the specified timeslot for dentist " +dname+" in the database. Looks like all the timeslots are full."})

        #the timeslot is already booked.
        if data[dname]['time'][tslot] == "reserved":
            allAvailTimeslots = ""
            avail_timeslot_count=0;
            for item in all_timeslots:
                if data[dname]['time'][item] == "not reserved":
                    avail_timeslot_count +=1;
                    allAvailTimeslots += item + ", "
            allAvailTimeslots = allAvailTimeslots[:-2]
            if avail_timeslot_count >1:
                print("The time " + tslot + " you would like to book has been already booked, and however you could choose from these timeslots: " + allAvailTimeslots)
                return jsonify({'answer':"The time " + tslot + " you would like to book has been already booked, and however you could choose from these timeslots: " + allAvailTimeslots})
            else:
                print("The time " + tslot + " you would like to book has been already booked, and there are no more available timeslot for " + dname)
                return jsonify({'answer':"The time " + tslot + " you would like to book has been already booked, and there are no more available timeslot for " + dname})
        
        #actual reservation. 
        data[dname]['time'][tslot] = "reserved"
        data[dname]['availableTime'].remove(tslot)
        file_out = open('data.json', "w")
        file_out.write(json.dumps(data))
        print("You have successfully booked " + tslot + " with " + dname)
        return jsonify({'answer': "You have successfully booked " + tslot + " with " + dname})
