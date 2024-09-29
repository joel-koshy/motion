import google.generativeai as genai # ver 0.8.2 w/ 'google' api ver 3.0.0
import os # standard
import json 
import typing_extensions as typing

class EventObject(typing.TypedDict): 
    title:str
    start:str
    end:str
    eventType:str

genai.configure(api_key=os.environ['API_KEY']) # start gemini session
model = genai.GenerativeModel("gemini-1.5-flash") # declare gemini model
conf_data = genai.GenerationConfig(response_mime_type="application/json", response_schema=list[EventObject])

def get_ai_output(pdf):
    syllabus = genai.upload_file(pdf)
    event_name = model.generate_content([syllabus, "Return the details of all course-work, including but not limited to quizes, exams, homeworks, and class times on the syllabus as a raw json object without text formatting. All coursework eventTypes must either be Assesment or Assignment. All class-time eventTypes must be Course. There must only be one entry for each Assignment or Assesment i.e objects with the same title should not exist. The property start represents the due date of the assignment or the test-date of the assesment or when a class starts. End must represents the end time of classes, for eventTypes of Assignments and Assesments this must be the same as the start value.  All dates must follow the formatting YYYY-MM-DD.  Maintain this format for all requests of this nature going forward."],
    generation_config=conf_data).text
    print(event_name)   
    json_obj = json.loads(event_name)
    return json_obj 