import logging
from bot.virustotalbot_proxy import main as get_proxy  # Proxy fonksiyonunu ekliyoruz
from bot.virustotalbot_mail import get_temp_mail, register_and_get_api  # Mail işlemleri için
import json

logging.basicConfig(filename='/vagrant/pythonapp.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


def test_virustotal_bot():
    logging.info("Starting VirusTotalBot...")

    # Proxy alma işlemi
    proxy = get_proxy()
    logging.info(f"Using proxy: {proxy}")

    # Temp-mail al
    temp_email = get_temp_mail(proxy)
    logging.info(f"Temp-mail created: {temp_email}")

    # VirusTotal'a kayıt olup API anahtarını alma
    api_key = register_and_get_api(temp_email, proxy)
    logging.info(f"API Key received: {api_key}")

    # API key'i kaydetme
    if api_key:
        with open('/bot/virustotal_api.json', 'w') as f:
            f.write(json.dumps({'api_key': api_key}))
        logging.info("API key saved to virustotal_api.json.")
    else:
        logging.error("Failed to retrieve API key.")

    logging.info("VirusTotalBot test completed successfully.")
    return "VirusTotalBot çalıştı, yeni API çekti."

if __name__ == "__main__":
    test_virustotal_bot()
