# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised
import json
import csv
from io import BytesIO, StringIO, TextIOWrapper
import os
import time
import logging
import uuid
import datetime
from typing import List, Dict, Any, Union, Optional, Tuple, Set
from google.api_core.exceptions import NotFound
from google.cloud import  bigquery
from google.cloud.storage import Client as GCSClient
from ipulse_shared_base_ftredge import (DuplicationHandling,
                                        DuplicationHandlingStatus,
                                        MatchConditionType,
                                        DataSourceType,
                                        LogLevel,
                                        DataActionType,
                                        log_debug, log_info, log_warning, log_error)
from ipulse_shared_data_eng_ftredge import (ContextLog,
                                            Pipelinemon)
############################################################################
##################### GOOGLE CLOUD STORAGE ##################################
############################################################################

def read_json_from_gcs(storage_client:GCSClient, bucket_name:str, file_name:str, logger=None,print_out=False):
    """ Helper function to read a JSON or CSV file from Google Cloud Storage """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        return data
    except NotFound:
        log_warning(msg=f"Warning: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except json.JSONDecodeError:
        log_error(msg=f"Error: The file {file_name} could not be decoded as JSON.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", exc_info=True, logger=logger, print_out=print_out)
        return None

def  read_file_from_gcs_extended(storage_client:GCSClient, bucket_name:str, file_path:str, file_extension:DataSourceType=None, pipelinemon:Pipelinemon=None, logger=None, print_out=False):
    """Helper function to read a JSON or CSV file from Google Cloud Storage with optional Pipelinemon monitoring."""
    try:
        # Determine the file extension
        base_file_name, ext = os.path.splitext(file_path)  # ext includes the dot (.) if present
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = file_extension.value
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = file_extension.value
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")


        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        # Check if the blob (file) exists
        if not blob.exists():
            log_warning(msg=f"Warning: The file {file_path} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED,
                                               subject=file_path,
                                               description=f"File not found in GCS: {file_path} in bucket {bucket_name}"))
            return None

        # Download the file content
        data_string = blob.download_as_text()

        # Check if the file is empty , better alternative to if blob.size == 0 as blob.size might not be populated or accurate without reloading the blob metadata
        if not data_string: 
            msg = f"File {file_path} is empty in bucket {bucket_name}"
            log_warning(msg, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED,
                                               subject=f"blob {file_path} in {bucket_name}",
                                               description="Empty file"))
            return None

        # Initialize data variable
        data = None

        # Parse the data based on file extension
        if ext == ".json":
            try:
                data = json.loads(data_string)
            except json.JSONDecodeError as e:
                msg = f"Error decoding JSON from GCS: {file_path} in bucket {bucket_name}: {e}"
                log_error(msg=msg, logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_log(ContextLog(LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED,
                                                   subject=file_path, description=msg))
                return None
        elif ext == ".csv":
            try:
                data_io = StringIO(data_string)
                reader = csv.DictReader(data_io)
                data = list(reader)
            except csv.Error as e:
                msg = f"Error reading CSV from GCS: {file_path} in bucket {bucket_name}: {e}"
                log_error(msg=msg, logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_log(ContextLog(LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED,
                                                   subject=file_path, description=msg))
                return None
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        # Log successful read
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.INFO_READ_FILE_FROM_CLOUD_STORAGE_COMPLETE,
                                           subject=f"blob {file_path} in {bucket_name}",
                                           description="File read from GCS"))
        return data

    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        log_error(msg=msg, exc_info=True, logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED, e=e))
        return None
    


    

