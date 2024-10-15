import logging
from database import fetch_data

# Logging yapılandırması
logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG, 
					format='%(asctime)s %(levelname)s:%(message)s')

def get_weekly_scan_data():
	logging.info("Fetching weekly scan data from WebHit table...")
	try:
		# Bu haftanın başlangıç tarihini ve geçen haftanın başlangıç tarihini al
		query_current_week = """
		SELECT Date, ScanCount FROM dbo.WebHit
		WHERE Date >= CONVERT(DATE, GETDATE() - 6) 
		AND Date <= CONVERT(DATE, GETDATE())
		"""
		current_week_data = fetch_data(query_current_week)
		logging.debug(f"Bu haftaki veri: {current_week_data}")

		if not current_week_data:
			logging.warning("No data found for current week.")

		# Geçen haftanın tarama verilerini getir
		query_previous_week = """
		SELECT Date, ScanCount FROM dbo.WebHit
		WHERE Date >= CONVERT(DATE, GETDATE() - 14)
		AND Date < CONVERT(DATE, GETDATE() - 6)
		"""
		previous_week_data = fetch_data(query_previous_week)
		logging.debug(f"Geçen haftaki veri: {previous_week_data}")

		if not previous_week_data:
			logging.warning("No data found for previous week.")

		# Verileri birleştir
		current_week = [row[1] for row in current_week_data] if current_week_data else []
		previous_week = [row[1] for row in previous_week_data] if previous_week_data else []

		logging.info(f"Veriler birleştirildi. Bu hafta: {current_week}, Geçen hafta: {previous_week}")
		return {
			'current_week': current_week,
			'previous_week': previous_week
		}

	except Exception as e:
		logging.error(f'Error fetching weekly scan data from WebHit table: {e}')
		return None
