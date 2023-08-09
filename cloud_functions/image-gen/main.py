import functions_framework
import openai
import os
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

@functions_framework.http
def image_gen(request):
    
    request_json = request.get_json()
    prompt_image = request_json['input']['body']['prompt_image']
    
    response_image = openai.Image.create(
        prompt= prompt_image,
        n=1,
        size="1024x1024")
    
    image_url = response_image['data'][0]['url']
    print('image_url: ', image_url)
    result = {"image_url": image_url}
    return jsonify(result)