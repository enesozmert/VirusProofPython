import time
import logging
from database import fetch_data

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def run_query_for_chart():
    while True:
        total_entries = 0
        try:
            query = "SELECT COUNT(id) FROM scans"
            result = fetch_data(query)
            total_entries = result[0][0] if result else 0

            logging.info(f"Total entries in scans table: {total_entries}")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(60)
        with open('queryforchart.txt', 'a') as file:
            file.write(f"Total entries in scans table: {total_entries}\n")
