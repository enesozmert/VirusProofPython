import logging
import requests

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Temp-mail alma fonksiyonu
def get_temp_mail(proxy):
    try:
        response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox', proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        temp_mail = response.json()[0]
        logging.info(f"Temp-mail created: {temp_mail}")
        return temp_mail
    except requests.RequestException as e:
        logging.error(f"Failed to get temp-mail: {e}")
        return None
