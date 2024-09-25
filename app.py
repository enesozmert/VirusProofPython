from flask import Flask, jsonify
import signal
import sys
import logging
from database import execute_query, fetch_data
from queryforchart import run_query_for_chart
from weekly_scan_data import get_weekly_scan_data  # Yeni modülü ekliyoruz

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

def signal_handler(sig, frame):
    logging.info('Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.route('/api/scan-data', methods=['GET'])
def scan_data():
    logging.info("API request received for scan data.")
    data = get_weekly_scan_data()
    if data:
        logging.info(f"Data successfully fetched: {data}")
        return jsonify(data), 200
    else:
        logging.error("Error: Data could not be fetched.")
        return jsonify({"error": "Data could not be fetched"}), 500

if __name__ == '__main__':
    logging.info('Running query for chart')
    run_query_for_chart()
    logging.info('Starting Flask app')
    app.run(host="0.0.0.0", debug=True, port=7777)
