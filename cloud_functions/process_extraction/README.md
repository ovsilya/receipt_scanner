# Extractor Function Using Google Cloud Document AI

This code is a part of an extraction pipeline that uses [Google Cloud Document AI](https://cloud.google.com/document-ai/docs) to parse the content of documents and extract specific pieces of information. The function uses a Google Cloud Function to process the Document AI extraction output and return it in the required format.

## Code Functionality

The function `process_extraction(request)` is triggered by an HTTP request. This HTTP request is supposed to contain JSON data with the required `destination_uri` where the extraction output will be stored.

When the function is called, it first initiates empty lists for several possible extracted entities like: addresses, date times, item lists, names, prices and total. Then, it prepares a Google Cloud Storage Bucket to save the extracted data.

The function then iteratively goes through all files in the specified Storage Bucket. For each file, it checks if the file is in the supported JSON format. If not, the function skips that file and goes to the next one.

For each JSON file, the file content is retrieved and mapped to a Document Object. The specific extracted entities (addresses, date times, item lists, names, prices and total) are then consolidated from each document entities. 

Finally, the function returns a JSON object containing the combined list of extracted entities as strings. The return format is:

```json
{
    "input_file_name": "the name of the input file",
    "address": "combined extracted address entities as a single string",
    "date_time": "combined extracted date time entities as a single string",
    "items": "combined extracted items entities as a single string",
    "name": "combined extracted name entities as a single string",
    "prices": "combined extracted price entities as a single string",
    "total": "combined extracted total entities as a single string"
}
```

## Usage

The `process_extraction(request)` function is designed to be deployed as a Cloud Function. The function is triggered by a HTTP request containing the required `destination_uri`. The `destination_uri` should point to the Google Cloud Storage bucket where the output from Document AI extraction is stored.

**Note:** This function is dependent on several environments including Google Cloud Storage and Document AI from Google Cloud. Appropriate authentication and environment setup are required to run this function.