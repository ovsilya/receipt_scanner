import re
import os
import json
from google.cloud import bigquery
from google.cloud import storage
import functions_framework

#Reading environment variables
gcs_output_uri = os.environ.get('GCS_OUTPUT_URI')
gcs_output_uri_prefix = os.environ.get('GCS_OUTPUT_URI_PREFIX')
gcs_archive_bucket_name = os.environ.get('GCS_ARCHIVE_URI')

destination_uri = f"{gcs_output_uri}/{gcs_output_uri_prefix}/"
storage_client = storage.Client()

@functions_framework.http
def delete_inter_files(request):

    request_json = json.loads(request.get_data().decode('utf-8'))
    bucket_name = request_json['input']['bucket']
    object_name = request_json['input']['object']

    # split the destination URI into the first and second parts: gs://receipt_scanner_output/processed/
    match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)
  
    #Get a pointer to the Storage Bucket where the output will be placed
    bucket = storage_client.get_bucket(output_bucket)

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