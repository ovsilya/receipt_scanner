# Time Parsing

This code is a Google Cloud Function that is primarily useful for parsing date and time from a piece of text. It makes use of OpenAI's gpt-4 model for natural language processing and understanding.

Once the function receives a JSON request containing date and time in text format, it processes this information and extracts the following values:
  - Time in '%H:%M:%S' format,
  - Date in '%Y-%m-%d' format,
  - Day of the week,
  - Day period like Breakfast, Lunch, Dinner.

If multiple times are detected in the text, the function calculates the average time and uses that time as the result. If no values are detected, it is mentioned as 'none' in the output. The results are returned in the JSON format.

To detect the day period, the function follows these rules: 
  - Breakfast is from the earliest possible time until 11:30am
  - Lunch is from 11:30am to 5:00pm
  - Dinner is from 5:00pm till the latest possible time
  
The results are returned in JSON where the keys are time, date, day_of_week, day_period with their respective values.


## Requirements
This function primarily makes use of the openai and functions_framework libraries from Python. It fetches the GCP_PROJECT, OPENAI_ORGANIZATION and OPENAI_API variables from the OS environment in order to make use of Google Cloud and OpenAI.


## Usage:
This function can be called with a POST method, providing the request's body with a 'input' key and then 'body' which contains 'date_time'.

```python
payload = {
   "input": {
      "body": {
          "date_time": "Sunday, 12 December 2021, 7:30pm"
      }
   }
}

response = requests.post('https://<Cloud Function URL>', json=payload)

response.json()
```

The response will contain a newly created JSON, indicating the relevant time details extracted from the given text:

```json
{
  "date_time_analysis": {
    "time": "19:30:00",
    "date": "2021-12-12",
    "day_of_week": "Sunday",
    "day_period": "Dinner"
  }
}
```