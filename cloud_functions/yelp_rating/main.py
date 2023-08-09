import functions_framework
import os
import openai
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

@functions_framework.http
def yelp_rating(request):

    request_json = request.get_json()
    name = request_json['input']['body']['name']
    address = request_json['input']['body']['address']
        
    query = "Give me a list of 5 restaurants similar to " + name + " near " + address

    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Generate only JSON, no extra descriptions."},
            {"role": "user", "content": f"Generate a list of top 5 restaurants similar to {name}."},
			{"role": "user", "content": f"Address of the restaurant: {address}."},
            {"role": "assistant", "content": "Rating is based on YELP"},
            {"role": "assistant", "content": "Restaurants are within 3km from the one mentioned in the \"user\" message"},
            {"role": "assistant", "content": "Output format -- JSON format."},
            {"role": "assistant", "content": "JSON Keys: name of the place, address, rating, cuisine type, distance from the restaurant mentioned in the prompt"},
            {"role": "assistant", "content": "return only JSON, no extra descriptions"}
        ]
    )
    rating = Response['choices'][0]['message']['content']
    print('rating: ', rating)
    result = {"rating": rating}
    return jsonify(result)