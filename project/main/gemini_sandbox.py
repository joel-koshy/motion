import google.generativeai as genai # ver 0.8.2 w/ 'google' api ver 3.0.0
import os # standard
import sys # standard
import subprocess # standard
import jicson # ver 1.0.2
import json 
import typing_extensions as typing

class CalEvent(typing.TypedDict):
    date: str
    events: list[str]

''' TESTED ON/USES PYTHON 3.10 | GEMINI REQUIRES PYTHON >= 3.9 | ADJUST CODE AND DEPENDENCIES AS NEEDED '''
genai.configure(api_key=os.environ['API_KEY']) # start gemini session
model = genai.GenerativeModel("gemini-1.5-flash") # declare gemini model
conf_data = genai.GenerationConfig(response_mime_type="application/json", response_schema=list[CalEvent])
# syllabus = genai.upload_file("/Users/vishnukunnummal/Documents/School/GSU/2024-25/Fall 2024/CHEM 1211K/CHEM 1211_Fall 2024_ACH80 syllabus1.pdf") # upload pdf --> FEED FROM USER INPUT
# num_events = model.generate_content(["Tell me how many assignment due dates, quiz dates, and exam dates there are for this course. Just output a single number total, no other text", syllabus]).text # determines how many events there are in a syllabus in order to see how many times it needs to add an event to the calendar

def get_ai_output(pdf):
    syllabus = genai.upload_file(pdf)
    num_events = model.generate_content(["Tell me how many assignment due dates, quiz dates, and exam dates there are for this course. Just output a single number total, no other text.", syllabus]).text
    # calender_events_json = {}
    # event_name = model.generate_content(["Return the details of the first due date/quiz date/exam date on the syllabus schedule as a .ICS file", syllabus]).text.strip('`').strip('ics\n') # returns ics file as plaintext after stripping excess text
    # event_name = model.generate_content(["Return the details of all due date/quiz date/exam date on the syllabus schedule as a raw json object without text formatting.  Maintain this format for all requests of this nature going forward.", syllabus]).text
    event_name = model.generate_content([syllabus, "Return the details of all due date/quiz date/exam date on the syllabus schedule as a raw json object without text formatting.  Maintain this format for all requests of this nature going forward."],
generation_config=conf_data).text
    print(event_name)   
    # json_obj = jicson.fromText(event_name) # converts ics to json object using jicson library
    json_obj = json.loads(event_name)
    # calender_events_json = calender_events_json.update(json_obj)
    return json_obj 


    for i in range(int(num_events)):
        if i == 0: # prompt for first event is slightly different than for others
            event_name = model.generate_content(["Return the details of the first due date/quiz date/exam date on the syllabus schedule as a .ICS file", syllabus]).text.strip('`').strip('ics\n') # returns ics file as plaintext after stripping excess text
            # print(event_name) # debugging use, may remove this
            # f = open("my_event.ics", 'w') # opens new ics file for writing
            # f.write(event_name) # adds plaintext to ics file
            # if os.name == 'nt':  # opens newly written ics file for windows systems
            #     os.startfile('my_event.ics')
            # elif os.name == 'posix':  # opens newly written ics file for mac
            #     opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            #     subprocess.call([opener, 'my_event.ics'])
            json_obj = jicson.fromText(event_name) # converts ics to json object using jicson library
            calender_events_json = calender_events_json.update(json_obj)
            # print(json_obj) 
            # with open("sample.json", "w") as outfile: # writes json_obj to sample.json file
            #     outfile.write(json_obj)
            # ''' ADD CODE TO UPLOAD JSON TO MONGODB HERE '''

        else:
            continue 
                # same process as above conditional but for events that aren't listed first
            event_name = model.generate_content(["Return the details of the next due date/quiz date/exam date on the syllabus schedule as a .ICS file. Maintain the same format for all future requests of this type going forward.", syllabus]).text.strip('`').strip('ics\n')
            print(event_name)
            json_obj = jicson.fromText(event_name)
            print(calender_events_json, json_obj)
            # calender_events_json = calender_events_json.update(json_obj)

            # f = open("my_event.ics", 'w')
            # f.write(event_name)
            # if os.name == 'nt':
            #     os.startfile('my_event.ics')
            # elif os.name == 'posix':
            #     opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            #     subprocess.call([opener, 'my_event.ics'])
    return calender_events_json 

# for i in range(int(num_events)): # loops through each event, adding to the calendar each time

#     if i == 0: # prompt for first event is slightly different than for others
#         event_name = model.generate_content(["Return the details of the first due date/quiz date/exam date on the syllabus schedule as a .ICS file", syllabus]).text.strip('`').strip('ics\n') # returns ics file as plaintext after stripping excess text
#         print(event_name) # debugging use, may remove this
#         f = open("my_event.ics", 'w') # opens new ics file for writing
#         f.write(event_name) # adds plaintext to ics file
#         if os.name == 'nt':  # opens newly written ics file for windows systems
#             os.startfile('my_event.ics')
#         elif os.name == 'posix':  # opens newly written ics file for mac
#             opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
#             subprocess.call([opener, 'my_event.ics'])
#         json_obj = jicson.fromText(event_name) # converts ics to json object using jicson library
#         print(json_obj) # print to verify
#         with open("sample.json", "w") as outfile: # writes json_obj to sample.json file
#             outfile.write(json_obj)
#         ''' ADD CODE TO UPLOAD JSON TO MONGODB HERE '''

#     else: # same process as above conditional but for events that aren't listed first
#         event_name = model.generate_content(["Return the details of the next due date/quiz date/exam date on the syllabus schedule as a .ICS file", syllabus]).text.strip('`').strip('ics\n')
#         print(event_name)
#         f = open("my_event.ics", 'w')
#         f.write(event_name)
#         if os.name == 'nt':
#             os.startfile('my_event.ics')
#         elif os.name == 'posix':
#             opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
#             subprocess.call([opener, 'my_event.ics'])