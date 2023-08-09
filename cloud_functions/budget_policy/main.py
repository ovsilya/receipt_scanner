import os
import re
import json
import openai
import tempfile
import subprocess
import functions_framework
from google.cloud import storage
import google.cloud.storage as gcs
from flask import jsonify, request

project_id = os.environ.get('GCP_PROJECT')
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API')
bucket_name = "receipt_scanner_archived"
file_name = "company_meal_expense_policy.txt"

def load_policy_doc(bucket_name, file_name):
    # Instantiate a storage client
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_text()
        return content
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def extract_numbers_and_find_max(input_string):
    # Search for numbers in the input_string
    numbers = re.findall(r'-?\d+\.?\d*', input_string)
    
    # Convert each number to its corresponding float or integer
    cleaned_numbers = [int(num) if '.' not in num else float(num) for num in numbers]

    # Check if the list is empty, and return None if it is
    if not cleaned_numbers:
        return None

    # Find the maximum number and return it
    max_number = max(cleaned_numbers)
    return max_number

def extract_policy_numbers(txt_content):
    
    Response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Return JSON only, no descriptions."},
            {"role": "user", "content": "This is a budget policy document. Extract budget values from the provided text based on seniority level in the company:"},
            {"role": "user", "content": f"Text: {txt_content}"},
			{"role": "assistant", "content": "Extract values and return them in JSON format with the keys: breakfast_budget, lunch_budget, dinner_budget."},
            {"role": "assistant", "content": "if no/irrelevant/corrupted values are detected, fill the key values with 'no_values_detected' phrase."},
            {"role": "assistant", "content": "Mandatory keys for seniority level: Junior, Senior, Executive"},
            {"role": "assistant", "content": "do not include dollar sign or any other currency symbols"}
        ]
    )
    choices = Response['choices'][0]['message']['content']
    return choices

def str_to_dict(json_string):
    # Load the JSON string into a Python dictionary
    dictionary = json.loads(json_string)
    return dictionary

def validate_budget(max_total, parsed_time, alcohol_classif_class, budget_policy_dict):
    employee_level = "Senior"
    alcohol_class = alcohol_classif_class

    breakfast_budget = float(budget_policy_dict[employee_level]["breakfast_budget"])
    lunch_budget = float(budget_policy_dict[employee_level]["lunch_budget"])
    dinner_budget = float(budget_policy_dict[employee_level]["dinner_budget"])

    if max_total is None or max_total == 0:
        return "Invalid total cost value. Please provide a non-zero value."

    if "Breakfast" in parsed_time["day_period"]:
        if max_total <= breakfast_budget:
            return "Breakfast is in budget!"
        else:
            return "Breakfast is NOT in budget :("
    elif "Lunch" in parsed_time["day_period"]:
        if max_total <= lunch_budget:
            return "Lunch is in budget!"
        else:
            return "Lunch is NOT in budget :("
    elif "Dinner" in parsed_time["day_period"]:
        if max_total <= dinner_budget:
            return "Dinner is in budget!"
        else:
            return "Dinner is NOT in budget :("
    else:
        return "Meal time is not detected --> cannot check the budget policy!"


@functions_framework.http
def budget_policy(request):

    # get company's budget policy numbers from the text file:
    try:
        content = load_policy_doc(bucket_name, file_name)
        budget_policy_dict = str_to_dict(extract_policy_numbers(content))
        request_json = request.get_json()
        
        # read input variables: 
            # total (str), 
            # parsed_time (str), 
            # alcohol class (yes, no, unknown)
        
        total = request_json["input"]["entities_extracted_output"]["body"]["total"]
        parsed_time = json.loads(request_json["input"]["time_parsing_output"]["body"]["date_time_analysis"])
        alcohol_classif_class = request_json["input"]["alcohol_check_output"]["body"]["alcohol_check"]

        budget_message = validate_budget(extract_numbers_and_find_max(total), parsed_time, alcohol_classif_class,budget_policy_dict)
        result = {"budget_message": budget_message}
        print('budget_message', budget_message)
        return jsonify(result)

    except Exception as e:
        result = {"budget_message": f"An error occurred: {str(e)}"}
        print(f"An error occurred: {str(e)}")
        return jsonify(result)

    