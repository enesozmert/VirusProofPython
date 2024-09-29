import os
import time
import logging
import requests
import json

JSON_FILE = 'avcomperative.json'

def is_json_file_recent():
    try:
        file_mod_time = os.path.getmtime(JSON_FILE)
        current_time = time.time()
        return (current_time - file_mod_time) < 60  # 60 saniyede bir güncellensin
    except FileNotFoundError:
        logging.info("JSON file not found, needs to be generated.")
        return False

def fetch_data_from_api():
    logging.info("Fetching scan engine data from API...")
    try:
        response = requests.get('http://localhost:5000/api/ScanEngineRanks/pagination?skip=0&take=100')
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])  # 'data' key'i altındaki listeyi al
    except requests.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return None

def process_and_save_data(data):
    processed_data = [{"name": item.get("scanEngineName"), "score": item.get("rank")}
                      for item in data if item.get("scanEngineName") and item.get("rank")]

    try:
        with open(JSON_FILE, 'w') as json_file:
            json.dump(processed_data, json_file, indent=4)
        logging.info("Data successfully written to avcomperative.json.")
    except Exception as e:
        logging.error(f"Error writing data to JSON file: {e}")

def run_rank_update():
    if is_json_file_recent():
        logging.info("JSON file is recent. No need to fetch new data.")
        return "No need to run algorithm, data is up-to-date."
    
    data = fetch_data_from_api()
    if data:
        process_and_save_data(data)
        logging.info("Rank data updated successfully.")
        return "Algorithm executed successfully"
    else:
        return "Failed to fetch data"
