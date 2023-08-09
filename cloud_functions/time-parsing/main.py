
import os
import json
import openai
import functions_framework
from flask import jsonify, request

#Reading environment variables
project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

def str_to_dict(json_string):
    # Load the JSON string into a Python dictionary
    dictionary = json.loads(json_string)
    return dictionary

@functions_framework.http
def time_parsing(request):
    request_json = request.get_json()
    date_time = request_json['input']['body']['date_time']
    
    user_str = '''
        Extract from the text the following values: 
        - time as '%H:%M:%S', 
        - date as '%Y-%m-%d', 
        - day of the week, 
        - day period: Breakfast, Lunch, Dinner.
        '''

    Assistant_str = '''
        - Timeframe for Breakfast: from earliest possible until 11:30am
        - Timeframe for Lunch: from 11:30am to 5:00pm
        - Timeframe for Dinner: from 5:00pm till the latest possible time
        - If values not detected: use 'none' value. 
        - If multiple times detected: calculate average time and use as result time.
        - Return as json file with mandatory keys: time, date, day_of_week, day_period.
        '''

    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Return JSON only, no descriptions."},
            {"role": "user", "content": user_str},
            {"role": "user", "content": f"Text: {date_time}"},
            {"role": "assistant", "content": Assistant_str}
        ]
    )

    date_time_analysis = Response['choices'][0]['message']['content']
    # date_time_dict = str_to_dict(date_time_analysis) #cannot save JSON to BQ table set. Needs to be string
    result = {"date_time_analysis": date_time_analysis}
    return jsonify(result)