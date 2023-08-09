# Calories Estimates Function

This repository contains a Python script for calories estimation of restaurant items based on receipt data. The main function 'calories_estimates' is deployed as a Google Cloud Function to process receipt data input and generate an estimate of the calories contained within each item in the receipt.

## Requirements

- Python 3.6 or higher
- Google Cloud SDK
- OpenAI API key
- OpenAI GPT3 Model

## Modules Used

- Flask (A micro web framework written in Python)
- OpenAI API (API for GPT3)
- OS 

This script specifically uses the Flask method 'functions_framework.http' to serve as an http function. 

## How It Works

This program receives JSON input through HTTP, the JSON should contain information about the receipt items. It will then process this information by communicating with OpenAi's GPT3 AI model, which will generate estimates for the calories contained in each item on the receipt. 

The program will return a JSON output where each key represents an item from the receipt and its corresponding value is the estimated calories for that item. Additionally, it will also add a key 'total', the value of which is the sum of all item's calories. 

If any of the items are ambiguous or it fails to estimate calories for any item, it will assign a value of 'unknown' for that item.

## Usage

The main function 'calories_estimates' takes in an HTTP request. The request must be a JSON object with the following structure:

```python
{"input":{"body":{"items":"receipt items"}}}
```

Example:

```python
{"input":{"body":{"items":"steak, burger, fries"}}}
```

## Exceptions 

If an empty, corrupted list items or no list items are provided, the function will return an empty JSON. 

## AI Role

The 'calories_estimates' function leverages OpenAI's GPT3 AI model for providing estimates. It provides information to the model using 'ChatCompletion' method which contains several 'user' and 'system' roles to guide the AI.

## Output

The function will return a JSON output where each key represents an item from the receipt and its corresponding value is the estimated calories for that item.

## Deployment

This function is intended for deployment on Google Cloud as a cloud function, specifically to serve HTTP requests. 

## Important Notes

Please make sure to set the below environment variables in GCP cloud function settings:

- `GCP_PROJECT`: Your Google Cloud Project ID
- `OPENAI_ORGANIZATION`: Your OpenAI organization
- `OPENAI_API`: Your OpenAI API key

The name of the main function to be deployed is 'calories_estimates'. 

## License

[Insert License Here]