# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import requests

from . import Resource
from .. import schemas
import json

import os
from rivescript import RiveScript
from .wit import ask_wit, updateBIDfromtemp, resetTheStatus, readTempData
import re

username = 'anotheruser'
bot= RiveScript()
bot.load_directory(
    os.path.join(os.path.dirname(__file__), ".", "brain")
)
bot.sort_replies()


class Question(Resource):
    def get(self):
        expression = g.args.get("expression")
        print("User says: %s" % expression)
        
        answer = bot.reply(username, expression)
        if answer == 'callforCancel':
            print("control: callforCancel")
            with open('tempData.json') as data_file:
                cancel_data = json.load(data_file)
            data_file.close()
            
            with open('bookingInfo.json') as data_file:
                customer_info = json.load(data_file)
            data_file.close()

            if cancel_data['callForCancellation'] =='1':
                bookingID = re.findall(r'\bCB9322BID\w+', expression)[0]
                print("Found bookingID:",bookingID)
                if bookingID in customer_info:
                    cancel_docName = customer_info[bookingID][0]['DOCNAME']
                    cancel_docName = cancel_docName.strip()
                    cancel_bID = customer_info[bookingID][0]['TIMEVal'] 
                    cancel_bID = cancel_bID.strip()                   
                    url = requests.put("http://127.0.0.1:5003/v1/dentist/"+cancel_docName+"/timeslot/"+cancel_bID+"/cancel")
                    tempResponse = url.json() 
                    print(tempResponse)
                    tempResponse = tempResponse['answer']
                    if "You have successfully canceled" in tempResponse:
                        del(customer_info[bookingID])
                        file_out = open('bookingInfo.json', "w")
                        file_out.write(json.dumps(customer_info))
                        file_out.close()
                        answer = "You have sucessfully canclled appointment with booking ID : "+bookingID
                    else:
                        answer = tempResponse
                else:
                    answer ="I did not find the provided booking ID:"+bookingID            
            else:
                answer = "I don't understand what you are tying to do. If you are trying to cancel, please type cancel the booking."

        if answer == 'list':
            try:
                url = requests.get("http://127.0.0.1:5001/v1/dentists")
                result = url.json()
                answer = result['answer']
                
            except:
                print("ERR")
                answer = "ERR"

        if answer =='thanksRESPONSE':
            checkCache = readTempData()
            if checkCache['callForCancellation'] == 1 or checkCache['bookingStatus']==1:
                answer = "You are welcome!. See you soon."
            else:
                answer = "You can thank me later. Go ahead! Make an appointment."


        if "details010" in answer:
            answer = answer.replace('details010','')
            answer = answer.capitalize() 
            try:
                url = requests.get("http://127.0.0.1:5001/v1/dentist/details/"+ answer)
                result_temp = url.json()
                answer = result_temp['answer']
            except:
                answer = "ERR"
        
        if answer == "RIVEresetCurrentStatus":
            print("questions:RIVEresetCurrentStatus")
            resetTheStatus()
            answer = "You are all set to make a booking now."


        if 'RiveCheckNameandTime' in answer:
            print('RiveCheckNameandTime')
            with open('tempData.json') as data_file:
                data = json.load(data_file)
            data_file.close()
            if data['DOCNAME'] =='Empty' and data['TIMEVal'] == 'Empty':
                answer = "Looks like you have not provided Dentist's name and timeslot. Please provide the Dentist's Name and Timeslot to make an appointment"
            elif data['DOCNAME'] == 'Empty':
                answer = 'Please provide the dentist name to proceed with the booking.'
            elif data['TIMEVal'] == 'Empty':
                answer = 'Looks like you have not entered the timeslot. Please provide the timeslot to proceed with the booking.'
            elif data['bookingStatus'] =='1':
                answer = "You have already made an appointment. To make one more appointment please type 'Make a new appointment'"
            # else:
            #     url = requests.post("http://127.0.0.1:5003/v1/dentist/"+data['DOCNAME']+"/timeslot/"+data['TIMEVal'] +'/reserve')
            #     print("http://127.0.0.1:5003/v1/dentist/"+data['DOCNAME']+"/timeslot/"+data['TIMEVal'] +'/reserve')
            #     answer = url.json()  
        if "Nice to meet you" in answer:
            print('editing name')
            answer = answer[:17] + answer[17].swapcase() + answer[18:] 
            
        if "ERR" in answer:
            expression = expression.strip()
            with open('timeResponse.json') as data_file:
                time_response = json.load(data_file)
            data_file.close()
            with open('tempData.json') as data_file:
                timeUpdateData = json.load(data_file)            
            if expression in time_response['availableTime']:                
                if timeUpdateData['TIMEVal'] == 'Empty':
                    file_out = open('tempData.json', "w") 
                    timeUpdateData['TIMEVal']= expression.strip()           
                    file_out.write(json.dumps(timeUpdateData))
                    file_out.close()   
                    answer = 'manuelEntryTimeslot'
                else:
                    answer = "You have already updated the timeslot."
            else:
                answer = "checkwithWIT"

        if "checkwithWIT" in answer:
            print("Checking with Wit")
            answer = ask_wit(expression)
        with open('tempData.json') as data_file:
            data = json.load(data_file)
        data_file.close() 
        print("IN WIT PART | ", answer)            
        if 'WitElsePart' in answer:
            if data['bookingStatus']== str(1):
                answer = "Your already have an appointment. If you are trying to make an new appointment type 'Make a new appointment' or 'sample commands' to see sample commands"              
            else:
                answer = "I did not get that."
        
        elif (('WitUpdatedName' in answer)  or ('WitUpdatedTimeSlot' in answer) or ('manuelEntryTimeslot' in answer)):
            print("control: Questions booking.")

            if data['TIMEVal'] == 'Empty':
                answer = 'Looks like you have selected the Dentist but not the timeslot. Please provide the timeslot to proceed with the booking.'
            
            elif data['DOCNAME'] == 'Empty':
                answer = "Looks like you have not selected the Dentist. Please provide the Dentist's name to proceed with the booking."
            
            else:
                url = requests.put("http://127.0.0.1:5003/v1/dentist/"+data['DOCNAME']+"/timeslot/"+data['TIMEVal'] +'/reserve')
                temp_result = url.json()
                answer = temp_result['answer']
                if 'You have successfully booked' in answer:
                    file_out = open('tempData.json', "w")
                    data['bookingStatus'] = str(1)
                    newBID = data['lastgenbid']
                    tempNum = int(newBID[9:])+1
                    newBID = newBID[:9]+str(tempNum)
                    data['lastgenbid'] =newBID
                    file_out.write(json.dumps(data))
                    file_out.close()
                    updateBIDfromtemp()
                    print("Booking Sucessfull. Updated the file.\n")
                    answer = "You have Sucessfully made the booking. Here is the Summary: DoctorName : "+data['DOCNAME']+",  timeslot : "+ data['TIMEVal'] + " and Booking ID : "+ newBID +".    Please keep this ID handy for reference."
                if (('We do not have time' in answer) or ('you could choose from these timeslots' in answer)):
                    file_out = open('tempData.json', "w")
                    data['TIMEVal'] = 'Empty'
                    file_out.write(json.dumps(data))
                    file_out.close()     
                    print("Updated the name. Waiting for the new timeslot.")                           

            # else:
            #     answer = "I'm not sure what you are trying to say."
        
        if 'WitCheckNameandTime' in answer:
            print('WitCheckNameandTime')
            with open('tempData.json') as data_file:
                data = json.load(data_file)
            data_file.close()
            if data['DOCNAME'] =='Empty' and data['TIMEVal'] == 'Empty':
                answer = "Looks like you have not provided Dentist's name and timeslot. Please provide the Dentist's Name and Timeslot to make an appointment"
            elif data['DOCNAME'] == 'Empty':
                answer = 'Please provide the dentist name to proceed with the booking.'
            elif data['TIMEVal'] == 'Empty':
                answer = 'Looks like you have not entered the timeslot. Please provide the timeslot to proceed with the booking.'
            elif data['bookingStatus'] =='1':
                answer = "You have already made an appointment. To make one more appointment please type 'Make a new appointment'"

        print("Returned answer: {}".format(answer))
        return {'answer':answer}, 200, None
