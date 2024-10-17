import logging
from .virustotalbot_proxy import get_working_proxy
from .virustotalbot_mail import get_temp_mail
from .virustotal_registration import register_virustotal  # Düzeltme
import json

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def test_virustotal_bot():
    logging.info("Starting VirusTotalBot...")

    # Proxy alma işlemi
    proxy = get_working_proxy()
    if proxy:
        logging.info(f"Using proxy: {proxy}")
    else:
        logging.error("No working proxy available. Exiting.")
        return

    # Temp-mail al
    temp_email = get_temp_mail(proxy)
    if temp_email:
        logging.info(f"Temp-mail created: {temp_email}")
    else:
        logging.error("Failed to get temp-mail. Exiting.")
        return

    # VirusTotal'a kayıt
    username, password = generate_random_credentials()  # Kayıt için kullanıcı bilgileri oluşturulmalı
    driver = start_browser_with_proxy(proxy)
    register_virustotal(driver, temp_email, username, password)  # register_and_get_api yerine bu kullanılır

    logging.info("VirusTotalBot test completed successfully.")
    return "VirusTotalBot çalıştı, yeni API çekti."

if __name__ == "__main__":
    test_virustotal_bot()
