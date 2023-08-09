# Yelp Rating Flask API

This flask-api provides a service that generates a list of top 5 restaurants around a specific location, which are similar to a particular restaurant. It uses the OpenAI's GPT-4 to analyze and provide a list of restaurants, all in a JSON format. The scoring system for restaurants is based on Yelp's rating.

## Code Description

The script sets up a Flask API service using the Functions Framework. When the service receives a POST request, the `yelp_rating` function is invoked with the request object as an argument.

The function fetches the HTTP POST request data in JSON format which includes the name and address of a restaurant. The name and address of the restaurant is then inserted into a query string which asks to "Give me a list of 5 restaurants similar to [name] near [address]".

Next, a `ChatCompletion` is created using OpenAI's API which simulates a conversation asking the model to generate a list of top 5 similar restaurants, providing the address of the restaurant and the format of the output.

The response from the model is then printed out and returned to the client as a JSON object.

## Environment Variables

- `GCP_PROJECT`: Your Google Cloud Project ID.
- `OPENAI_ORGANIZATION`: Your OpenAI Organization ID.
- `OPENAI_API`: Your OpenAI API key.

## Setup

1. Ensure you have the necessary environment variables set up.
2. Install the necessary dependency, `Flask`, using pip: 
    ```
    pip install flask
    ```
3. Run the flask API.
    ```
    python app.py
    ```
4. Make a POST request to `http://localhost:8080/` with the restaurant's name and address.

## Request Object

The request object structure should be like:

```json
{
	"input": {
		"body": {
			"name": "Restaurant Name",
			"address": "Restaurant Address"
		}
	}
}
```

This structure allows the API to know exactly where to get the necessary data regardless of the caller's language or structure.

## Response Object

The object returned contains a single key, "rating", with the value being a JSON of the list of the restaurants.