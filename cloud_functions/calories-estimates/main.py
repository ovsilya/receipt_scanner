import os
import json
import openai
import functions_framework
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

def str_to_dict(json_string):
    # Load the JSON string into a Python dictionary
    dictionary = json.loads(json_string)
    return dictionary

@functions_framework.http
def calories_estimates(request):

    request_json = request.get_json()
    items = request_json['input']['body']['items']

    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Return JSON only, no descriptions."},
            {"role": "user", "content": "The text represents the information from a restaurant receipt."},
            {"role": "user", "content": "Generate JSON file wih the following parameters: key=item in the receipt; value=estimated calories in the item;"},
            {"role": "user", "content": "Add the last key \"total\" and its value = sum of all item's calories;"},
            {"role": "user", "content": f"Text: {items}"},
            {"role": "assistant", "content": "Each key represent a single item from the menu."},
            {"role": "assistant", "content": "Include customization into the item. Ex. steak, (medium rare, no ketchup, no bun)."},
            {"role": "assistant", "content": "Add the last key \"total\" and its value = sum of item\'s calories."},
            {"role": "assistant", "content": "If no/empty/corrupted list items provided, return empty JSON."},
            {"role": "assistant", "content": "If ambiguous items, assign value = \'unknown\'"},
            {"role": "assistant", "content": "Return JSON only, no descriptions."}
        ]
    )
    # "If date or time has multiple mentions, give me only average value of each."
    calories = Response['choices'][0]['message']['content']
    # calories_dict = str_to_dict(calories) #cannot save JSON to BQ table set. Needs to be string
    result = {"calories": calories}
    return jsonify(result)