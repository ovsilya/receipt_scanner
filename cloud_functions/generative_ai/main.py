import os
import functions_framework
import os
import openai
from google.cloud import bigquery
from prettytable import PrettyTable

#Reading environment variables
# gcs_output_uri_prefix = os.environ.get('GCS_OUTPUT_URI_PREFIX')
project_id = os.environ.get('GCP_PROJECT')
# location = os.environ.get('PARSER_LOCATION')
# processor_id = os.environ.get('PROCESSOR_ID')
# # geocode_request_topicname = os.environ.get('GEOCODE_REQUEST_TOPICNAME')
# timeout = int(os.environ.get('TIMEOUT'))

client = bigquery.Client(project=project_id)
openai.organization = "org-onLKDyqeEBuoi92Nt0TTKGth"
openai.api_key = "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"

@functions_framework.http
def generative_ai(request):
  
  # Set up the query to fetch the 50th row from the table
  query = (
      f"SELECT * FROM `iot-poc-354821.receipt_scanner.doc_ai_extracted_entities` "
      f"LIMIT 1 OFFSET 65"
  )
  # Run the query and fetch the results
  result = client.query(query).result()
  # Create a PrettyTable object to store the row data
  table = PrettyTable()
  # Add the field names to the table
  table.field_names = [field.name for field in result.schema]
  # Add the data for the 50th row to the table
  for row in result:
      table.add_row(list(row.values()))
      address = row[0]
      date_time = row[1]
      items = row[2]
      name = row[3]
      prices = row[4]
      total = row[5]

  # Create a dictionary object with the variables as keys and their corresponding string values
  result = {
      "address": address,
      "date_time": date_time,
      "items": items,
      "name": name,
      "prices": prices,
      "total": total
  }
  # Return the dictionary as a JSON-encoded string
  return jsonify(result)