def read_csv_from_gcs(bucket_name:str, file_name:str, storage_client:GCSClient, logger=None, print_out=False):
    """ Helper function to read a CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data_file = StringIO(data_string)
        reader = csv.DictReader(data_file)
        return list(reader)
    except NotFound:
        log_warning(msg=f"Error: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except csv.Error:
        log_error(msg=f"Error: The file {file_name} could not be read as CSV.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", logger=logger, print_out=print_out, exc_info=True)
        return None



def write_file_to_gcs_extended(storage_client: GCSClient,
                               data: dict | list | str, bucket_name: str, file_path: str,
                                duplication_handling: DuplicationHandling,
                                duplication_match_condition_type: MatchConditionType,
                                duplication_match_condition: str = "",
                                max_retries: int = 2,
                                max_deletable_files: int = 1,
                                file_extension:DataSourceType =None,
                                logger=None, print_out=False, raise_e=False, pipelinemon: Pipelinemon = None):

    """Saves data to Google Cloud Storage with optional Pipelinemon monitoring.

    Handles duplication with strategies: OVERWRITE, INCREMENT, SKIP, or RAISE_ERROR.

    !! As of now only supporting STRING duplication_match_condition !!
    """

    max_deletable_files_allowed = 3
    cloud_storage_ref = DataSourceType.GCS.value

    # GCS-related metadata
    saved_to_path = None
    matched_duplicates_count = 0
    matched_duplicates_deleted = []
    duplication_handling_status = None
    error_during_operation = None
    data_str = None
    data_bytes = None
    content_type = None

    response = {
        "saved_to_path": saved_to_path,
        "matched_duplicates_count": matched_duplicates_count,
        "matched_duplicates_deleted": matched_duplicates_deleted,
        "duplication_handling_status": duplication_handling_status,
        "duplication_match_condition_type": duplication_match_condition_type.value,
        "duplication_match_condition": duplication_match_condition,
        "error_during_operation": error_during_operation
    }

    supported_match_condition_types = [MatchConditionType.EXACT, MatchConditionType.PREFIX]
    supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

    try:
        if max_deletable_files > max_deletable_files_allowed:
            raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
        if duplication_handling not in supported_duplication_handling:
            msg = f"Error: Duplication handling not supported. Supported types: {[dh.value for dh in supported_duplication_handling]}"
            raise ValueError(msg)
        if duplication_match_condition_type not in supported_match_condition_types:
            msg = f"Error: Match condition type not supported. Supported types: {[mct.value for mct in supported_match_condition_types]}"
            raise ValueError(msg)
        elif duplication_match_condition_type != MatchConditionType.EXACT and not duplication_match_condition:
            msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type.value}"
            raise ValueError(msg)

        # Determin extension
        base_file_name, ext = os.path.splitext(file_path) ## ext is the file extension with the dot (.) included
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = file_extension.value
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = file_extension.value
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")

        if ext == '.json':
            if isinstance(data, (list, dict)):
                data_str = json.dumps(data, indent=2)
            else:
                data_str = data  # Assuming data is already a JSON-formatted string
            data_bytes = data_str.encode('utf-8')  # Encode the string to UTF-8 bytes
            content_type = 'application/json'
        elif ext == '.csv':
            # Convert data to CSV
            if isinstance(data, (list, dict)):
                # output = StringIO()
                output_bytes = BytesIO()
                output_text = TextIOWrapper(output_bytes, encoding='utf-8', newline='\n')
                if isinstance(data, dict):
                    # Convert dict to list of dicts with a single item
                    data = [data]
                # Assuming data is a list of dicts
                if len(data) == 0:
                    raise ValueError("Cannot write empty data to CSV.")
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output_text, fieldnames=fieldnames,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n') # Add quoting and line terminator
                writer.writeheader()
                writer.writerows(data)
                output_text.flush()
                output_bytes.seek(0)
                data_bytes = output_bytes.getvalue()
                # Remove any trailing newlines
                data_bytes = data_bytes.rstrip(b'\n')
            else:
                data_bytes = data.encode('utf-8')  # Assuming data is already a CSV-formatted string
            # print(data_bytes.decode('utf-8'))
            content_type = 'text/csv'
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        increment = 0
        attempts = 0
        success = False

        # Check for existing files based on duplication_match_condition_type
        files_matched_on_condition = []
        bucket = storage_client.bucket(bucket_name)
        if duplication_match_condition_type == MatchConditionType.PREFIX:
            files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
        elif duplication_match_condition_type == MatchConditionType.EXACT:
            duplication_match_condition = file_path if not duplication_match_condition else duplication_match_condition
            if bucket.blob(duplication_match_condition).exists():
                files_matched_on_condition = [bucket.blob(file_path)]

        matched_duplicates_count = len(files_matched_on_condition)
        response["matched_duplicates_count"] = matched_duplicates_count

        # Handle duplication based on duplication_handling
        if matched_duplicates_count:
            log_msg = f"Duplicate FOUND, matched_duplicates_count: {matched_duplicates_count}"
            if pipelinemon:
                pipelinemon.add_log(ContextLog(LogLevel.NOTICE_FILE_IN_CLOUD_STORAGE_ALREADY_EXISTS, subject="duplicate_found", description=log_msg))
            log_info(log_msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True

            if duplication_handling == DuplicationHandling.RAISE_ERROR:
                raise FileExistsError("File(s) matching the condition already exist.")

            if duplication_handling == DuplicationHandling.SKIP:
                response["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
                log_msg = f"SKIPPING Write to GCS, response: {response}"
                log_info(log_msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True
                return response

            if duplication_handling == DuplicationHandling.OVERWRITE:
                if matched_duplicates_count > max_deletable_files:
                    raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

                for blob in files_matched_on_condition:
                    cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
                    blob.delete()
                    matched_duplicates_deleted.append(cloud_storage_path_to_delete)
                    log_msg = f"File deleted as part of overwrite: {cloud_storage_path_to_delete}"
                    if pipelinemon:
                        pipelinemon.add_system_impacted(f"delete: {cloud_storage_ref}_bucket_file: {cloud_storage_path_to_delete}")
                        pipelinemon.add_log(ContextLog(LogLevel.ACTION_DELETE_IN_CLOUD_STORAGE_COMPLETE, subject="delete_duplicate", description=log_msg))
                    log_info(log_msg, logger=logger, print_out=print_out)

                response["matched_duplicates_deleted"] = matched_duplicates_deleted
                response["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value

            elif duplication_handling == DuplicationHandling.INCREMENT:
                while bucket.blob(file_path).exists():
                    increment += 1
                    file_path = f"{base_file_name}_v{increment}{ext}"
                saved_to_path = f"gs://{bucket_name}/{file_path}"
                response["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value
                log_msg = "INCREMENTING as Duplicate FOUND"
                log_info(log_msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True

        # GCS Upload
        saved_to_path = f"gs://{bucket_name}/{file_path}"
        while attempts < max_retries and not success:
            try:
                blob = bucket.blob(file_path)
                blob.upload_from_string(data_bytes, content_type=content_type)
                log_msg = f"File uploaded to GCS: {saved_to_path}"
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"upload: {cloud_storage_ref}_bucket_file: {saved_to_path}")
                    pipelinemon.add_log(ContextLog(LogLevel.ACTION_WRITE_IN_CLOUD_STORAGE_COMPLETE, subject="file_upload", description=log_msg))
                log_info(log_msg, logger=logger, print_out=print_out)
                success = True
            except Exception as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(2 ** attempts)
                else:
                    raise e

    except Exception as e:
        error_during_operation = f"Error occurred while writing file to GCS; Error details: {type(e).__name__} - {str(e)}"
        response["error_during_operation"] = error_during_operation
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_EXCEPTION, e=e, description=f"response: {response}"))
        log_error(response, logger=logger, print_out=print_out)
        if raise_e:
            raise e

    response["saved_to_path"] = saved_to_path if success else None
    return response



# def write_json_to_gcs_extended(storage_client: GCSClient, data: dict | list | str, bucket_name: str, file_name: str,
#                                                 duplication_handling_enum: DuplicationHandling, duplication_match_condition_type_enum: MatchConditionType,
#                                                 duplication_match_condition: str = "", max_retries: int = 2, max_deletable_files: int = 1,
#                                                 logger=None, print_out=False, raise_e=False, pipelinemon: Pipelinemon = None):

#     """Saves data to Google Cloud Storage with optional Pipelinemon monitoring.

