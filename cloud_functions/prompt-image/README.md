# Flask App using OpenAI API

This Flask web application is a deployment of an API endpoint on Google Cloud Platform's Functions Framework.

The purpose of this application is to use OpenAI's API for generating text from the GPT-4 model. 

The text that the model generates is intended to give a one-sentence description of a user's order for them to visualize it.

## Working

The function prompt_image receives a POST request at the root URL which contains a JSON body. This JSON body includes the name of items the user has ordered.

These items are then concatenated with a string to form a query: "I ordered {items} what is that? give me a 1 sentence description so I can visualize it"

This query is then sent to the GPT-4 model as a user's content to generate a one-sentence description of the items ordered.

The response from the model is a string which is stored in the prompt_image variable and sent back to the client in the form of a JSON object.

## Environment Variables

The GCP_PROJECT environment variable stores the project ID of the Google Cloud Platform.

The OPENAI_ORGANIZATION environment variable stores the organization ID for OpenAI.

The OPENAI_API environment variable stores the API key for OpenAI.

## Dependent Services

This application is dependent on OpenAI's GPT-4 model to process the user's request and generate a one-sentence description of the ordered items.

## Example

For example, if the user sends a POST request to the endpoint with the JSON body:
```json
{
    "input": {
        "body": {
            "items": "Pizza, Coke"
        }
    }
}
```
Then, the model might return:
```json
{
    "prompt_image": "A pizza with a bubbly crust and abundant toppings of cheese, vegetables and meat, delivered with a chilled, carbonated coke."
}
```