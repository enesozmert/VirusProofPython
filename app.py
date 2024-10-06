from flask import Flask, request, jsonify
import signal
import sys
import logging
import threading
import subprocess
from database import execute_query, fetch_data
from queryforchart import get_total_scan_data
from weekly_scan_data import get_weekly_scan_data
from algorithm import main

# Loglama ayarları
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/vagrant/pythonapp.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

print("Logging setup tamam.")  # Bu aşamanın geçtiğini kontrol ediyoruz

app = Flask(__name__)
print("Flask app oluşturuldu.")  # Flask app nesnesinin oluşturulduğunu kontrol ediyoruz

def signal_handler(sig, frame):
    logging.info('Exiting gracefully...')
    print("Çıkış yapılıyor.")  # Signal handler kontrolü
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print("Signal handler ayarlandı.")  # Signal handler'ın ayarlandığını kontrol ediyoruz

@app.route('/api/scan-data-haftalik', methods=['GET'])
def scan_data():
    logging.info("API request received for scan data.")
    print("API isteği alındı.")  # API isteği alındığını kontrol ediyoruz
    
    data = get_weekly_scan_data()
    print("Veri çekildi.")  # get_weekly_scan_data çalışmasını kontrol ediyoruz
    
    if data:
        logging.info(f"Data successfully fetched: {data}")
        print("Veri başarıyla çekildi.")  # Veri başarılı şekilde çekildiğini kontrol ediyoruz
        return jsonify(data), 200
    else:
        logging.error("Error: Data could not be fetched.")
        print("Veri çekilemedi.")  # Veri çekilemezse hata mesajı
        return jsonify({"error": "Data could not be fetched"}), 500

@app.route('/api/total-scan-data', methods=['GET'])
def total_scan_data():
    logging.info("API request received for total scan data.")
    print("API isteği alındı.")  # API isteği alındığını kontrol ediyoruz
    
    total_entries = get_total_scan_data()
    print("Veri çekildi.")  # get_total_scan_data çalışmasını kontrol ediyoruz
    
    if total_entries is not None:
        logging.info(f"Total scan data successfully fetched: {total_entries}")
        print("Veri başarıyla çekildi.")  # Veri başarılı şekilde çekildiğini kontrol ediyoruz
        return jsonify({"total_entries": total_entries}), 200
    else:
        logging.error("Error: Total scan data could not be fetched.")
        print("Veri çekilemedi.")  # Veri çekilemezse hata mesajı
        return jsonify({"error": "Total scan data could not be fetched"}), 500

@app.route('/api/algorithm', methods=['GET'])
def run_algorithm():
    logging.info("API called to run algorithm...")
    
    # scanGuid parametresini isteğin query string'inden alıyoruz
    scan_guid = request.args.get('scanGuid')
    
    if not scan_guid:
        return jsonify({"error": "scanGuid parametresi eksik"}), 400
    
    result = main(scan_guid)  # scanGuid'i algorithm.py'deki main fonksiyonuna ilet
    
    if "No need to run algorithm" in result:
        return jsonify({"message": "No need to run algorithm, data is up-to-date"}), 200
    else:
        return jsonify({"result": result}), 200
if __name__ == '__main__':
    logging.info('Starting Flask app')

    print("Flask app başlatılıyor.")  # Flask uygulamasının başlatıldığını kontrol ediyoruz
    app.run(host="0.0.0.0", debug=True, port=7777)