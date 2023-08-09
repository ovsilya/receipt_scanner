import os
import functions_framework
import openai
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')

@functions_framework.http
def prompt_image(request):

    request_json = request.get_json()
    items = request_json['input']['body']['items']

    query = "I ordered " + items + " what is that? give me a 1 sentence description so I can visualize it"

    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
            {"role": "assistant", "content": "only the description"}
        ]
    )

    prompt_image = Response['choices'][0]['message']['content']
    print('prompt_image: ', prompt_image)
    result = {"prompt_image": prompt_image}
    return jsonify(result)