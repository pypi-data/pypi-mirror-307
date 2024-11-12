import os
import json
import glob 
import pandas as pd
from decimal import Decimal

def walk_find_json(json_directory:str):
    files_list = list(glob.glob(json_directory.rstrip()+"/*.json"))
    return files_list

# def load_json(all_files):
#     # file_path = os.path.join(json_directory, json_file)
#     file_path = glob.glob("/mnt/sfs-shelfaudit-data/ugendar/Code/All_Meta_files_UD/*.json")
#     # details = extract_json_details(file_path)
#     # all_files.append(details)
#     return file_path

def open_and_load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data
        
# Function to extract details from the JSON files
def extract_json_details(data, file_path):
        # Extract and convert the timestamps to Decimal for higher precision
        ios_start_time = data.get("timestamp", {}).get("startTime", "N/A")
        ios_end_time = data.get("timestamp", {}).get("endTime", "N/A")
        android_start_time = data.get("timeStamp", {}).get("recordingStartTime", "N/A")
        android_end_time = data.get("timeStamp", {}).get("recordingEndTime", "N/A")

        # Convert float timestamps to Decimal
        ios_start_time = str(ios_start_time) if isinstance(ios_start_time, (float, str)) else ios_start_time
        ios_end_time = str(ios_end_time) if isinstance(ios_end_time, (float, str)) else ios_end_time
        android_start_time = str(android_start_time) if isinstance(android_start_time, (float, str)) else android_start_time
        android_end_time = str(android_end_time) if isinstance(android_end_time, (float, str)) else android_end_time
        if "androidID" in data["dataObject"]:
            merge_key = str(data["dataObject"]["androidID"]) + "_" + str(android_start_time)
        elif "uuid" in data["deviceInfo"]:
            merge_key = str(data["deviceInfo"]["uuid"]) + "_" + str(ios_start_time)
        else:
            raise Exception(f"Device should be neither android and ios, but we are getting error in: {file_path}")
        # Flatten the JSON data as needed
        details = {
            "file_name": os.path.basename(file_path),
            "ios_timestamp_startTime": ios_start_time,
            "ios_timestamp_EndTime": ios_end_time,
            "android_timestamp_startTime": android_start_time,
            "android_timestamp_endTime": android_end_time,
            "collector_name": data.get("storeDetails", {}).get("collectorName", "N/A"),
            "retailer_name": data.get("storeDetails", {}).get("retailerName", "N/A"),
            "store_name": data.get("storeDetails", {}).get("storeName", "N/A"),
            "store_id": data.get("storeDetails", {}).get("storeID", "N/A"),
            "location": data.get("storeDetails", {}).get("location", "N/A"),
            "device_model": data.get("dataObject", {}).get("deviceModel", "N/A"),
            "android_id": data.get("dataObject", {}).get("androidID", "N/A"),
            "android_bersion": data.get("dataObject", {}).get("androidVersion", "N/A"),
            "uuid": data.get("deviceInfo", {}).get("uuid", "N/A"),
            "app_version": data.get("deviceInfo", {}).get("appVersion", "N/A"),
            "model": data.get("deviceInfo", {}).get("model", "N/A"),
            "os_version": data.get("deviceInfo", {}).get("osVersion", "N/A"),
            "merge_key": merge_key
            # Add more fields as required
        }
        
        return details
    
def create_df_to_display(all_data,spread_sheet_name ="json_files_details_Data_Upload.xlsx" ,write_df = False):
    # Create a DataFrame from the details list
    df = pd.DataFrame(all_data)

    # Set pandas display options to avoid rounding
    pd.options.display.float_format = '{:.15f}'.format
    if write_df:
        # Save the DataFrame to an Excel file with high precision
        df.to_excel(spread_sheet_name, index=False, float_format='%.15f')
        print(f"Spreadsheet {spread_sheet_name} has been created with the sliced file names and details.")
    return df
    
def transform_data(file_path):
    json_data= open_and_load_json(file_path)
    details = extract_json_details(json_data,file_path)
    return details  

def generate_metadata(json_directory,write_df = False):           
    files = walk_find_json(json_directory)
    base_name = os.path.basename(json_directory.rstrip("/"))
    # load_json(all_files)
    list_data = []
    for f in files:
        list_data.append(transform_data(f)) 
    df = create_df_to_display(list_data,base_name+"_metadata.xlsx",write_df)
    #pattern = r'^(?:android_|ios_)(.*?)(?:_data)'
    #df["merge_key"] = df['file_name'].str.extract(pattern)
    return df