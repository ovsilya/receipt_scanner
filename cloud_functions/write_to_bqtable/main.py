import os
import json
from google.cloud import bigquery
import functions_framework
from flask import jsonify, request

dataset_name = os.environ.get('DATASET_NAME')
table_name = os.environ.get('TABLE_NAME')

# Create a dict to create the schema and to avoid BigQuery load job fails due to inknown fields
bq_schema={
    "address":"STRING",  
    "date_time":"STRING", 
    "items":"STRING", 
    "name":"STRING",
    "prices":"STRING",
    "total":"STRING",
    "yelp_rating":"STRING",
    "time_parsing":"STRING",
    "calories_estimates":"STRING",
    "image_url":"STRING",
    "alcohol_check":"STRING",
    "budget_policy":"STRING"
}
bq_load_schema=[]

for key,value in bq_schema.items():
    bq_load_schema.append(bigquery.SchemaField(key,value))
bq_client = bigquery.Client()

def write_to_bq(dataset_name, table_name, entities_extracted_dict):
 
    dataset_ref = bq_client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    test_dict=entities_extracted_dict.copy()
    for key,value in test_dict.items():
      if key not in bq_schema:
          print ('Deleting key not in schema: ' + key)
          del entities_extracted_dict[key]

    row_to_insert =[]
    row_to_insert.append(entities_extracted_dict)
 
    json_data = json.dumps(row_to_insert, sort_keys=False)
    #Convert to a JSON Object
    json_object = json.loads(json_data)
   
    job_config = bigquery.LoadJobConfig(schema=bq_load_schema)
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
 
    job = bq_client.load_table_from_json(json_object, table_ref, job_config=job_config)
    error = job.result()  # Waits for table load to complete.
    print(error)


@functions_framework.http
def write_to_bqtable(request):

    request_json = request.get_json()
    print("request_json: ", request_json)
    # entities_extracted = request_json["input"]["entities_extracted_output"]["body"]
    address = request_json["input"]["entities_extracted_output"]["body"]['address']
    date_time = request_json["input"]["entities_extracted_output"]["body"]['date_time']
    items = request_json["input"]["entities_extracted_output"]["body"]['items']
    name = request_json["input"]["entities_extracted_output"]["body"]['name']
    prices = request_json["input"]["entities_extracted_output"]["body"]['prices']
    total = request_json["input"]["entities_extracted_output"]["body"]['total']

    calories = request_json["input"]["calories_estimates_output"]["body"]["calories"]
    image_url = request_json["input"]["image_gen_output"]["body"]["image_url"]
    date_time_analysis = request_json["input"]["time_parsing_output"]["body"]["date_time_analysis"]
    rating = request_json["input"]["yelp_rating_output"]["body"]["rating"]

    alcohol = request_json["input"]["alcohol_checker_output"]["body"]["alcohol_check"]
    budget = request_json["input"]["budget_policy_output"]["body"]["budget_message"]

    entities_extracted_dict = {}
    entities_extracted_dict['address'] = address
    entities_extracted_dict['date_time'] = date_time
    entities_extracted_dict['items'] = items
    entities_extracted_dict['name'] = name
    entities_extracted_dict['prices'] = prices
    entities_extracted_dict['total'] = total

    entities_extracted_dict['calories_estimates'] = calories
    entities_extracted_dict['image_url'] = image_url
    entities_extracted_dict['time_parsing'] = date_time_analysis
    entities_extracted_dict['yelp_rating'] = rating
    entities_extracted_dict['alcohol_check'] = alcohol
    entities_extracted_dict['budget_policy'] = budget


    print('entities_extracted_dict', entities_extracted_dict)
    # #Write the entities to BQ
    print('Writing to BQ')
    write_to_bq(dataset_name, table_name, entities_extracted_dict)

    response_dict = {"message": "successfully saved to BQ!"}
    return jsonify(response_dict)