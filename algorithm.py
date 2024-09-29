import requests
import logging
import json
import os
import time

# Loglama ayarları, tüm loglar '/vagrant/pythonapp.log' dosyasına yazılacak
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# JSON dosyasının yolu
json_file_path = 'avcomperative.json'

# 24 saat yerine 1 dakikayı saniye cinsinden hesapla (test amaçlı)
ONE_MINUTE_IN_SECONDS = 60

# JSON dosyasının son değişiklik zamanını kontrol eden fonksiyon
def is_json_file_recent():
    if os.path.exists(json_file_path):
        last_modified_time = os.path.getmtime(json_file_path)
        current_time = time.time()
        # Eğer dosya son 1 dakika içinde değiştirilmişse True döner
        return (current_time - last_modified_time) < ONE_MINUTE_IN_SECONDS
    return False

# API'dan veri çekme fonksiyonu
def fetch_scan_engine_data():
    logging.info("Fetching scan engine data from API...")
    try:
        response = requests.get('http://localhost:5000/api/ScanEngineRanks/pagination?skip=0&take=100')
        response.raise_for_status()  # Eğer hata oluşursa HTTPError fırlatır
        data = response.json()
        logging.info("Data successfully fetched from API.")
        return data.get('data')  # Anahtar 'data' altındaki listeyi döndür
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return None

# Veriyi işleme ve JSON dosyasına kaydetme fonksiyonu
def process_and_save_data(data):
    logging.info("Processing data...")
    processed_data = []

    # Gelen verinin bir liste olduğunu kontrol et
    if isinstance(data, list):
        for item in data:
            scan_engine_name = item.get('scanEngineName')
            rank = item.get('rank')
            if scan_engine_name and rank is not None:
                processed_data.append({
                    "name": scan_engine_name,
                    "score": rank
                })

        logging.info("Data processing completed.")

        # JSON dosyasına yazma
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(processed_data, json_file, indent=4)
            logging.info("Data successfully written to avcomperative.json.")
        except Exception as e:
            logging.error(f"Error writing data to JSON file: {e}")
    else:
        logging.error("Expected a list from API response but got something else.")

def main():
    logging.info("Starting algorithm script...")

    if is_json_file_recent():
        logging.info("JSON file is recent. No need to fetch new data.")
        return False  # Güncelleme yapılmadı
    else:
        logging.info("JSON file is outdated or does not exist. Fetching new data...")

    data = fetch_scan_engine_data()
    if data:
        process_and_save_data(data)
        logging.info("Algorithm script completed.")
        return True  # Güncelleme yapıldı
    else:
        logging.error("No data to process.")
        return False  # Hata durumu

if __name__ == "__main__":
    main()
