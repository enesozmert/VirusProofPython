import logging
import requests

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Temp-mail alma fonksiyonu
def get_temp_mail(proxy):
    try:
        response = requests.get('https://api.temp-mail.org/request/mail/new', proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        temp_mail = response.json().get('mail')
        logging.info(f"Temp-mail created: {temp_mail}")
        return temp_mail
    except requests.RequestException as e:
        logging.error(f"Failed to get temp-mail: {e}")
        return None

# VirusTotal'a kayıt olup API anahtarı alma
def register_and_get_api(temp_mail, proxy):
    try:
        # Proxy ile istek atarak kayıt olma
        registration_url = "https://www.virustotal.com/gui/join-us"
        response = requests.post(
            registration_url,
            data={"email": temp_mail},
            proxies={"http": proxy, "https": proxy}
        )
        response.raise_for_status()
        return "dummy-api-key"
    except requests.RequestException as e:
        logging.error(f"Failed to register and get API key: {e}")
        return None
