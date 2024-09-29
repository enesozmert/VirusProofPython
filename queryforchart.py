import logging
from database import fetch_data

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def get_total_scan_data():
    try:
        logging.info("Fetching total scan data from scans table...")
        query = "SELECT COUNT(id) FROM scans"
        result = fetch_data(query)
        total_entries = result[0][0] if result else 0
        logging.info(f"Total entries in scans table: {total_entries}")
        return total_entries
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None