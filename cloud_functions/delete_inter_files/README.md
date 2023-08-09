# Google Cloud Function to Delete Intermediate Files after Document AI Processing 

This Python script is a Google Cloud Function that is designed to clean up (delete) intermediate files after the files have been parsed by the Document AI (Doc AI) tool. 

The function also moves the input file to an archive bucket once Doc AI processing is finished. Further, it deletes the file from the input force to fully clean up the processing environment.

## How It Works

The function `delete_inter_files` is an HTTP triggered function that takes in a request which includes the details of the input file (bucket and object name).

The function performs the following steps:

1. The function reads a JSON message from the HTTP request. This message includes the details of the file (i.e., the name of the bucket where the file is stored and the object name of the file).

2. The function reads environment variables to get the details of the output storage bucket, the output storage prefix, and the archive bucket where the input files should be moved after processing by Doc AI.

3. The function matches the `destination_uri` to get the main output bucket and prefix for all output blobs.

4. Then, the function gets a pointer to the Storage Bucket where the output files are placed.

5. It then lists all blobs in this output bucket with the prefix `gcs_output_uri_prefix` and deletes them one by one. This removes all the intermediate files created by the Doc AI Parser.

6. The function then copies the input processed file to the archive bucket, and deletes the source file from the input bucket.

## Usage

This Google Cloud Function should be deployed on the same Google Cloud project where the Document AI Parser is running. This will ensure that the function has the appropriate permissions to manage the Google Cloud Storage bucket where the intermediate files are stored.

The function should be triggered after the Document AI Parser has completely processed a file. This can be achieved by setting an event trigger for the function for the `onChange` event of the output Storage bucket.

This function helps in managing your Google Cloud Storage by cleaning up unnecessary files and freeing up storage. It also archives the processed files for future reference.