#     Handles duplication with strategies: OVERWRITE, INCREMENT, SKIP, or RAISE_ERROR.

#     !! As of now only supporting STRING duplication_match_condition !!
#     """

#     max_deletable_files_allowed = 3
#     cloud_storage_ref=DataSourceType.GCS.value

#     # GCS-related metadata
#     saved_to_path = None
#     matched_duplicates_count = 0
#     matched_duplicates_deleted = []
#     duplication_handling_status = None
#     error_during_operation = None

#     response = {
#         "saved_to_path": saved_to_path,
#         "matched_duplicates_count": matched_duplicates_count,
#         "matched_duplicates_deleted": matched_duplicates_deleted,
#         "duplication_handling_status": duplication_handling_status,
#         "duplication_match_condition_type": duplication_match_condition_type_enum.value,
#         "duplication_match_condition": duplication_match_condition,
#         "error_during_operation": error_during_operation
#     }

#     supported_match_condition_types = [MatchConditionType.EXACT, MatchConditionType.PREFIX]
#     supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

#     try:
#         if max_deletable_files > max_deletable_files_allowed:
#             raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
#         if duplication_handling_enum not in supported_duplication_handling:
#             msg = f"Error: Duplication handling not supported. Supported types: {[dh.value for dh in supported_duplication_handling]}"
#             raise ValueError(msg)
#         if duplication_match_condition_type_enum not in supported_match_condition_types:
#             msg = f"Error: Match condition type not supported. Supported types: {[mct.value for mct in supported_match_condition_types]}"
#             raise ValueError(msg)
#         elif duplication_match_condition_type_enum != MatchConditionType.EXACT and not duplication_match_condition:
#             msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type_enum.value}"
#             raise ValueError(msg)

#         # Prepare data
#         if isinstance(data, (list, dict)):
#             data_str = json.dumps(data, indent=2)
#         else:
#             data_str = data

#         increment = 0
#         attempts = 0
#         success = False

#         # Check for existing files based on duplication_match_condition_type
#         files_matched_on_condition = []
#         bucket = storage_client.bucket(bucket_name)
#         base_file_name, ext = os.path.splitext(file_name)
#         if duplication_match_condition_type_enum == MatchConditionType.PREFIX:
#             files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
#         elif duplication_match_condition_type_enum == MatchConditionType.EXACT:
#             duplication_match_condition = file_name if not duplication_match_condition else duplication_match_condition
#             if bucket.blob(duplication_match_condition).exists():
#                 files_matched_on_condition = [bucket.blob(file_name)]

#         matched_duplicates_count = len(files_matched_on_condition)
#         response["matched_duplicates_count"] = matched_duplicates_count

#         # Handle duplication based on duplication_handling
#         if matched_duplicates_count:
#             log_msg = f"Duplicate FOUND, matched_duplicates_count: {matched_duplicates_count}"
#             if pipelinemon:
#                     pipelinemon.add_log(ContextLog(LogLevel.NOTICE_FILE_IN_CLOUD_STORAGE_ALREADY_EXISTS, subject="duplicate_found", description=log_msg))

#             if duplication_handling_enum == DuplicationHandling.RAISE_ERROR:
#                 raise FileExistsError("File(s) matching the condition already exist.")

#             if duplication_handling_enum == DuplicationHandling.SKIP:
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
#                 log_msg = f"SKIPPING, response: {response}"
#                 log_info(log_msg, logger=logger, print_out=print_out) ## only logsor prints if logger is provided and print_out is True
#                 return response

#             if duplication_handling_enum == DuplicationHandling.OVERWRITE:
#                 if matched_duplicates_count > max_deletable_files:
#                     raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

#                 for blob in files_matched_on_condition:
#                     cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
#                     blob.delete()
#                     matched_duplicates_deleted.append(cloud_storage_path_to_delete)
#                     log_msg = f"File deleted as part of overwrite: {cloud_storage_path_to_delete}"
#                     if pipelinemon:
#                         pipelinemon.add_system_impacted(f"delete: {cloud_storage_ref}_bucket_file: {cloud_storage_path_to_delete}")
#                         pipelinemon.add_log(ContextLog(LogLevel.ACTION_DELETE_IN_CLOUD_STORAGE_COMPLETE, subject="delete_duplicate", description=log_msg))
#                     log_info(log_msg, logger=logger, print_out=print_out)

#                 response["matched_duplicates_deleted"] = matched_duplicates_deleted
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value

#             elif duplication_handling_enum == DuplicationHandling.INCREMENT:
#                 while bucket.blob(file_name).exists():
#                     increment += 1
#                     file_name = f"{base_file_name}_v{increment}{ext}"
#                 saved_to_path = f"gs://{bucket_name}/{file_name}"
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value
#                 log_msg = "INCREMENTING as Duplicate FOUND "
#                 log_info(log_msg, logger=logger, print_out=print_out) ## only logsor prints if logger is provided and print_out is True

#         # GCS Upload
#         saved_to_path = f"gs://{bucket_name}/{file_name}"
#         while attempts < max_retries and not success:
#             try:
#                 blob = bucket.blob(file_name)
#                 blob.upload_from_string(data_str, content_type='application/json')
#                 log_msg = f"File uploaded to GCS: {saved_to_path}"
#                 if pipelinemon:
#                     pipelinemon.add_system_impacted(f"upload: {cloud_storage_ref}_bucket_file: {saved_to_path}")
#                     pipelinemon.add_log(ContextLog(LogLevel.ACTION_WRITE_IN_CLOUD_STORAGE_COMPLETE, subject="file_upload", description=log_msg))
#                 log_info(log_msg, logger=logger, print_out=print_out)
#                 success = True
#             except Exception as e:
#                 attempts += 1
#                 if attempts < max_retries:
#                     time.sleep(2 ** attempts)
#                 else:
#                     raise e

