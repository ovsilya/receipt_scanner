# Google Cloud Functions - BigQuery Writer

This python script acts as a Google Cloud function that writes JSON data sent to it into a Google BigQuery (BQ) table. It receives JSON data from a HTTP request, processes the data, and writes the relevant information to the pre-configured BigQuery table. 

This function is useful when there is a need to persist data into a BigQuery table for downstream data analysis or machine learning tasks. 

## Overview of the Code

1. The function `write_to_bq` is invoked to write the data into BigQuery. It takes in the dataset name, table name, and a dictionary of the data to be inserted as parameters. The function uses Google Cloud's BigQuery Python client library to perform the dataset reference, table reference and loading job.

2. The environment variables representing the dataset name and table name used in BigQuery are retrieved using `os.environ.get` function.

3. The BigQuery schema that the function uses to format the JSON data for insertion in the table is defined.

4. The main entry point of the Cloud Function is `write_to_bqtable`, which is a HTTP-triggered function. This function retrieves the request data in JSON format, processes it to fit the BigQuery schema, and then calls `write_to_bq` function to write to BigQuery.

5. Any non-schema fields present in the processed data are eliminated before writing data to BigQuery, thus ensuring that only data that suits our schema enters BigQuery.

6. Appropriate HTTP responses are sent based on whether the persistence to BigQuery was successful or not.

## Configuration

The environment variables `DATASET_NAME` and `TABLE_NAME` should be set to the correct BigQuery dataset and table name where data should be written. If these variables are not set, the Cloud Function will not be able to properly write to BigQuery.

Make sure all the dependencies are installed including the Google Cloud BigQuery client library for Python in the Cloud Function environment. 

## Usage

Deploy this script as a Google Cloud function. This Cloud Function can then receive HTTP requests with JSON body, and subsequently write the data to a specified BigQuery table.

After deploying this function, you can make HTTP requests to the URL of the deployed Google Cloud Function. The request body must be a JSON object with the data you want to write to BigQuery.

A successful response from the function will be a JSON object with a message indicating that the data has been successfully saved to BigQuery. If there is an error, the HTTP response will include details of the error.

For example, a successful response looks like this:

```json
{
  "message": "successfully saved to BQ!"
}
```

Remember to secure your function to ensure that only authorized services can call this function and write data to your BigQuery table.