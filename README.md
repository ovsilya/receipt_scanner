# Google Cloud Platform (GCP) Workflow Application

This GCP Workflow Application leverages an organized YAML configuration file to orchestrate GCP resources and services. This repository contains structured and efficient code utilized by GCP Workflows for automating complex tasks that span multiple GCP services such as Cloud Storage, Document AI, Cloud Functions, and BigQuery.

## Configuration Structure

The `main` section is the core of the YAML structure, serving as the aggregation point for the workflow's steps. Each step is designated an individual responsibility and implements a unit of work, either through GCP native services or custom-developed functions deployed on Google Cloud Function (GCF).

## Workflow Steps

The `init` step initializes a series of variables, storing extracted entities, ratings, estimates, and generation outputs. Following this, the `log_event` step writes logs for the event object at `INFO` level severity. `check_data_key` evaluates if a `data` key is present in the input event, which predicates further progression of the workflow.

Subsequent control flow is manipulated to ensure accurate processing by the `switch` statement. Absence of the `data` key leads to the execution of `log_missing_data`, logging a `WARNING` level message and consequent termination of the workflow. However, presence of the `data` key triggers the `run_docai` routine.

Within `run_docai`, operations revolve around Document AI functionalities. From the delineated bucket and object, data extraction commences, followed by a succession of HTTP POST requests initiated towards various cloud functions. These requests process the extracted text, with ultimate results being stored in the `entities_extracted` dictionary.

## Parallel Execution

The `parallelStep` section stimulates the simultaneous execution of multiple operations. These include fetching Yelp ratings (`yelp`), parsing time (`time`), estimating caloric intake (`calories`), administering an alcohol check (`alcohol_checker`), and generating an image (`image`). Each operation, comprising of one or more HTTP POST requests to specifically defined cloud functions, outputs results that are preserved in associated variables.

## Final Procedures

Outputs from `run_docai` and `parallelStep` stages are integrated in a `genai_object`. An HTTP POST request sends this constructed object to the `write_to_bqtable` cloud function for persisting it into a predefined GCP BigQuery table. As a housekeeping measure, the `delete_inter_files` step is employed to remove intermediary files from the used GCP bucket.

## Logging 

Should the data key be absent in the input event during any stage of the workflow, the execution falls back to the `log_missing_data` step. A `WARNING` level log, stating `'Data key not found in event'` is issued and the workflow execution is ceased.

This workflow implementation underpins robust orchestration mechanisms for complex tasks encompassing a variety of GCP services and functions. It is a reflection of responsible computing where resources are efficiently consumed and full logging capabilities ensure transparency in execution.