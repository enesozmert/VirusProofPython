import requests
import threading
from datetime import datetime
import logging
from database import execute_query
from database import get_connection

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

class FetchAndUpdateData:
    def __init__(self):
        self.timer = None
        self.previous_day_scan_count = 0

    def fetch_and_update_data(self):
        logging.debug('Fetching and updating data')
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if datetime.now().weekday() == 0 and datetime.now().hour == 0:
                execute_query("UPDATE WebHit SET PreviousWeekScanCount = ScanCount")
                execute_query("UPDATE WebHit SET ScanCount = 0")
                self.previous_day_scan_count = 0

            response = requests.get('http://localhost:5000/api/Scans/GetScanCount')
            data = response.json()

            if data['success']:
                total_scan_count = data['data']
                day_of_week = datetime.now().strftime('%A')

                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    self.previous_day_scan_count = total_scan_count
                    execute_query("UPDATE WebHit SET ScanCount = 0 WHERE DayOfWeek = ?", [day_of_week])

                scan_count = total_scan_count - self.previous_day_scan_count
                logging.info(f'Total Scan Count: {total_scan_count}, Previous Day Scan Count: {self.previous_day_scan_count}, Scan Count: {scan_count}, Day of Week: {day_of_week}')

                execute_query("UPDATE WebHit SET ScanCount = ? WHERE DayOfWeek = ?", [scan_count, day_of_week])

            self.timer = threading.Timer(60, self.fetch_and_update_data)
            self.timer.start()
        except Exception as e:
            logging.error(f'Error in fetch_and_update_data: {e}')

    def start(self):
        self.fetch_and_update_data()

    def stop(self):
        if self.timer:
            self.timer.cancel()

fetch_and_update_data = FetchAndUpdateData()
