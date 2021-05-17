# from .openweathermap import get_weather_forecast
# from .restaurant import get_restaurant_list
from .credentials import TOKEN
import requests
from datetime import datetime
import calendar
import json 

def resetTheStatus():
    print("control:resetTheStatus")
    with open('tempData.json') as data_file:
        jsondata = json.load(data_file)
    data_file.close()
    file_out = open('tempData.json', "w")   
    jsondata['DOCNAME'] = 'Empty'
    jsondata['TIMEVal'] = 'Empty'
    jsondata['bookingStatus'] = '0'
    jsondata['callForCancellation'] = '0'
    file_out.write(json.dumps(jsondata))
    file_out.close()
    print("Sucessfully cleared temp / current data\n")


def formatTheName(input_name):
    if 'dentist' in input_name:
        input_name = input_name.replace("dentist", "")
    if 'doctor' in input_name:
        input_name = input_name.replace("doctor", "")
    input_name = input_name.strip()
    input_name = input_name.capitalize()  
    return input_name   

def readTempData():
    with open('tempData.json') as data_file:
        jsondata = json.load(data_file)
    return jsondata

def updateBIDfromtemp():
    with open('tempData.json') as data_file:
        jsondata = json.load(data_file)
    with open('bookingInfo.json') as booking_file:
        bookingData = json.load(booking_file)
    bookingData[jsondata['lastgenbid']] = [{'DOCNAME':jsondata['DOCNAME'],'TIMEVal':jsondata['TIMEVal']}]
    file_out = open('bookingInfo.json', "w")    
    file_out.write(json.dumps(bookingData))
    file_out.close()
    print("Updated the BID in booking file sucessfully \n ")

def checkDocNameInDB(dentistName):
    print("control:checkDocNameInDB\n")
    print("Calling the URL : http://127.0.0.1:5001/v1/dentists")
    url = requests.get("http://127.0.0.1:5001/v1/dentists")
    result = url.json()
    temp = result['answer']
    print("temp:", temp)
    if dentistName in temp:
        print("foundDocNAME")
        return 'foundDocNAME'
    return 'notFoundDocNAME'