#     except Exception as e:
#         error_during_operation = f"Error occurred while writing JSON to GCS path: {saved_to_path} ; Error details: {type(e).__name__} - {str(e)}"
#         response["error_during_operation"] = error_during_operation
#         if pipelinemon:
#             pipelinemon.add_log(ContextLog(LogLevel.ERROR_EXCEPTION, e=e, description="response: {response}"))
#         log_error(response, logger=logger, print_out=print_out)
#         if raise_e:
#             raise e

#     response["saved_to_path"] = saved_to_path if success else None
#     return response


# def write_csv_to_gcs(bucket_name:str, file_name:str, data:dict | list | str, storage_client:GCSClient, logger=None, print_out=False, raise_e=False):
#     """ Helper function to write a CSV file to Google Cloud Storage """
#     try:
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(file_name)
#         data_file = StringIO()
#         if data and isinstance(data, list) and isinstance(data[0], dict):
#             fieldnames = data[0].keys()
#             writer = csv.DictWriter(data_file, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(data)
#         else:
#             raise ValueError("Data should be a list of dictionaries")
#         blob.upload_from_string(data_file.getvalue(), content_type='text/csv')
#         log_info(msg=f"Successfully wrote CSV to {file_name} in bucket {bucket_name}.", logger=logger, print_out=print_out)
#     except ValueError as e:
#         log_error(msg=f"ValueError: {e}",logger=logger, print_out=print_out)
#         if raise_e:
#             raise e
#     except Exception as e:
#         log_error(msg=f"An unexpected error occurred while writing CSV to GCS: {e}", logger=logger, print_out=print_out, exc_info=True)
#         if raise_e:
#             raise e



###########################################################################################
###########################################################################################
#################################### GOOGLE BIGQUERY ######################################
###########################################################################################
###########################################################################################


###########################################################################################
#################################### BIGQUERY SCHEMA FUNCTIONS ############################
###########################################################################################

def create_bigquery_schema_from_json_schema(json_schema: list) -> list:
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema


def create_bigquery_schema_from_cerberus_schema(cerberus_schema: dict) -> list:
    """Converts a Cerberus validation schema to a BigQuery schema.
        Handles 'custom_date' and 'custom_timestamp' rules as DATE and TIMESTAMP.
    """
    bq_schema = []
    for field_name, field_rules in cerberus_schema.items():
        field_type = _convert_cerberus_type_to_bigquery(field_rules)  # Pass field_name for rule checks
        mode = 'REQUIRED' if field_rules.get('required') else 'NULLABLE'
        max_length = field_rules.get('maxlength')

        field = bigquery.SchemaField(field_name, field_type, mode=mode)
        if max_length:
            field._properties['max_length'] = max_length

        bq_schema.append(field)

    return bq_schema

def _convert_cerberus_type_to_bigquery(field_rules: dict) -> str:
    """Maps a Cerberus type to a BigQuery data type, handling custom rules."""

    if 'check_with' in field_rules:
        if field_rules['check_with'] == 'standard_str_date':
            return 'DATE'
        if field_rules['check_with'] == 'iso_str_timestamp':
            return 'TIMESTAMP'
        if field_rules['check_with'] == 'standard_str_time':
            return 'TIME'

    
    # Default type mapping if no custom rule is found
    type_mapping = {
        'string': 'STRING',
        'integer': 'INT64',
        'float': 'FLOAT64',
        'boolean': 'BOOL',
        'datetime': 'TIMESTAMP',
        'date': 'DATE',
        'time': 'TIME'


    }
    # Handle the case where 'type' is a list
    field_type = field_rules.get('type', 'string')
    if isinstance(field_type, list):
        # Choose the first valid type from the list or default to 'STRING'
        for ft in field_type:
            if ft in type_mapping:
                return type_mapping[ft]
        return 'STRING'  # Default if no valid type found
    else:
        return type_mapping.get(field_type, 'STRING')


###########################################################################################
#################################### BIGQUERY CREATE TABLES ###############################
###########################################################################################
def create_bigquery_table(project_id: str,
                          dataset_name: str,
                          table_name: str,
                          schema: List[bigquery.SchemaField],
                          replace_if_exists: bool = False,
                          bigquery_client: Optional[bigquery.Client] = None,
                          pipelinemon: Optional[Pipelinemon]  = None,
                          logger: Optional[logging.Logger] = None):
    """
    Creates a BigQuery table. If create_or_replace is True, it will replace the table if it already exists.
    
    Parameters:
        project_id (str): GCP Project ID.
        dataset_name (str): BigQuery Dataset name.
        table_name (str): BigQuery Table name.
        schema (List[bigquery.SchemaField]): BigQuery table schema.
        replace_if_exists (bool): Flag to create or replace the table if it exists.
        bigquery_client (Optional[bigquery.Client]): Pre-initialized BigQuery client. If not provided, a new client is created.
        pipelinemon (Optional): Pipeline monitoring object (if applicable).
        logger (Optional[logging.Logger]): Logger for logging messages.
    """

    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)

     # Check if the DATASET exists, and create it if it does not
    dataset_ref = bigquery_client.dataset(dataset_name)
    try:
        bigquery_client.get_dataset(dataset_ref)  # Will raise NotFound if dataset does not exist
        log_info(msg=f"Dataset {dataset_name} already exists.", logger=logger)
    except NotFound:
        # Create the dataset if it doesn't exist
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Specify the location, change if needed
        dataset = bigquery_client.create_dataset(dataset)
        log_info(msg=f"Dataset {dataset_name} created.", logger=logger)
        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_create_dataset: {dataset_name}")
            pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_CREATE_COMPLETE, subject=dataset_name, description=f"Dataset created."))

     # Check if the TABLE exists before attempting to delete it
    table_ref = dataset_ref.table(table_name)
    try:
       
        table_exists = False
        try:
            bigquery_client.get_table(table_ref)
            table_exists = True
            pipelinemon.add_log(ContextLog(level=LogLevel.NOTICE_ALREADY_EXISTS, subject=table_name, description=f"Table {table_name} already existed in {dataset_name}."))
        except NotFound:
            table_exists = False
        if replace_if_exists and table_exists:
            bigquery_client.delete_table(table_ref)
            log_info(msg=f"Table {table_name} in dataset {dataset_name} was deleted.", logger=logger)
            if pipelinemon:
                pipelinemon.add_system_impacted(f"bigquery_delete_table: {table_name}")
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_DELETE_CLOUD_DB_TABLE_COMPLETE, subject=table_name, description=f"Table {table_name} deleted in dataset {dataset_name}."))

        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_create_table: {table_name}")
            pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_CREATE_CLOUD_DB_TABLE_COMPLETE, subject=table_name, description=f"Table {table_name} created in dataset {dataset_ref}."))
        log_info(msg=f"Table {table_name} created in dataset {dataset_ref}.", logger=logger)
        
    except Exception as e:
        log_error(msg=f"Error creating table {table_name} in dataset {dataset_ref}: {e}", logger=logger, exc_info=True)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_CREATE_FAILED, subject=table_name, description=f"Error creating table {table_name} in dataset {dataset_ref}: {e}"))

