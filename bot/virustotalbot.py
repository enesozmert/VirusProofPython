import logging
from .virustotalbot_proxy import get_working_proxy
from .virustotalbot_mail import get_temp_mail
from .virustotal_registration import register_virustotal, start_browser_with_proxy  # start_browser_with_proxy de eklendi
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
    logging.info(f"Generated credentials for VirusTotal: Username - {username}, Password - {password}")

    try:
        logging.info("Starting Selenium browser with proxy...")
        driver = start_browser_with_proxy(proxy)
        if driver:
            logging.info("Selenium browser successfully started with proxy.")
        else:
            logging.error("Failed to start the Selenium browser. Exiting.")
            return

        register_virustotal(driver, temp_email, username, password)
    except Exception as e:
        logging.error(f"Failed to start Selenium or register on VirusTotal: {e}")

    logging.info("VirusTotalBot test completed successfully.")
    return "VirusTotalBot çalıştı, yeni API çekti."

if __name__ == "__main__":
    test_virustotal_bot()
