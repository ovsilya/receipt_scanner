# Alcohol Check Function

This repository contains a cloud function named `alcohol_check`. this function checks if a given text input contains any mention of alcohol drinks. It uses OpenAI's GPT-4 model for text classification and is hosted on Google Cloud.

## How does it work?

The function is triggered by an HTTP request sent to its endpoint. The function takes a JSON object as request where input is provided as text under the data key of 'items'. It uses OpenAI's ChatCompletion API to get a response by feeding the provided text to the model with predefined instructions.

The chat model is provided with a series of messages, where roles can be 'system', 'user', or 'assistant'. In our case, the user role messages contain the main task description and the text to classify, while the system messages set up the task/intent of the assistant role. 

The assistant then categorizes the text according to the presence of alcohol drink(s). The possible class values are:

- **yes**: The text explicitly mentions or describes alcohol drink(s).
- **no**: The text does not contain any mention or hint of alcohol drink(s).
- **unknown**: The provided text is corrupt, ambiguous, or not provided at all.

Based on this model response, it then returns a JSON object with classified class to the request sender.

## Usage

To use this function, make an HTTP POST request to the function's endpoint with `input` as the key and the `text` as the value in the request body.

```
{
    "input": {
        "body": {
            "items": "your_text_here"
        }
    }
}
```

The function will then return a JSON response with the `alcohol_check` key indicating the presence of alcohol in the provided text:

```json
{
    "alcohol_check": "yes/no/unknown"
}
```

## Dependencies

This code uses the openai python package.

```shell
pip install openai
```

It also uses the flask and functions_framework packages for serving the function on Google Cloud.

```shell
pip install flask functions-framework
```