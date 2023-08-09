# Receipt Scanner: Company Meal Budget Check

This project is part of a receipt scanning tool that checks if an employee's meal expense is within the company's budget policy. The operation specifically explores the company budget for meals based on the receipt details and the company's meal policy. This operation is implemented as a Google Cloud Function.

The script in this repository does the following:

1. It retrieves a company's meal budget policy text file from a Google Cloud Storage (GCS) bucket.

2. It uses OpenAI's gpt-4 model to parse through the budget policy document and extract the budget values for different meal times based on the seniority level in the company.

3. It receives the total meal expense, the meal time, and alcohol check result as input from a JSON payload.

4. It uses the parsed information to determine whether the employee's meal expense is within the company's budget policy or not.

## Functions

The script comprises the following functions:

1. `load_policy_doc(bucket_name, file_name)`: This function fetches the company's meal budget policy text file from the GCS bucket.

2. `extract_numbers_and_find_max(input_string)`: This function extracts all numbers from a given string and returns the maximum number.

3. `extract_policy_numbers(txt_content)`: This function uses OpenAI's gpt-4 model to parse the budget policy document and extract budget values based on seniority level.

4. `str_to_dict(json_string)`: This function accepts a JSON string and converts it to a dictionary.

5. `validate_budget(max_total, parsed_time, alcohol_classif_class, budget_policy_dict)`: This validates whether the meal is within the company's budget policy or not.

6. Google Cloud Function `budget_policy(request)`: This is the main function that couples all the above functions and performs the budget check. It returns a JSON response for the client.

## How to Test the Function

This Google Cloud Function can be tested by sending a POST request to the deployed function URL with a JSON payload structured as follows:

```json
{
    "input": {
        "entities_extracted_output": {
            "body": {
                "total": "<receipt_total>"
            }
        },
        "time_parsing_output": {
            "body": {
                "date_time_analysis": "<meal_time>"
            }
        },
        "alcohol_check_output": {
            "body": {
                "alcohol_check": "<yes/no>"
            }
        }
    }
}
```

`<receipt_total>`: The total amount in the receipt.

`<meal_time>`: The mealtime (breakfast, lunch, dinner).

`<yes/no>`: Whether alcohol was purchased or not.