###########################################################################################
#################################### BIGQUERY INSERT AND MERGE ###############################
###########################################################################################

def insert_batch_into_bigquery_extended(project_id: str,
                                    data: Union[Dict[str, Any], List[Dict[str, Any]]],
                                    data_table_full_path: str,
                                    records_ref:str="data", #can be metadata , etc.
                                    max_job_errors_to_log: int=7,
                                    create_table_if_not_exists: bool=False,
                                    bigquery_client: Optional[bigquery.Client] =None,
                                    schema: Optional[List[bigquery.SchemaField]]=None,
                                    pipelinemon: Optional[Pipelinemon]=None,
                                    logger: Optional[logging.Logger] =None
                                )-> Dict[str, Any]:
    """Executes a BigQuery batch load job and logs the results.
    returns action_results: dict
    """
    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)
    action_status={
        "action_type":DataActionType.INSERT.value,
        "action_execution_state": "NOT_STARTED",
        "action_execution_details": "",
        "action_execution_errors_count": 0,
        "action_execution_exception": ""
    }
    try:
        success_action_log_levl=LogLevel.ACTION_WRITE_BULK_IN_CLOUD_DB_COMPLETE
        # Handle single record case consistently
        if isinstance(data, dict):
            data = [data]
            success_action_log_levl=LogLevel.ACTION_WRITE_IN_CLOUD_DB_COMPLETE

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Append to existing data
        if create_table_if_not_exists:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED  # Create New table if not exists
        else:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_NEVER  # Don't create Create New table if not exists

        action_status["action_execution_state"] = "INSERT_JOB_STARTED"
        job =bigquery_client.load_table_from_json(data, data_table_full_path, job_config=job_config,project=project_id)
        job.result()  # Wait for job completion
        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_load: {data_table_full_path}")
        action_status['action_execution_state'] = job.state
        action_status["action_execution_errors_count"] = len(job.errors) if job.errors else 0
        action_status["action_execution_details"]= json.dumps({
                                        "bigquery_job_id": job.job_id if job.job_id else "",
                                        "action_job_output_bytes": job.output_bytes if job.output_bytes else 0,
                                        "action_job_output_rows": job.output_rows if job.output_rows else 0,
                                        "action_job_user_email": job.user_email if job.user_email else "",
                                        "duration_ms": (job.ended - job.started).total_seconds() * 1000 if job.started and job.ended else None
                                    })
        # Check job status
        if job.state == "DONE" and job.errors is None:
            msg=f"Successful LoadJob {job.job_id} for {records_ref}. Event Results: {action_status}"
            log_debug(msg=msg)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=success_action_log_levl,subject="bigquery load_table_from_json",description=msg))
        else:
            limited_errors = job.errors[:max_job_errors_to_log]
            if len(job.errors) > max_job_errors_to_log:
                limited_errors.append({"message": f"and {len(job.errors) - max_job_errors_to_log} more errors..."})
            error_message = f"Errored Bigquery LoadJob {job.job_id} for {records_ref} for table {data_table_full_path}. Job Results: {action_status}. Errors: {limited_errors}"
            log_warning(msg=error_message, logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_WRITE_WITH_ERRORS, subject="bigquery load_table_from_json",description=error_message))
    except Exception as e:
        action_status["action_execution_exception"] = str(e)
        log_warning(msg=f"Exception occurred, Failed to execute event {action_status} for {records_ref}: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))

    return action_status


def merge_batch_into_bigquery_extended(
    project_id: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    data_table_full_path: str,
    merge_key_columns: Union[str, List[str]], # Columns to use for identifying duplicates
    records_ref: str = "data",
    max_job_errors_to_log: int = 7,
    bigquery_client: Optional[bigquery.Client] = None,
    schema: Optional[List[bigquery.SchemaField]] = None,
    pipelinemon: Optional[Pipelinemon]=None,
    logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    """
    Merges data into a BigQuery table, avoiding duplicates based on the provided merge key columns.
    Returns:
        Dict[str, Any]: Status information about the merge operation.
    """

    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)

    action_status = {
        "action_type": DataActionType.MERGE.value,
        "action_execution_state": "NOT_STARTED",
        "action_execution_details": "",
        "action_execution_errors_count": 0,
        "action_execution_exception": "",
    }
    error_occured=False

    try:
        success_action_log_level = LogLevel.ACTION_WRITE_BULK_IN_CLOUD_DB_COMPLETE
        ########## checking if data is a single record (in a dict format)
        if isinstance(data, dict):
            data = [data]
            success_action_log_level = LogLevel.ACTION_WRITE_IN_CLOUD_DB_COMPLETE

         # 1. Stage Incoming Data:
        # Extract dataset and table name
        dataset_name = data_table_full_path.split('.')[1]  # Extract the dataset name
        table_name = data_table_full_path.split('.')[2]  # Extract the table name

        # Construct the temp table name
        temp_table_name = f"{table_name}_{uuid.uuid4().hex[:8]}_temp"
        # Construct the full temp table path
        temp_table_full_path = f"{project_id}.{dataset_name}.{temp_table_name}"

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE  # Clear temp table if exists
        job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED

        action_status["action_execution_state"] = "TEMP_TABLE_LOAD_STARTED"
        job = bigquery_client.load_table_from_json(data, temp_table_full_path, job_config=job_config, project=project_id)
        job.result()  # Wait for job completion
        if pipelinemon:
            pipelinemon.add_system_impacted(f"create bigquery_temp_table: {temp_table_name}")
        action_status['action_execution_state'] = f"TEMP_TABLE_LOAD={job.state}"
        action_status["action_execution_errors_count"] = len(job.errors) if job.errors else 0
        action_status["action_execution_details"]= json.dumps({"Temp Load Job": {
                                        "bigquery_job_id": job.job_id if job.job_id else "",
                                        "action_job_output_bytes": job.output_bytes if job.output_bytes else 0,
                                        "action_job_output_rows": job.output_rows if job.output_rows else 0,
                                        "action_job_user_email": job.user_email if job.user_email else "",
                                    }})
         # Check job status
        if job.state == "DONE" and job.errors is None:
            msg=f"Successful Temp LoadJob load_table_from_json {job.job_id} for {records_ref}. Event Results: {action_status}"
            log_debug(msg=msg)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_CREATE_CLOUD_DB_TABLE_COMPLETE ,subject=temp_table_name,description=msg))
                pipelinemon.add_log(ContextLog(level=success_action_log_level,subject=temp_table_name,description=msg))
        else:
            limited_errors = job.errors[:max_job_errors_to_log]
            if len(job.errors) > max_job_errors_to_log:
                limited_errors.append({"message": f"and {len(job.errors) - max_job_errors_to_log} more errors..."})
            error_message = f"Errored Bigquery LoadJob {job.job_id} for {records_ref} for TEMP table {temp_table_name}. Job Results: {action_status}. Errors: {limited_errors}"
            log_warning(msg=error_message, logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_WRITE_WITH_ERRORS, subject=temp_table_name,description=error_message))
            return action_status

        try:
            # 2. Perform the Merge:
            if isinstance(merge_key_columns, str):
                merge_key_columns = [merge_key_columns]
            merge_condition = " AND ".join([f"target.{col} = source.{col}" for col in merge_key_columns])

            merge_query = f"""
            MERGE `{data_table_full_path}` AS target
            USING `{temp_table_full_path}` AS source
            ON {merge_condition}
            WHEN NOT MATCHED THEN
                INSERT ROW
            """
            action_status["action_execution_state"] = "MERGE_QUERY_STARTED"
            merge_job = bigquery_client.query(merge_query)
            merge_job.result()  # Wait for the merge to complete

            action_status['action_execution_state'] = f"MERGE_QUERY={merge_job.state}"
            action_status["action_execution_errors_count"] = len(merge_job.errors) if merge_job.errors else 0
        # Assuming action_status["action_execution_details"] already contains some JSON data
            existing_details = action_status.get("action_execution_details", "{}")
            existing_details_dict = json.loads(existing_details)
            merge_job_details = {
                    "bigquery_job_id": merge_job.job_id if merge_job.job_id else "",
                    "action_job_duration_ms": (merge_job.ended - merge_job.started).total_seconds() * 1000 if merge_job.started and merge_job.ended else None, 
                    "action_job_slot_millis": merge_job.slot_millis if merge_job.slot_millis else 0,  # Resource usage
                    "action_job_num_dml_affected_rows": merge_job.num_dml_affected_rows if merge_job.num_dml_affected_rows else 0, # Important for MERGE!
                    "action_total_bytes_processed": merge_job.total_bytes_processed if merge_job.total_bytes_processed else 0,
                    "action_jtotal_bytes_billed": merge_job.total_bytes_billed if merge_job.total_bytes_billed else 0,
                    "action_job_user_email": merge_job.user_email if merge_job.user_email else ""
            }
            existing_details_dict["MergeJob"]=merge_job_details
            action_status["action_execution_details"] = json.dumps(existing_details_dict)

            # Check job status
            if merge_job.state == "DONE" and merge_job.errors is None:
                msg=f"Successful MergeJob {merge_job.job_id} for {records_ref}. Event Results: {action_status}"
                log_debug(msg=msg)
                if pipelinemon:
                    pipelinemon.add_log(ContextLog(level=success_action_log_level,subject="bigquery load_table_from_json",description=msg))
            else:
                limited_errors = merge_job.errors[:max_job_errors_to_log]
                if len(merge_job.errors) > max_job_errors_to_log:
                    limited_errors.append({"message": f"and {len(merge_job.errors) - max_job_errors_to_log} more errors..."})
                error_occured=True
                error_message = f"Errored Bigquery MergeJob {merge_job.job_id} for {records_ref} for table {data_table_full_path}. merge_job Results: {action_status}. Errors: {limited_errors}"
                log_warning(msg=error_message, logger=logger)
                if pipelinemon:
                    pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_WRITE_WITH_ERRORS, subject="bigquery load_table_from_json",description=error_message))
        except Exception as e:
            action_status["action_execution_exception"] = str(e)
            log_warning(msg=f"Exception occurred, Failed to execute event {action_status} for {records_ref}: {type(e).__name__} - {str(e)}", logger=logger)
            error_occured=True
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e, description=action_status))

        # 4. Clean Up Temporary Table:
        if pipelinemon:
            pipelinemon.add_system_impacted(f"delete bigquery_temp_table: {temp_table_name}")
        # bigquery_client.delete_table(temp_table_full_path, not_found_ok=True)

        if not error_occured:
            action_status['action_execution_state'] = "MERGE_COMPLETE_TEMP_TABLE_DELETED"
        else:
            action_status['action_execution_state'] = "MERGE_FAILED_TEMP_TABLE_DELETED"
        msg=f"Temp Table {temp_table_name} Deleted. Event Results: {action_status}"
        log_debug(msg=msg)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_DELETE_CLOUD_DB_TABLE_COMPLETE,subject="bigquery load_table_from_json",description=msg))

    except Exception as e:
        action_status["action_execution_exception"] = str(e)
        log_warning(msg=f"Exception occurred, Failed to execute event {action_status} for {records_ref}: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e, description = action_status))

    return action_status



def read_query_sql_bigquery_table(project_id: str,
                             query: str,
                             bigquery_client: Optional[bigquery.Client] = None,
                             pipelinemon: Optional[Pipelinemon] = None,
                             logger: Optional[logging.Logger] = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Executes a BigQuery SQL query and logs the results.
    Args:
        project_id (str): The Google Cloud project ID.
        query (str): The SQL query to execute.
        bigquery_client (Optional[bigquery.Client], optional): The BigQuery client instance. Defaults to None.
        pipelinemon (Optional[Pipelinemon], optional): The Pipelinemon instance for monitoring. Defaults to None.
        logger (Optional[logging.Logger], optional): The logger instance. Defaults to None.
    Returns:
        Tuple[Dict[str, Any], List[Dict[str, Any]]]: A dictionary of event results and a list of query results.
    """
    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)
    action_status = {
        "action_type": DataActionType.READ.value,
        "action_execution_state": "NOT_STARTED",
        "action_execution_details": "",
        "action_execution_errors_count": 0,
        "action_execution_exception": ""
    }
    try:
        action_status["action_execution_state"] = "QUERY_JOB_STARTED"
        query_job = bigquery_client.query(query, project=project_id)
        results = query_job.result()
        action_status['action_execution_state'] = query_job.state
        action_status["action_execution_errors_count"] = len(query_job.errors) if query_job.errors else 0
        action_status["action_execution_details"] = json.dumps({
            "bigquery_job_id": query_job.job_id if query_job.job_id else "",
            "total_bytes_billed": query_job.total_bytes_billed,  # Cost-relevant information
            "total_bytes_processed": query_job.total_bytes_processed,  # Data processed by the query
            "user_email": query_job.user_email if query_job.user_email else "",
            "duration_ms": (query_job.ended - query_job.started).total_seconds() * 1000 if query_job.started and query_job.ended else None,  # Duration of the query
            "cache_hit": query_job.cache_hit,  # Indicates if query results were served from cache
            "slot_millis": query_job.slot_millis,  # Slot usage (cost-related)
            "num_dml_affected_rows": query_job.num_dml_affected_rows, # Number of rows affected (DML)
        })
        if query_job.state == 'DONE' and query_job.errors is None:
            
            results = list(query_job)
            log_debug(msg=f"Successfully executed query. Found {len(results)} records.", logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.INFO_READ_CLOUD_DB_COMPLETE, subject="query_job", description=f"Query Job Completed Successfully. Results: {action_status}"))
            return action_status, results
        else:
            log_warning(msg=f"Failed to execute query. Query Job State: {query_job.state}, Errors: {query_job.errors}", logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_READ_DB_FAILED, subject="query_job", description=f"query_job.state != 'DONE' or query_job.errors is not None.  Errors: {query_job.errors}"))
            return action_status, []
    except Exception as e:
        log_warning(msg=f"Exception occurred during querying: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        action_status["action_execution_exception"] = str(e)
        return action_status, []


def read_query_existing_dates_from_timeseries_bigquery_table(
    project_id: str,
    data_table_full_path: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    date_column: str,
    conditions: Dict[str, Any],
    start_value: Optional[Any] = None,
    end_value: Optional[Any] = None,
    bigquery_client: bigquery.Client = None,
    pipelinemon: Optional[Any] = None,
    logger: Optional[Any] = None
) -> Tuple[Dict[str, Any], Set[Any]]:
    """
    Queries existing records in BigQuery and returns a set of existing values from a specified column.
    Args:
        date_column (str): The column to check for existing records.
        conditions (Dict[str, Any]): Dictionary of fields and their corresponding values to check in the WHERE clause.
    Returns:
        Tuple[Dict[str, Any], Set[Any]]: A dictionary of event results and a set of existing values from the specified column.
    """

    # Ensure data is a list, even if a single record is passed
    if isinstance(data, dict):
        data = [data]

    action_results = {
        "action_type":DataActionType.READ.value,
        "action_execution_state": "NOT_STARTED",
        "action_execution_details": "",
        "action_execution_errors_count": 0,
        "action_execution_exception": "",
    }

    # Infer the type of the column_to_check based on the data
    first_value = data[0][date_column]
    if isinstance(first_value, datetime.datetime):
        column_type = "TIMESTAMP"
    elif isinstance(first_value, datetime.date):
        column_type = "DATE"
    elif isinstance(first_value, str):
        try:
            # Try to parse as date, assume it's a date string if successful
            datetime.datetime.strptime(first_value, '%Y-%m-%d')
            column_type = "DATE"  # Treat string dates as STRING
        except ValueError:
            column_type = "STRING"  # It's just a regular string
    else:
        column_type = "STRING"  # Default to STRING for general use

    # Sort data based on column_to_check
    data = sorted(data, key=lambda x: x[date_column], reverse=True)
    recent_value = data[0][date_column]
    oldest_value = data[-1][date_column]

    try:
        # Build the WHERE clause dynamically
        where_clauses = []
        query_parameters = []

        for field, value in conditions.items():
            where_clauses.append(f"{field} = @{field}")
            param_type = "STRING" if isinstance(value, str) else "INTEGER"  # Adjust as needed
            query_parameters.append(bigquery.ScalarQueryParameter(field, param_type, value))

        # Handle the range filter based on start_value and end_value
        if start_value is not None and end_value is not None:
            where_clauses.append(f"{date_column} BETWEEN @start_value AND @end_value")
            query_parameters.extend([
                bigquery.ScalarQueryParameter("start_value", column_type, start_value),
                bigquery.ScalarQueryParameter("end_value", column_type, end_value),
            ])
        else:
            where_clauses.append(f"{date_column} BETWEEN @oldest_value AND @recent_value")
            query_parameters.extend([
                bigquery.ScalarQueryParameter("oldest_value", column_type, oldest_value),
                bigquery.ScalarQueryParameter("recent_value", column_type, recent_value),
            ])

        where_clause = " AND ".join(where_clauses)

        query = f"""
        SELECT {date_column} FROM `{data_table_full_path}`
        WHERE {where_clause}
        """
#### EXAMPLE
# query = f"""SELECT date_id FROM `{data_table_full_path}`
#              WHERE asset_id = @asset_id AND date_id BETWEEN @records_oldest_date AND @records_recent_date  """
#  job_config = bigquery.QueryJobConfig(
#                   query_parameters=[bigquery.ScalarQueryParameter("asset_id", "STRING", asset_id),
                            #         bigquery.ScalarQueryParameter("records_recent_date", "DATE", sourced_records_recent_date),
                            #         bigquery.ScalarQueryParameter("records_oldest_date", "DATE", sourced_records_oldest_date))   


        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        action_results["action_execution_state"] = "QUERY_JOB_STARTED"
        query_job = bigquery_client.query(query, job_config=job_config, project=project_id)
        results = query_job.result()
        action_results['action_execution_state'] = query_job.state
        action_results["action_execution_errors_count"] = len(query_job.errors) if query_job.errors else 0
        action_results["action_execution_details"]= json.dumps({"bigquery_job_id": query_job.job_id if query_job.job_id else "",
                                                    "total_bytes_billed": query_job.total_bytes_billed,  # Cost-relevant information
                                                    "total_bytes_processed": query_job.total_bytes_processed, # Data processed by the query
                                                    "user_email": query_job.user_email if query_job.user_email else "",
                                                    "duration_ms": (query_job.ended - query_job.started).total_seconds() * 1000 if query_job.started and query_job.ended else None,  # Duration of the query
                                                    "cache_hit": query_job.cache_hit,  # Indicates if query results were served from cache
                                                    "slot_millis": query_job.slot_millis,  # Slot usage (cost-related)
                                                    "num_dml_affected_rows": query_job.num_dml_affected_rows, # Number of rows affected (DML)
                                                    })     
        if query_job.state != 'DONE' or query_job.errors is not None:
            log_warning(msg=f"Failed to query existing records from BigQuery. Query Job State: {query_job.state}, Errors: {query_job.errors}", logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_READ_DB_FAILED, subject="query_job", description="query_job.state != 'DONE' or query_job.errors is not None"))
            return action_results, set()

        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.INFO_READ_CLOUD_DB_COMPLETE, subject="query_job", description=f"Query Job Completed Successfully. Results: {action_results}"))

        # Keep received types as they are such as TIMESTAMP as datetime object but convert DATE to String
        if column_type == "DATE":
            existing_values = {row[date_column].strftime('%Y-%m-%d') for row in results}
        else:
            existing_values = {row[date_column] for row in results}

        log_debug(msg=f"Found {len(existing_values)} existing records.", logger=logger)
        return action_results, existing_values

    except Exception as e:
        log_warning(msg=f"Exception occurred during querying: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        action_results["action_execution_exception"] = str(e)
        return action_results, set()


def write_query_sql_bigquery_table(project_id: str,
                                    query: str,
                                    bigquery_client: Optional[bigquery.Client] = None,
                                    pipelinemon: Optional[Pipelinemon] = None,
                                    logger: Optional[logging.Logger] = None) -> Dict[str, Any]:
    """Executes a BigQuery SQL query for write operations and logs the results."""
    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)

    action_status = {
        "action_type": DataActionType.WRITE.value,
        "action_execution_state": "NOT_STARTED",
        "action_execution_details": "",
        "action_execution_errors_count": 0,
        "action_execution_exception": ""
    }
    
    try:
        action_status["action_execution_state"] = "WRITE_JOB_STARTED"
        query_job = bigquery_client.query(query, project=project_id)
        query_job.result()  # Wait for the job to complete
        
        action_status["action_execution_state"] = query_job.state
        action_status["action_execution_details"] = json.dumps({
            "bigquery_job_id": query_job.job_id,
            "total_bytes_billed": query_job.total_bytes_billed,
            "num_dml_affected_rows": query_job.num_dml_affected_rows,
            "user_email": query_job.user_email,
            "slot_millis": query_job.slot_millis
        })
        
        if query_job.errors:
            action_status["action_execution_errors_count"] = len(query_job.errors)
            raise RuntimeError(f"Write job failed with errors: {query_job.errors}")
        
        log_debug(f"Successfully executed write query. Rows affected: {query_job.num_dml_affected_rows}.", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_WRITE_IN_CLOUD_DB_COMPLETE, subject="write_query_sql_job", description="Write sql query completed successfully."))
        
        return action_status

    except Exception as e:
        action_status["action_execution_exception"] = str(e)
        log_warning(f"Exception occurred during write query: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        
        return action_status