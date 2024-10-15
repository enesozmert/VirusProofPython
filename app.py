from flask import Flask, request, jsonify
import signal
import sys
import logging
import threading
import subprocess
from database import execute_query, fetch_data
from chart.queryforchart import get_total_scan_data
from chart.weekly_scan_data import get_weekly_scan_data
from algoritma.algorithm import main
from flask_cors import CORS
from rank.rank import run_rank_update
from bot.hybridanalysisbot import test_hybrid_analysis_bot
from bot.virustotalbot import test_virustotal_bot

# Loglama ayarları
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("/vagrant/pythonapp.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

print("Logging setup tamam.")  # Bu aşamanın geçtiğini kontrol ediyoruz

app = Flask(__name__)
# Flask app nesnesinin oluşturulduğunu kontrol ediyoruz
print("Flask app oluşturuldu.")


def signal_handler(sig, frame):
    logging.info("Exiting gracefully...")
    print("Çıkış yapılıyor.")  # Signal handler kontrolü
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# Signal handler'ın ayarlandığını kontrol ediyoruz
print("Signal handler ayarlandı.")


@app.route("/api/scan-data-haftalik", methods=["GET"])
def scan_data():
    logging.info("API request received for scan data.")
    print("API isteği alındı.")  # API isteği alındığını kontrol ediyoruz

    data = get_weekly_scan_data()
    print("Veri çekildi.")  # get_weekly_scan_data çalışmasını kontrol ediyoruz

    if data:
        logging.info(f"Data successfully fetched: {data}")
        print(
            "Veri başarıyla çekildi."
        )  # Veri başarılı şekilde çekildiğini kontrol ediyoruz
        return jsonify(data), 200
    else:
        logging.error("Error: Data could not be fetched.")
        print("Veri çekilemedi.")  # Veri çekilemezse hata mesajı
        return jsonify({"error": "Data could not be fetched"}), 500


@app.route("/api/total-scan-data", methods=["GET"])
def total_scan_data():
    logging.info("API request received for total scan data.")
    print("API isteği alındı.")  # API isteği alındığını kontrol ediyoruz

    total_entries = get_total_scan_data()
    print("Veri çekildi.")  # get_total_scan_data çalışmasını kontrol ediyoruz

    if total_entries is not None:
        logging.info(f"Total scan data successfully fetched: {total_entries}")
        print(
            "Veri başarıyla çekildi."
        )  # Veri başarılı şekilde çekildiğini kontrol ediyoruz
        return jsonify({"total_entries": total_entries}), 200
    else:
        logging.error("Error: Total scan data could not be fetched.")
        print("Veri çekilemedi.")  # Veri çekilemezse hata mesajı
        return jsonify({"error": "Total scan data could not be fetched"}), 500


@app.route("/api/algorithm", methods=["GET"])
def run_algorithm():
    scan_guid = request.args.get("scanGuid")

    if not scan_guid:
        return jsonify({"error": "scanGuid parametresi eksik"}), 400

    result = main(scan_guid)  # scanGuid'i algorithm.py'deki main fonksiyonuna ilet
    return jsonify(result), 200


@app.route("/api/rank-update", methods=["GET"])
def update_ranks():
    result = run_rank_update()
    return jsonify({"message": result}), 200


@app.route("/api/ApiBot", methods=["GET"])
def run_bot_tests():
    # Hybrid Analysis botunu çalıştır
    hybrid_result = test_hybrid_analysis_bot()
    logging.info(f"Hybrid Analysis bot result: {hybrid_result}")

    # VirusTotal botunu çalıştır
    virustotal_result = test_virustotal_bot()
    logging.info(f"VirusTotal bot result: {virustotal_result}")

    # Sonuçları döndür
    return (
        jsonify(
            {"message_hybrid": hybrid_result, "message_virustotal": virustotal_result}
        ),
        200,
    )


# CORS ayarları
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


if __name__ == "__main__":
    logging.info("Starting Flask app")

    print(
        "Flask app başlatılıyor."
    )  # Flask uygulamasının başlatıldığını kontrol ediyoruz
    app.run(host="0.0.0.0", debug=True, port=7777)
