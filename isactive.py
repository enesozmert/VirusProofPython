import requests
import logging
import threading
from database import fetch_data, execute_query

logging.basicConfig(filename='isactivelog.txt', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

class IsActiveChecker:
    def __init__(self):
        self.timer = None

    def check_api_status(self):
        try:
            query = """
            SELECT TOP (1000) [Id], [ApiId], [APIKey], [Status]
            FROM [VirusProofs].[dbo].[ScanApiCredentials]
            """
            api_credentials = fetch_data(query)

            for cred in api_credentials:
                api_key = cred[2]  # APIKey column is at index 2
                status = self.is_api_key_active(api_key)
                self.update_api_status(cred[0], status)
            
            self.timer = threading.Timer(60, self.check_api_status)  # 1 minute
            self.timer.start()
        except Exception as e:
            logging.error(f'Error in check_api_status: {e}')

    def is_api_key_active(self, api_key):
        try:
            # Replace this URL with the actual API endpoint to check API key status
            response = requests.get(f'https://api.example.com/status?key={api_key}')
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('status') == 'valid':
                    return 1  # API is active
                else:
                    logging.info(f'API key {api_key} is invalid: {response_json}')
                    return 0  # API is inactive
            else:
                logging.warning(f'API key {api_key} check failed with status code: {response.status_code}')
                return 0  # API is inactive
        except requests.exceptions.RequestException as e:
            logging.error(f'Error checking API key {api_key}: {e}')
            return 0  # API is inactive

    def update_api_status(self, api_id, status):
        try:
            update_query = """
            UPDATE [VirusProofs].[dbo].[ScanApiCredentials]
            SET [Status] = ?
            WHERE [Id] = ?
            """
            execute_query(update_query, [status, api_id])
            logging.info(f'Updated API ID {api_id} status to {status}')
        except Exception as e:
            logging.error(f'Error updating API ID {api_id} status: {e}')

    def start(self):
        self.check_api_status()

    def stop(self):
        if self.timer:
            self.timer.cancel()

is_active_checker = IsActiveChecker()
