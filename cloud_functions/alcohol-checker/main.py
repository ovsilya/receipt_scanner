import os
import functions_framework
import openai
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

@functions_framework.http
def alcohol_check(request):

    request_json = request.get_json()
    items = request_json['input']['body']['items']
    

    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Return a class only, nothing else."},
			{"role": "user", "content": "Classify the text in '''text'''by whether it includes alcohol drink(s) or not."},
            {"role": "user", "content": f"Text: {items}"},
            {"role": "assistant", "content": "There are only three classes: yes, no, unknown."},
            {"role": "assistant", "content": "If no/corrupted/ambiguous text is provided, the class is \"unknown\"."},
            {"role": "assistant", "content": "Return a class only, nothing else."}
        ]
    )
    # "If date or time has multiple mentions, give me only average value of each."
    alcohol_check = Response['choices'][0]['message']['content']
    print('alcohol_check: ', alcohol_check)
    result = {"alcohol_check": alcohol_check}
    return jsonify(result)