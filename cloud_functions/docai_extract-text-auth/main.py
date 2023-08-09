import os
import json
from google.cloud import documentai_v1beta3 as documentai
import functions_framework
from flask import jsonify, request

#Reading environment variables
project_id = os.environ.get('GCP_PROJECT')
location = os.environ.get('PARSER_LOCATION')
processor_id = os.environ.get('PROCESSOR_ID')
gcs_output_uri = os.environ.get('GCS_OUTPUT_URI')
gcs_output_uri_prefix = os.environ.get('GCS_OUTPUT_URI_PREFIX') #processed/
timeout = int(os.environ.get('TIMEOUT'))

destination_uri = f"{gcs_output_uri}/{gcs_output_uri_prefix}/" # gs://receipt_scanner_output/processed/
name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
print('destination_uri: ', destination_uri)

docai_client = documentai.DocumentProcessorServiceClient()

@functions_framework.http
def docai_process(request):
    
    request_json = json.loads(request.get_data().decode('utf-8'))

    bucket = request_json['input']['bucket']
    object_name = request_json['input']['object']
    event_type = request_json['input']['contenttype']

    #file name to be processed with DocAI
    gcs_input_uri = 'gs://' + bucket + '/' + object_name

    if(event_type == 'image/gif' or event_type == 'application/pdf' or event_type == 'image/tiff' ):
        
        ######################## DocAI Part #############################
        input_config = documentai.types.document_processor_service.BatchProcessRequest.BatchInputConfig(gcs_source=gcs_input_uri, mime_type=event_type)
        output_config = documentai.types.document_processor_service.BatchProcessRequest.BatchOutputConfig(gcs_destination=destination_uri)
        request_ai = documentai.types.document_processor_service.BatchProcessRequest(
            name=name,
            input_configs=[input_config],
            output_config=output_config,
        )
        operation = docai_client.batch_process_documents(request_ai)
        # Wait for the operation to finish
        operation.result(timeout=timeout)
        
        response_dict = {"destination_uri": destination_uri}
        print("Processing is complete!")
        return jsonify(response_dict)
              
    else:
        print('Cannot parse the file type')