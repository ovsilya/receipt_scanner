import base64
import re
import os
import json
from datetime import datetime
from google.cloud import bigquery
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage
import functions_framework
 
#Reading environment variables
gcs_output_uri_prefix = os.environ.get('GCS_OUTPUT_URI_PREFIX')
project_id = os.environ.get('GCP_PROJECT')

# Setting variables
gcs_output_uri = f"gs://receipt_scanner_output"
gcs_archive_bucket_name = f"receipt_scanner_archived"
destination_uri = f"{gcs_output_uri}/{gcs_output_uri_prefix}/"

dataset_name = 'receipt_scanner'
table_name = 'doc_ai_extracted_entities'

# Create a dict to create the schema and to avoid BigQuery load job fails due to inknown fields
bq_schema={
    "address":"STRING",  
    "date_time":"STRING", 
    "items":"STRING", 
    "name":"STRING",
    "prices":"STRING",
    "total":"STRING"
}
bq_load_schema=[]
for key,value in bq_schema.items():
    bq_load_schema.append(bigquery.SchemaField(key,value))
bq_client = bigquery.Client()
storage_client = storage.Client()

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

def get_text(doc_element: dict, document: dict):
    # Document AI identifies form fields by their offsets in document text. This function converts offsets to text snippets.
    response = ''
    # If a text segment spans several lines, it will be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

@functions_framework.http
def write_extracted(request):

    request_json = json.loads(request.get_data().decode('utf-8'))
    print(request_json)
    bucket_name = request_json['input']['bucket']
    object_name = request_json['input']['object']
    
    addresses = []
    date_times = []
    items_list = []
    names = []
    pirces_list = []
    total = []

    ################# Prepare a place to save extracted data ########################
    # split the destination URI into the first and second parts: gs://receipt_scanner_output/processed/
    match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)
  
    #Get a pointer to the Storage Bucket where the output will be placed
    bucket = storage_client.get_bucket(output_bucket)
    
    # Get List of Document Objects from the Output Bucket #processed
    blob_list = list(bucket.list_blobs(prefix=prefix))
    # print('Output files:')

    for i, blob in enumerate(blob_list):

        print("i = =====================", i)
        # Download the contents of this blob as a bytes object.
        if '.json' not in blob.name:
            print('blob name ' + blob.name)
            print(f"skipping non-supported file type {blob.name}")
        else:
            #Setting the output file name based on the input file name
            print('Fetching from ' + blob.name)
            start = blob.name.rfind("/") + 1
            end = blob.name.rfind(".") + 1           
            input_filename = blob.name[start:end:] + 'gif'
            print('input_filename ' + input_filename)
  
            # Getting ready to read the output of the parsed document - setting up "document"
            # Download JSON File as bytes object and convert to Document Object
            blob_as_bytes = blob.download_as_bytes()
            document = documentai.types.Document.from_json(blob_as_bytes)
  
            ########################### Writing into BigQuery from .json file #####################
            #Reading all entities into a dictionary to write into a BQ table
            entities_extracted_dict = {}
            entities_extracted_dict['input_file_name'] = input_filename
            
            for entity in document.entities:   
                type_ = entity.type_
                raw_value = entity.mention_text
                if type_.strip().lower() == 'address':
                    addresses.append(raw_value)          
                if type_.strip().lower() == 'date_time':
                    date_times.append(raw_value)
                if type_.strip().lower() == 'items':
                    items_list.append(raw_value)
                if type_.strip().lower() == 'name':
                    names.append(raw_value)
                if type_.strip().lower() == 'prices':
                    pirces_list.append(raw_value)
                if type_.strip().lower() == 'total':
                    total.append(raw_value)
            
            addresses_str = '\n'.join(addresses)
            date_times_str = '\n'.join(date_times)
            items_list_str = '\n'.join(items_list)
            names_str = '\n'.join(names)
            pirces_list_str = '\n'.join(pirces_list)
            total_str = '\n'.join(total)
            
            entities_extracted_dict['address'] = addresses_str
            entities_extracted_dict['date_time'] = date_times_str
            entities_extracted_dict['items'] = items_list_str
            entities_extracted_dict['name'] = names_str
            entities_extracted_dict['prices'] = pirces_list_str
            entities_extracted_dict['total'] = total_str

            print(entities_extracted_dict)
            print('Writing to BQ')
            #Write the entities to BQ
            write_to_bq(dataset_name, table_name, entities_extracted_dict)
            
    #Deleting the intermediate files created by the Doc AI Parser
    blobs = bucket.list_blobs(prefix=gcs_output_uri_prefix) #processed
    for blob in blobs:
        print('Deleting blob: ' + blob.name)
        blob.delete()
    
    # #Copy input file to archive bucket
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(object_name)
    destination_bucket = storage_client.bucket(gcs_archive_bucket_name)
    blob_copy = source_bucket.copy_blob(source_blob, destination_bucket, object_name)
    
    #delete from the input folder
    source_blob.delete()

    response_dict = {"message": "successfully saved to BQ!"}
    return (json.dumps(response_dict), 200, {'Content-Type': 'application/json'})
