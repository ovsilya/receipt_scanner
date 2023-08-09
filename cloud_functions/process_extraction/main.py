import re
import os
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage
import functions_framework
from flask import jsonify, request
 
storage_client = storage.Client()

@functions_framework.http
def process_extraction(request):

    request_json = request.get_json()
    destination_uri = request_json['input']['body']['destination_uri']

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
  
            #################################################################################
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
            
    return jsonify(entities_extracted_dict)