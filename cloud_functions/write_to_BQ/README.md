# Receipt Scanner - Extraction, Analysis and Dump
This script is designed to solve the problem of automated receipt scanning. It accomplishes parsing receipts, extracting useful information from the receipts, saving and analyzing the data. The script is written in Python and makes use of a variety of APIs and services, such as Google's Document AI and BigQuery service.

#### Features:
- Extracts data from receipts.
- Analyses the extracted data.
- Processes intermediate files created by the Document AI Parser.
- Dumps parsed and analyzed data into BigQuery.
- Archive original receipts files.

## How It Works

1. The script first sets up and reads environmental variables.
2. After setting up, it fetches input receipt files.
3. It then uses Google's Document AI to parse and extract information from the receipts.
4. The extracted information includes address, date, items, name, price and total.
5. All the extracted information is read into a dictionary ready to be written to BigQuery.
6. Errors and types which do not match the desired schema are processed and excluded from what is written to BigQuery.
7. The successfully read data is then dumped into BigQuery.
8. Once the dump is successful, all intermediate files that were created by Document AI Parser are deleted. This is done to save space and resources.
9. Original receipts files are archived and the source files deleted.

## Usage
To use this script, deploy it on any server and pass request data in the format:

```python
{
    'input': 
    {
        'bucket': 'source_bucket_name',
        'object': 'object_name',
    }
}
```
The script will fetch, extract, process and dump accordingly.

## Prerequisites
The services and libraries needed for this script include:
- Google Cloud BigQuery
- Google Document AI (documentai_v1beta3)
- Google Cloud Storage
- os
- json
- re
- base64
- datetime
- functions_framework

Ensure that the necessary APIs are enabled on your Google Cloud Console and the required libraries installed.

## Note
This is just a rough guide on what the script does. Most of the details and intricacies on how the script is structured and how it does its job is found within the comments in the code. If you wish to understand it better, please go through the code, starting from the top.

## Contribution
For any contribution, feel free to make a pull request. Would love help in making it better.