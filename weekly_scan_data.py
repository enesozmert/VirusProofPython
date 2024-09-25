import logging
from database import fetch_data

# Loglama ayarları
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def get_weekly_scan_data():
    logging.info("Fetching weekly scan data...")
    try:
        # Bu haftanın tarama verilerini getir
        logging.debug("Fetching current week data...")
        query_current_week = "SELECT DayOfWeek, ScanCount FROM WebHit WHERE DayOrder BETWEEN 1 AND 7"
        current_week_data = fetch_data(query_current_week)

        # Geçen haftanın tarama verilerini getir
        logging.debug("Fetching previous week data...")
        query_previous_week = "SELECT DayOfWeek, PreviousWeekScanCount FROM WebHit WHERE DayOrder BETWEEN 1 AND 7"
        previous_week_data = fetch_data(query_previous_week)

        # Verileri birleştir
        current_week = [row[1] for row in current_week_data]
        previous_week = [row[1] for row in previous_week_data]

        # JSON formatında veriyi döndür
        data = {
            'current_week': current_week,
            'previous_week': previous_week
        }

        logging.info(f'Weekly scan data fetched successfully: {data}')
        return data

    except Exception as e:
        logging.error(f'Error fetching weekly scan data: {e}')
        return None
