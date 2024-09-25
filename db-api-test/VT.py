import os
import requests
import json
import time

def get_api_key():
    with open('API-KEY', 'r') as file:
        return file.read().strip()

def scan_file(file_path, api_key):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {
        'x-apikey': api_key
    }
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file)
        }
        response = requests.post(url, headers=headers, files=files)
    return response.json()

def get_analysis_result(analysis_id, api_key):
    url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
    headers = {
        'x-apikey': api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    file_path = input("Lütfen taranacak dosyanın yolunu girin: ")
    if not os.path.exists(file_path):
        print("Dosya bulunamadı!")
        return
    
    api_key = get_api_key()
    initial_result = scan_file(file_path, api_key)
    
    analysis_id = initial_result['data']['id']
    print(f"Analiz ID: {analysis_id}")
    
    while True:
        result = get_analysis_result(analysis_id, api_key)
        if result['data']['attributes']['status'] == 'completed':
            break
        print("Analiz devam ediyor, lütfen bekleyin...")
        time.sleep(10) 
    
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()