def ask_wit(expression):
#    print('expression:',expression)
    result = requests.get('https://api.wit.ai/message?v=20201102&q={}'.format(expression),
                        headers={'Authorization': TOKEN})

    jsonResult = result.json()
    # print(jsonResult['intents'][0]['name'])
    #Fri 16-17pm
    answer = 'Empty'    
    try:                    
        if len(jsonResult['intents']) == 0:
            print("control:wit:ZeroJasonResult\n")
            dentistName = jsonResult['entities']['wit$contact:contact'][0]['value']
            print("Only Doctor Name was entered. Value: ",dentistName)  
            readJasonFile = readTempData () 
            if readJasonFile['DOCNAME'] =='Empty':
                readJasonFile['DOCNAME'] = dentistName
                file_out = open('tempData.json', "w")                
                file_out.write(json.dumps(readJasonFile))
                file_out.close()
                answer = 'WitUpdatedName'
            elif readJasonFile['TIMEVal'] =='Empty':
                answer = 'You have already selected the dentist: ' + readJasonFile['DOCNAME'] + ". Please provide the Timeslot to make an appointment"
            else: 
                answer = 'WitElsePart_NameOnly'

        elif  jsonResult['intents'][0]['name'] == 'dentistDetails':
            print("control:dentistDetails\n")
            detailsName = jsonResult['entities']['wit$contact:contact'][0]['value']
            print("detected details Name: {}".format(detailsName))
            if 'dentist' in detailsName:
                detailsName = detailsName.replace("dentist", "")
            if 'doctor' in detailsName:
                detailsName = detailsName.replace("doctor", "")
            detailsName = detailsName.strip()
            detailsName = detailsName.capitalize() 
            print("Corrected Name: {}".format(detailsName))
            print("Calling details URL:" + "http://127.0.0.1:5001/v1/dentist/details/"+ detailsName)
            url = requests.get("http://127.0.0.1:5001/v1/dentist/details/"+ detailsName)
            result = url.json()
            answer = result['answer']
            
                                
                

        elif jsonResult['intents'][0]['name'] == 'aptNameTime':
            print("control:aptNameTime\n")
            dayandtime = jsonResult['entities']['wit$datetime:datetime'][0]['value']
            name = jsonResult['entities']['wit$contact:contact'][0]['value']
            print("Time detected: {}".format(dayandtime))
            print("Name detected: {}".format(name))
            
            #formatting the Name
            if 'dentist' in name:
                name = name.replace("dentist", "")
            if 'doctor' in name:
                name = name.replace("doctor", "")
            name = name.strip()
            name = name.capitalize() 

            #building the timeslot.
            day_value = int(dayandtime[8:10])
            month_value = int(dayandtime[5:7])
            year_value = int(dayandtime[:4])
            dayoftheweek = datetime(year_value,month_value,day_value,0,0,0).strftime('%A')
            dayoftheweek = dayoftheweek[:3]
            from_time = dayandtime[11:13]
            to_time = str(int(from_time)+1)
            # flag = 'am'
            # if int(from_time)>12:
            #     flag = 'pm'
            if int(from_time)<10:
                from_time = from_time[1:]
            # appointment_slot  = dayoftheweek+' '+from_time+'-'+to_time+flag
            appointment_slot  = dayoftheweek+' '+from_time+'-'+to_time
            print(appointment_slot)
            with open('tempData.json') as data_file:
                data = json.load(data_file)
            data_file.close()
            if data['bookingStatus']=='1':
                answer = "Looks like you have already made an booking. To make a another booking type 'make a new booking'"
                print(answer)
            else:
                print("Calling details URL:" + "http://127.0.0.1:5003/v1/dentist/"+name+"/timeslot/"+appointment_slot +'/reserve')
                url = requests.put("http://127.0.0.1:5003/v1/dentist/"+name+"/timeslot/"+appointment_slot +'/reserve')
                result = url.json()
                answer = result['answer']
                if 'You have successfully booked' in answer:
                    file_out = open('tempData.json', "w")
                    data['DOCNAME'] = name
                    data['TIMEVal'] = appointment_slot
                    data['bookingStatus'] = '1'
                    newBID = data['lastgenbid']
                    tempNum = int(newBID[9:])+1
                    newBID = newBID[:9]+str(tempNum)
                    data['lastgenbid'] =newBID
                    file_out.write(json.dumps(data))
                    file_out.close()
                    updateBIDfromtemp()
                    print("Booking Sucessfull. Updated the file.\n")
                    print("Booking Sucessfull. Updated the file.\n")
                    answer = "You have Sucessfully made the booking. Here is the Summary: DoctorName : "+data['DOCNAME']+",  timeslot : "+ data['TIMEVal'] + " and Booking ID : "+ newBID +".    Please keep this ID handy for reference."
                    
                if (('We do not have time' in answer) or ('you could choose from these timeslots' in answer)):
                    file_out = open('tempData.json', "w")
                    data['DOCNAME'] = name
                    data['TIMEVal'] = 'Empty'
                    file_out.write(json.dumps(data))
                    file_out.close()     
                    print("Updated the name. Waiting for the new timeslot.")   

        elif jsonResult['intents'][0]['name'] == 'aptTime':
            print("control:aptTime\n")
            dayandtime = jsonResult['entities']['wit$datetime:datetime'][0]['value']
            print("Time detected: {}".format(dayandtime))
                        #building the timeslot.
            day_value = int(dayandtime[8:10])
            month_value = int(dayandtime[5:7])
            year_value = int(dayandtime[:4])
            dayoftheweek = datetime(year_value,month_value,day_value,0,0,0).strftime('%A')
            dayoftheweek = dayoftheweek[:3]
            from_time = dayandtime[11:13]
            to_time = str(int(from_time)+1)
            print("from_time: ",from_time)
            print("\nto_time: ",to_time)
            # flag = 'am'
            # if int(to_time)>=12:
            #     flag = 'pm'
            if int(from_time)<10:
                from_time = from_time[1:]

            # appointment_slot  = dayoftheweek+' '+from_time+'-'+to_time+flag
            appointment_slot  = dayoftheweek+' '+from_time+'-'+to_time

            print(appointment_slot) 
            with open('tempData.json') as data_file:
                data = json.load(data_file)
            data_file.close()
            if data['TIMEVal'] =='Empty':
                file_out = open('tempData.json', "w")
                data['TIMEVal'] = appointment_slot
                file_out.write(json.dumps(data))
                file_out.close()
                answer = 'WitUpdatedTimeSlot'
                print(answer)
            elif data['DOCNAME'] =='Empty':
                    answer = 'You have already selected the timeslot: ' + data['TIMEVal'] + ". Please provide the Dentist Name to make an appointment"
            else:
                answer = 'WitElsePart_aptTime'
                print(answer)            
        elif jsonResult['intents'][0]['name'] == 'appointdoc':
            print("control:appointdoc\n")
            docname_value = jsonResult['entities']['wit$contact:contact'][0]['value']
            print("Found Doctor Name:", docname_value)
            docname_value = formatTheName(docname_value)
            print("Formatted Doc Name:", docname_value)
            temp = checkDocNameInDB(docname_value)
            if temp =='foundDocNAME':
                with open('tempData.json') as data_file:
                    data = json.load(data_file)
                data_file.close()
                if data['DOCNAME'] =='Empty':
                    file_out = open('tempData.json', "w")
                    data['DOCNAME'] = docname_value
                    file_out.write(json.dumps(data))
                    file_out.close()
                    answer = 'WitUpdatedName'
                elif data['TIMEVal'] =='Empty':
                    answer = 'You have already selected the dentist: ' + data['DOCNAME'] + ". Please provide the Timeslot to make and appointment"
                else:
                    answer = 'WitElsePart_appointdoc' 
            else: 
                answer = 'I did not find dentist '+ docname_value+ "'s name in the database. Type 'list available dentists' to see all the detists."

        elif jsonResult['intents'][0]['name'] == 'listTimeslot':
            print("control:listTimeslot")
            listname  = jsonResult['entities']['wit$contact:contact'][0]['value']
            print("Resolved Name: ", listname)
            listname = formatTheName(listname)
            print("Formatted Name is ",listname)
            print("http://127.0.0.1:5003/v1/dentist/timeslot/"+listname)
            url = requests.get("http://127.0.0.1:5003/v1/dentist/timeslot/"+listname)
            result = url.json()
            answer = result['answer']
            print(answer)
        
        elif jsonResult['intents'][0]['name'] == 'aptCancel':
            print("control : aptCancel")
            cancel_data = readTempData()
            if cancel_data['callForCancellation'] == '0':
                cancel_data['callForCancellation'] = '1'
                file_out = open('tempData.json', "w")
                file_out.write(json.dumps(cancel_data))
                file_out.close()         
                answer = "You have opted for cancellation of booking. Please provide the booking ID to proceed with the cancellation.\n Please note that this is a irreversible action."
            else:
                answer = "Please provide the booking ID to proceed with the Cancellation of the appointment."
        
        elif jsonResult['intents'][0]['name'] == 'bookingHelp':
            print("control : bookingHelp")
            answer = "WitCheckNameandTime"
    except KeyError as err:
        answer = "I don't understand :("
    return answer



